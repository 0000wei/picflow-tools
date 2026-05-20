import subprocess, sys, os
cwd = '/home/wu/projects/image-tools'
# Preview changes
r = subprocess.run(['git', 'status', '--porcelain'], cwd=cwd, capture_output=True, text=True)
print('Changes:', r.stdout)

# Add all
subprocess.run(['git', 'add', '-A'], cwd=cwd, check=True)
print('staged')

# Commit
r = subprocess.run(['git', 'commit', '-m', 'Rebrand: PicFlow -> PicEte, picflow.tools -> picete.com'], cwd=cwd, capture_output=True, text=True)
print(r.stdout)
if r.returncode != 0:
    print('nothing to commit')
    sys.exit(0)

# Push
r = subprocess.run(['git', 'push'], cwd=cwd, capture_output=True, text=True)
print(r.stdout)
sys.stdout.flush()
sys.stderr.flush()
print('DONE')
