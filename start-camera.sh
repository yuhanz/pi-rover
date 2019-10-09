cd ~/jsmpeg && node websocket-relay.js supersecret 8081 8082 > /tmp/relay.txt &
cd ~/jsmpeg && http-server > /tmp/camera.txt &
ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -f mpegts -codec:v mpeg1video -s 640x480 -b:v 1000k -bf 0 http://localhost:8081/supersecret > /tmp/video.txt &
