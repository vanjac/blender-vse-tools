#!/bin/sh
# Args: path/to/video path/to/audio output_name

ffmpeg -i $1 -i $2 -c:v copy -c:a aac -strict experimental $3.mp4