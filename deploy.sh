#!/bin/bash
cd /home/wu/projects/image-tools
git add -A
git diff --cached --stat
echo "---"
git commit -m "Rebrand: PicFlow -> PicEte, picflow.tools -> picete.com"
echo "Exit code: $?"
echo "---"
git push
echo "Exit code: $?"
