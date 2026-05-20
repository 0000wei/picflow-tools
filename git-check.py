#!/usr/bin/env python3
import subprocess
r = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd='/home/wu/projects/image-tools')
print(r.stdout[:2000])
