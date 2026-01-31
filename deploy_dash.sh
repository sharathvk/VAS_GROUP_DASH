#!/bin/bash
# ----------------------------
# FULL AUTOMATED DASH DEPLOYMENT
# ----------------------------

# Variables
PROJECT_DIR=~/VAS_GROUP_DASH
APP_FILE=index.py
SCREEN_NAME=dash_app

# 1️⃣ Navigate to project
cd $PROJECT_DIR || { echo "Project folder not found"; exit 1; }

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Upgrade pip
pip install --upgrade pip

# 4️⃣ Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install dash dash-bootstrap-components gunicorn pandas
fi

# 5️⃣ Update index.py for external access (host=0.0.0.0) and production server
if ! grep -q "host=\"0.0.0.0\"" $APP_FILE; then
    echo "Updating $APP_FILE for host 0.0.0.0..."
    sed -i '/if __name__ == "__main__":/a \    app.run(host="0.0.0.0", port=8050)' $APP_FILE
fi

if ! grep -q "server = app.server" $APP_FILE; then
    echo "Adding server = app.server..."
    sed -i '1i server = app.server' $APP_FILE
fi

# 6️⃣ Install screen to run app in background
sudo yum install screen -y   # Ubuntu: sudo apt-get install screen -y

# 7️⃣ Start Dash app using Gunicorn in detached screen
screen -S $SCREEN_NAME -dm bash -c "source venv/bin/activate && gunicorn index:server --bind 0.0.0.0:8050"

# 8️⃣ Install Nginx
sudo yum install nginx -y     # Ubuntu: sudo apt-get install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx

# 9️⃣ Configure Nginx as reverse proxy
sudo tee /etc/nginx/conf.d/dash.conf > /dev/null <<EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8050;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOL

# 10️⃣ Restart Nginx
sudo nginx -t
sudo systemctl restart nginx

# ✅ Done
echo "✅ Dash app deployed!"
echo "Access it at: http://<EC2_PUBLIC_IP> (via Nginx)"
echo "or http://<EC2_PUBLIC_IP>:8050 (direct Gunicorn)"
echo "App is running in background via screen session: $SCREEN_NAME"
