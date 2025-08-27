#!/bin/bash

set -e

echo "Starting Django deployment..."

PROJECT_DIR="/home/ubuntu/NatHabit_Twitter_Assignment"
cd $PROJECT_DIR


if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
# Activate virtualenv
source venv/bin/activate


# Install dependencies
cd backend/
# Load environment variables from .env
cp .env.example .env && sed -i "s/DEBUG=1/DEBUG=0/" .env
echo "Loading environment variables..."
export $(grep -v '^#' .env | xargs)
pip install --upgrade pip
pip install -r requirements.txt

# Django maintenance
python manage.py migrate
python manage.py collectstatic --noinput

# Restart Gunicorn only if changes were pulled
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

# Restart Nginx (optional)
sudo systemctl restart nginx

echo "Deployment complete!"
