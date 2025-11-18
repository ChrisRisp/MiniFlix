#!/usr/bin/env bash
set -uo pipefail   # no `-e` so we can handle ffmpeg errors ourselves

RTMP_INPUT="${RTMP_INPUT:-rtmp://rtmp/live/stream}"
HLS_OUT="${HLS_OUT:-/var/media/hls}"

echo ">>> RTMP_INPUT: $RTMP_INPUT"
echo ">>> HLS_OUT:    $HLS_OUT"

mkdir -p "$HLS_OUT"

while true; do
  echo ">>> Cleaning old HLS outputs..."
  # Remove old segments/playlists; ignore errors if nothing exists
  rm -f "$HLS_OUT"/*.ts "$HLS_OUT"/*.m3u8 2>/dev/null || true

  echo ">>> Starting ffmpeg at $(date)"

  ffmpeg -loglevel info -y \
  -fflags +genpts \
  -i "$RTMP_INPUT" \
  -c:v libx264 -preset veryfast -tune zerolatency -b:v 2500k \
  -c:a aac -b:a 128k \
  -f hls \
  -hls_time 1 \
  -hls_list_size 3 \
  -hls_flags delete_segments+append_list+independent_segments \
  -start_number 0 \
  -reset_timestamps 1 \
  -hls_segment_filename "$HLS_OUT/rtmp_%04d.ts" \
  "$HLS_OUT/rtmp.m3u8"

  rc=$?
  echo ">>> ffmpeg exited with code $rc, sleeping 2s and restarting..."
  sleep 2
done
