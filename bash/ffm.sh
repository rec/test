find . \
     -name '*S01E01*.mp4' \
     -print \
     -exec sh -c 'i="{}"; ffmpeg -i "$i" -c:v h264_videotoolbox -b:v "${i}".mkv' \;
