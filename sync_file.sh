#!/bin/bash
rm -f sub sub2
curl -s https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub -o sub
curl -s https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub -o sub2
curl -s https://raw.githubusercontent.com/mytv-android/China-TV-Live-M3U8/refs/heads/main/iptv.m3u -o iptv.m3u
curl -s https://raw.githubusercontent.com/ckmah74/iptv/refs/heads/main/IPTV2025 -o iptv_2025.m3u
curl -s https://github.com/ghokun/tv/blob/main/bin/playlist.m3u -o tv.m3u
git add sub sub2 iptv.m3u iptv_2025.m3u tv.m3u
git diff --quiet && git diff --staged --quiet || (git commit -m "Update file from GitHub [$(date +%Y-%m-%d)]" && git push)
