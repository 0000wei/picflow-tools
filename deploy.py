#!/usr/bin/env python3
import subprocess, os, sys
basedir = '/home/wu/projects/image-tools'

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=basedir, **kw)
    return r

# 1. Status
r = run(['git', 'status', '--porcelain'])
sys.stdout.write(r.stdout)
sys.stdout.flush()

# 2. Add all
r = run(['git', 'add', '-A'])
print('staged')

# 3. Commit
r = run(['git', 'commit', '-m', 'Rebrand: PicFlow -> PicEte, picflow.tools -> picete.com'], check=False)
sys.stdout.write(r.stdout or '')
sys.stdout.write(r.stderr or '')
sys.stdout.flush()
if r.returncode != 0:
    print('Nothing to commit or error')
    sys.exit(0)

# 4. Push
r = run(['git', 'push'], check=False)
sys.stdout.write(r.stdout or '')
sys.stdout.write(r.stderr or '')
sys.stdout.flush()
print('DONE')
