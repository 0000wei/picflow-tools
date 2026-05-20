import subprocess, os
os.chdir('/home/wu/projects/image-tools')
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Rebrand: PicFlow -> PicEte, picflow.tools -> picete.com'], check=True)
subprocess.run(['git', 'push'], check=True)
print('DONE')
