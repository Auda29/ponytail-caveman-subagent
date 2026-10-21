"""Check the specific three-line read acknowledgement used in this evaluation.

This is an offline evaluator, not host enforcement or proof that files were read.
"""
import argparse
from pathlib import Path
import re
import subprocess


def check(text, expected_count):
    errors = []
    lines = text.strip().splitlines()
    if len(lines) > 3:
        errors.append('response exceeds the three-line task limit')
    fields = {}
    for line in lines:
        key, separator, value = line.partition(':')
        if not separator or key not in ('Status', 'Result', 'Evidence/checks'):
            errors.append('unexpected line or field')
            continue
        if key in fields:
            errors.append('duplicate field: ' + key)
        fields[key] = value.strip()
    for key in ('Status', 'Result', 'Evidence/checks'):
        if not fields.get(key):
            errors.append('missing or empty field: ' + key)
    if 'Status' in fields and fields['Status'] not in ('done', 'partial', 'blocked'):
        errors.append('invalid status')
    counts = re.findall(r'(?:^|[\s;])files_read=([^\s;]+)', fields.get('Evidence/checks', ''))
    if len(counts) != 1:
        errors.append('expected one files_read count')
    elif not re.fullmatch(r'[0-9]+', counts[0]):
        errors.append('files_read must be a nonnegative integer')
    elif int(counts[0]) != expected_count:
        errors.append(f'files_read={counts[0]}, expected {expected_count}')
    return errors


def tracked_count(repository):
    paths = subprocess.check_output(['git', '-C', str(repository), 'ls-files', '-z'])
    return len([path for path in paths.split(b'\0') if path])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path, help='Frozen repository used for the read task')
    parser.add_argument('handoff', type=Path)
    args = parser.parse_args()
    count = tracked_count(args.repository)
    errors = check(args.handoff.read_text(encoding='utf-8'), count)
    print('\n'.join(errors) if errors else f'PASS: format, line limit, files_read={count}')
    raise SystemExit(bool(errors))
