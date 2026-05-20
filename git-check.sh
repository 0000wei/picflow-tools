#!/bin/bash
echo "=== git status ==="
cd /home/wu/projects/image-tools && git status
echo ""
echo "=== files changed ==="
cd /home/wu/projects/image-tools && git diff --name-only
