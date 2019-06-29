#!/bin/bash

# Filename of the movie
MOVIE=/home/pi/a-movie.mov

# Options to omxplayer
OPTIONS=

echo "Starting to play $MOVIE"
omxplayer $OPTIONS $MOVIE
