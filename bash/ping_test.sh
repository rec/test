#!/bin/bash

YOUR_ISP=8.8.8.8

while :
do
  ping  -t 2 -o -c 1 $YOUR_ISP || say no ping
  sleep 1
done
