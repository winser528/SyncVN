#!/bin/bash
rm -f sub sub2
curl -s https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub -o sub
curl -s https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub -o sub2
git add sub sub2
git diff --quiet && git diff --staged --quiet || (git commit -m "Update file from GitHub [$(date +%Y-%m-%d)]" && git push)
