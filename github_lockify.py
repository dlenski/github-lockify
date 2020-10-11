#!/usr/bin/env python3

import argparse
import requests
from urllib import parse
from datetime import datetime, timedelta

def _parse_github_time(t):
    return t and datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
def _days(d):
    return timedelta(days=int(d))

def main(args = None):
    p = argparse.ArgumentParser(description='Lock closed GitHub issues en masse.')
    p.add_argument('owner', help='GitHub repository owner')
    p.add_argument('repo', help='Github repository name')
    p.add_argument('--do-it', action='store_true', help='Actually lock the issues (default is a dry-run where issues are simply listed).')
    p.add_argument('-r', '--lock-reason', choices=['off-topic','too heated','resolved','spam'], default='resolved', help='Lock-reason to apply (default %(default)s)')
    g = p.add_argument_group('Authentication', description='Not required for a dry-run (except on a private repo), but required to actually lock issues.')
    g.add_argument('-t', '--token', help='GitHub personal access token with repo scope (see https://github.com/settings/tokens).')
    g = p.add_argument_group('Selecting closed issues to lock', description='All criteria must match in order for an issue to be locked.')
    g.add_argument('-U','--updated-age', metavar='DAYS', type=_days, help='Only lock if last UPDATED at least this many days ago')
    g.add_argument('-C','--closed-age', metavar='DAYS', type=_days, help='Only lock if CLOSED at least this many days ago')
    g.add_argument('--created-age', metavar='DAYS', type=_days, help='Only lock if CREATED at least this many days ago')
    g.add_argument('-l', '--label', default=[], action='append', help='Only lock if this label is applied (may be specified repeatedly to require multiple labels)')
    g.add_argument('-a','--assignee', metavar='USERNAME', help='Only lock if assigned to this user ("none" for unassigned)')
    g.add_argument('-c','--creator', metavar='USERNAME', help='Only lock if created by this user')

    args = p.parse_args()

    now = datetime.utcnow()
    s = requests.session()
    if args.token:
        s.headers['Authorization'] = 'token ' + args.token

    params = {'state': 'closed', 'direction': 'asc', 'label': ','.join(args.label), 'assignee': args.assignee, 'creator': args.creator}
    params = {k:v for k,v in params.items() if v}

    issues = []
    next = 'https://api.github.com/repos/{}/{}/issues?per_page=100&{}'.format(args.owner, args.repo, parse.urlencode(params))
    while next:
        print('Fetching {} ...'.format(next))
        r = s.get(next)
        r.raise_for_status()
        next = r.links.get('next', {}).get('url')
        issues += r.json()

    to_lock = []
    for issue in issues:
        if 'pull_request' in issue:
            continue
        if args.updated_age and now - _parse_github_time(issue['updated_at']) < args.updated_age:
            continue
        if args.closed_age and now - _parse_github_time(issue['closed_at']) < args.closed_age:
            continue
        if args.created_age and now - _parse_github_time(issue['created_at']) < args.created_age:
            continue
        if issue['locked']:
            continue
        print ('Will lock issue #{} (created {}, updated {}, closed {} days ago; {})\n\t"{}"'.format(
            issue['number'],
            (now - _parse_github_time(issue['created_at'])).days,
            (now - _parse_github_time(issue['updated_at'])).days,
            (now - _parse_github_time(issue['closed_at'])).days,
            ('labels ' + ','.join(l['name'] for l in issue['labels'])) if issue['labels'] else 'unlabeled',
            issue['title'],
        ))
        to_lock.append((issue['number'], issue['title']))
    else:
        print('Found {} issues to lock.'.format(len(to_lock)))

    if args.do_it and args.token:
        for number, title in to_lock:
            print('Locking issue #{} ("{}")...'.format(number, title), end='')
            r = s.put('https://api.github.com/repos/{}/{}/issues/{}/lock?lock_reason={}'.format(
                args.owner, args.repo, number, parse.quote_plus(args.lock_reason)))
            r.raise_for_status()
            print(' LOCKED')
        else:
            print('Done. Locked {} issues.'.format(len(to_lock)))
    else:
        print('Dry run complete. Rerun with --token and --do-it to actually lock issues.')

if __name__=='__main__':
    main()
