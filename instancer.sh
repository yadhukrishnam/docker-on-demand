#!/bin/bash
cd ./instancer
python3 ./instancer/app.py > log.txt 2>&1 &
echo "Frontend spawned"
cd ./backend/server
python3 ./backend/server/app.py > log.txt  2>&1 &
echo "Backend spawned"
# script to run both docker-on-demand and instancer