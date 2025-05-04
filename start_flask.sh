#!/bin/bash
cd /home/<user>/medical_upload
source .venv/bin/activate
tmux new-session -d -s flask_app "python upload_server.py"
