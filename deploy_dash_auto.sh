#!/bin/bash
# =========================
# EC2 Dash Auto Deploy
# =========================

# VARIABLES
PROJECT_DIR=~/VAS_GROUP_DASH
VENV_DIR=$PROJECT_DIR/venv
SCREEN_NAME=dash_app
APP_FILE=index.py
GIT_BRANCH=main

echo "🔹 Starting auto-deploy for Dash app..."

# 1️⃣ Go to project directory
cd $PROJECT_DIR || { echo "❌ Project folder not found!"; exit 1; }

# 2️⃣ Pull latest code from Git
echo "🔹 Pulling latest code from Git..."
git reset --hard
git clean -fd
git fetch origin $GIT_BRANCH
git checkout $GIT_BRANCH
git pull origin $GIT_BRANCH

# 3️⃣ Stop old Gunicorn / screen session
echo "🔹 Stopping old Gunicorn and screen..."
screen -S $SCREEN_NAME -X quit 2>/dev/null || true
pkill gunicorn 2>/dev/null || true

# 4️⃣ Setup virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "🔹 Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

echo "🔹 Activating virtual environment..."
source $VENV_DIR/bin/activate

# 5️⃣ Upgrade pip
pip install --upgrade pip

# 6️⃣ Install dependencies
if [ -f "requirements.txt" ]; then
    echo "🔹 Installing/updating dependencies..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "🔹 Installing default dependencies..."
    pip install --no-cache-dir dash dash-bootstrap-components gunicorn pandas
fi

# 7️⃣ Test index.py for Gunicorn compatibility
if ! grep -q "server = app.server" $APP_FILE; then
    echo "❌ Error: 'server = app.server' missing in $APP_FILE"
    echo "Please add this line to expose app for Gunicorn."
    exit 1
fi

# 8️⃣ Start Gunicorn in detached screen
echo "🔹 Starting Gunicorn in detached screen..."
screen -S $SCREEN_NAME -dm bash -c "source $VENV_DIR/bin/activate && gunicorn $APP_FILE:server --bind 0.0.0.0:8050"

# 9️⃣ Done
echo "✅ Dash app deployed successfully!"
echo "👉 Access directly: http://<EC2_PUBLIC_IP>:8050"
echo "👉 App is running in screen session: $SCREEN_NAME"
