#!/bin/bash

# Set PATH to ensure all commands are found
PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin
# Path to your Django project directory
MQTT_PATH="/home/tonyho/"

# Name of the tmux session
SESSION_NAME="logger"
PANEL_NAME="panel"
SAVE_NAME="save_to_redis"
SAVE_USB="save_to_usb"
# Check if the tmux session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
  # Create a new detached tmux session
  tmux new-session -d -s  $SESSION_NAME -n main 'cd /home/tonyho/panel && bash'
  
  # Activate virtual environment and start Django server
  tmux send-keys -t $SESSION_NAME "source .venv/bin/activate" C-m
  tmux send-keys -t $SESSION_NAME "cd logger" C-m
  tmux send-keys -t $SESSION_NAME "python read-lite-local.py" C-m
fi

tmux has-session -t $PANEL_NAME 2>/dev/null
if [ $? != 0 ]; then
  # Create a new detached tmux session for panel
  tmux new-session -d -s $PANEL_NAME -n main 'cd /home/tonyho/panel && bash'
  
  # Activate virtual environment and start Django server
  tmux send-keys -t $PANEL_NAME "source .venv/bin/activate" C-m
  tmux send-keys -t $PANEL_NAME "cd panel" C-m
  tmux send-keys -t $PANEL_NAME "python manage.py runserver 0.0.0.0:8000" C-m
fi

tmux has-session -t $SAVE_NAME 2>/dev/null
if [ $? != 0 ]; then
  # Create a new detached tmux session for panel
  tmux new-session -d -s $SAVE_NAME -n main 'cd /home/tonyho/panel && bash'
  
  # Activate virtual environment and start Django server
  tmux send-keys -t $SAVE_NAME "source .venv/bin/activate" C-m
  tmux send-keys -t $SAVE_NAME "cd logger" C-m
  tmux send-keys -t $SAVE_NAME "python saveredis.py" C-m
fi

tmux has-session -t $SAVE_USB 2>/dev/null
if [ $? != 0 ]; then
  # Create a new detached tmux session for panel
  tmux new-session -d -s $SAVE_USB -n main 'cd /home/tonyho/panel && bash'
  
  # Activate virtual environment and start Django server
  tmux send-keys -t $SAVE_USB "source .venv/bin/activate" C-m
  tmux send-keys -t $SAVE_USB "cd logger" C-m
  tmux send-keys -t $SAVE_USB "echo 'zanik5dbkr' | sudo -S python checkusb.py" C-m
 
fi