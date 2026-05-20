#!/usr/bin/env python3
"""Git status check"""
import subprocess, os
os.chdir('/home/wu/projects/image-tools')
# Check git status
r = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
print("Unstaged/modified files:")
print(r.stdout if r.stdout else "(none)")
if r.stderr:
    print("STDERR:", r.stderr[:500])
print("---")
# Check diff
r = subprocess.run(['git', 'diff', '--stat'], capture_output=True, text=True)
print("Diff stat (unstaged):")
print(r.stdout if r.stdout else "(none)")
print("---")
# Check staged
r = subprocess.run(['git', 'diff', '--cached', '--stat'], capture_output=True, text=True)
print("Staged changes:")
print(r.stdout if r.stdout else "(none)")
