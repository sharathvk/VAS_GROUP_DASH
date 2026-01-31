#!/bin/bash
# =========================
# EC2 DASH FULL CLEAN + DEPLOY
# =========================

# -----------------------------
# VARIABLES
# -----------------------------
PROJECT_DIR=~/VAS_GROUP_DASH
VENV_DIR=$PROJECT_DIR/venv
SCREEN_NAME=dash_app
APP_FILE=index.py
GIT_BRANCH=main

echo "🔹 Starting full clean + deploy for Dash app..."

# -----------------------------
# 1️⃣ Go to project directory
# -----------------------------
cd $PROJECT_DIR || { echo "❌ Project folder not found!"; exit 1; }

# -----------------------------
# 2️⃣ Stop old Gunicorn / screen
# -----------------------------
echo "🔹 Stopping old Gunicorn and screen sessions..."
screen -S $SCREEN_NAME -X quit 2>/dev/null || true
pkill gunicorn 2>/dev/null || true

# -----------------------------
# 3️⃣ Clear Python & pip caches
# -----------------------------
echo "🔹 Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "🔹 Clearing pip cache..."
pip3 cache purge

# -----------------------------
# 4️⃣ Remove old virtual environment
# -----------------------------
echo "🔹 Removing old virtual environment..."
rm -rf $VENV_DIR

# -----------------------------
# 5️⃣ Create new virtual environment
# -----------------------------
echo "🔹 Creating new virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Upgrade pip
echo "🔹 Upgrading pip..."
python -m ensurepip --upgrade
pip install --upgrade pip

# -----------------------------
# 6️⃣ Pull latest code from Git
# -----------------------------
echo "🔹 Pulling latest code from Git..."
git reset --hard
git clean -fd
git fetch origin $GIT_BRANCH
git checkout $GIT_BRANCH
git pull origin $GIT_BRANCH

# -----------------------------
# 7️⃣ Install dependencies
# -----------------------------
if [ -f "requirements.txt" ]; then
    echo "🔹 Installing/updating dependencies from requirements.txt..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "🔹 Installing default dependencies..."
    pip install --no-cache-dir dash dash-bootstrap-components gunicorn pandas
fi

# -----------------------------
# 8️⃣ Check index.py for Gunicorn
# -----------------------------
if ! grep -q "server = app.server" $APP_FILE; then
    echo "❌ ERROR: 'server = app.server' missing in $APP_FILE!"
    echo "Please add this line to expose app for Gunicorn."
    exit 1
fi

# -----------------------------
# 9️⃣ Start Gunicorn in detached screen
# -----------------------------
echo "🔹 Starting Gunicorn in detached screen session..."
screen -S $SCREEN_NAME -dm bash -c "source $VENV_DIR/bin/activate && gunicorn $APP_FILE:server --bind 0.0.0.0:8050"

# -----------------------------
# 10️⃣ Optional: restart Nginx
# -----------------------------
if [ -f /etc/nginx/nginx.conf ]; then
    echo "🔹 Restarting Nginx..."
    sudo nginx -t
    sudo systemctl restart nginx
fi

# -----------------------------
# ✅ Done
# -----------------------------
echo "✅ Dash app deployed successfully!"
echo "👉 Direct access: http://<EC2_PUBLIC_IP>:8050"
echo "👉 Screen session: $SCREEN_NAME"
echo "👉 Nginx reverse proxy: http://<EC2_PUBLIC_IP> (if configured)"
