#!/usr/bin/env python3
"""Recompute every number in STUDY.md from the three CSV files in ../data.

Standard library only. Usage:  python3 scripts/summarize.py
License: MIT (see LICENSE-CODE).
"""
import collections
import csv
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def load(name):
    with open(os.path.join(DATA, name), newline='') as f:
        return list(csv.DictReader(f))


def uploads():
    rows = [r for r in load('uploads.csv') if r['deviation_pct'] and r['repeat_of_earlier_upload'] == 'no']
    devs = [float(r['deviation_pct']) for r in rows]
    small = [d for d in devs if abs(d) < 5]
    print('1. Predicted score vs leaderboard score')
    print(f'   distinct uploads with a written prediction: {len(devs)}')
    print(f'   within 0.01%: {sum(abs(d) < 0.01 for d in small)} of {len(small)} (excluding 1 task-level gap of {min(devs):+.1f}%)')
    print(f'   above prediction: {sum(d >= 0.01 for d in small)}, below: {sum(d <= -0.01 for d in small)}, '
          f'worst: {min(small):+.2f}%, mean: {sum(small) / len(small):+.3f}%')


def bets():
    rows = load('bets.csv')
    scored = [r for r in rows if r['agent_error'] and r['human_error']]
    a = [float(r['agent_error']) for r in scored]
    h = [float(r['human_error']) for r in scored]
    print('\n2. Pre-registered bets (error = prediction - actual; lower is better, so negative = too optimistic)')
    print(f'   scored: {len(scored)} (not scored: {len(rows) - len(scored)})')
    print(f'   agent too optimistic: {sum(x < -0.01 for x in a)}, too pessimistic: {sum(x > 0.01 for x in a)}')
    print(f'   agent closer than the human: {sum(abs(x) < abs(y) for x, y in zip(a, h))} of {len(scored)}')
    more_pess = [(x, y) for x, y in zip(a, h) if y > x]
    print(f'   human more pessimistic than the agent: {len(more_pess)} times, human closer in '
          f'{sum(abs(y) < abs(x) for x, y in more_pess)} of them')
    calls = [r for r in scored if r['agent_called']]
    print(f'   pass/fail calls: {len(calls)}, correct: {sum(r["agent_called"] == r["outcome"] for r in calls)}, '
          f'wrong: {[r["id"] + " called " + r["agent_called"] for r in calls if r["agent_called"] != r["outcome"]]}')


def corrections():
    rows = load('corrected_claims.csv')
    print('\n3. Claims later corrected by an exact check')
    d = collections.Counter(r['direction'] for r in rows)
    print(f'   total: {len(rows)}; overclaims: {d["over"]}, underclaims (premature kills): {d["under"]}')
    print(f'   {"evidence class":16s} {"over":>5s} {"under":>6s}')
    for c in ('proxy', 'model', 'early-run', 'judgement', 'probe', 'exact-verifier', 'outside'):
        o = sum(r['evidence_class'] == c and r['direction'] == 'over' for r in rows)
        u = sum(r['evidence_class'] == c and r['direction'] == 'under' for r in rows)
        print(f'   {c:16s} {o:5d} {u:6d}')
    fast = sum(r['direction'] == 'over' and r['evidence_class'] in ('proxy', 'model', 'early-run') for r in rows)
    print(f'   overclaims resting on a proxy, a model estimate or an early lead: {fast} of {d["over"]}')
    print(f'   corrected by the same thread that made the claim: {sum(r["self_corrected_by_same_thread"].startswith("yes") for r in rows)}')


if __name__ == '__main__':
    uploads()
    bets()
    corrections()
