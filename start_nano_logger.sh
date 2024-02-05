#!/bin/bash

# Set PATH to ensure all commands are found
PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin
# Path to your Django project directory
MQTT_PATH="/home/adminev/"

# Name of the tmux session
SESSION_NAME="logger"
# Name of the MQTT tmux session
MQTT_NAME="mqtt"

# Check if the tmux session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  # Create a new detached tmux session
  tmux new-session -d -s $SESSION_NAME -n main 'cd /home/adminev/logger && bash'
  
   
  tmux send-keys -t $SESSION_NAME "echo sb3of2jp3jd1 | sudo chmod a+rw /dev/ttyUSB0" C-m
  # Run  
  tmux send-keys -t $SESSION_NAME "python read-lite.py" C-m
fi

tmux has-session -t $MQTT_NAME 2>/dev/null
if [ $? != 0 ]; then
  tmux new-session -d -s $MQTT_NAME -n main 'cd /home/adminev/logger && bash'
  
  tmux send-keys -t $MQTT_NAME "python mqtt-ping.py" C-m
fi