ffmpeg -re -f lavfi -i "testsrc=size=1920x1080:rate=30" \
       -f lavfi -i "sine=frequency=1000" \
       -c:v libx264 -preset veryfast -g 60 -c:a aac -ar 44100 -b:a 128k \
       -f flv rtmp://localhost/live/in
