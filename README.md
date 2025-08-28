
#  Local Setup Guide (Django + MySQL)
Follow these steps to run the project locally:
## 1. Clone the Repository
git clone https://github.com/TheBabaYagaa/NatHabit_Twitter_Assignment.git
cd NatHabit_Twitter_Assignment
## 2. Create Virtual Environment
# Create venv
python3 -m venv venv
# Activate venv
# (Linux/Mac)
source venv/bin/activate
# (Windows - Git Bash/PowerShell)
venv\Scripts\activate
## 3. Setup Environment Variables
cd backend
## 4. Install Dependencies
pip install -r requirements.txt
cp .env.example .env
nano .env # Edit database credentials and other settings
Make sure `.env` contains correct DB settings (MySQL or SQLite).
## 5. Apply Database Migrations
python manage.py migrate
## install and run terraform
 
 cd infra/terraform
 zip function.zip lambda_function.py
 terraform init
 terraform apply
## 6. Create Superuser (Admin Login)
python manage.py createsuperuser
## 7. Run the Development Server
python manage.py runserver
The app will now be available at:
n http://127.0.0.1:8000/
n That’s it! You can now develop and test the app locally.


#  Deploying Django App on AWS EC2 (Gunicorn + Nginx)
Follow these steps to deploy the project on an **Ubuntu EC2 instance**:
## 1. Update & Upgrade Packages
sudo apt-get update && sudo apt-get upgrade -y
## 2. Install Required Packages
sudo apt-get install vim python3 python3-pip python3-dev pkg-config libmysqlclient-dev nginx -y
## 3. Clone the Project
git clone https://github.com/TheBabaYagaa/NatHabit_Twitter_Assignment.git
cd NatHabit_Twitter_Assignment
## 4. Create & Activate Virtual Environment
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
## 5. Setup Environment Variables
cd backend
cp .env.example .env
sed -i "s/DEBUG=1/DEBUG=0/" .env
nano .env # (edit values as needed)
## 6. Install Python Dependencies
pip install -r requirements.txt
## 7. Run Database Migrations
python manage.py migrate
## 8. Test the Server
python manage.py runserver 0.0.0.0:8000
## 9. Install Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 core.wsgi:application --chdir backend
Deactivate the virtual environment:
deactivate
## 10. Configure Gunicorn with systemd
### Create **gunicorn.socket**
sudo vi /etc/systemd/system/gunicorn.socket
Paste:
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.sock
[Install]
WantedBy=sockets.target
### Create **gunicorn.service**
sudo vi /etc/systemd/system/gunicorn.service
Paste:
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/NatHabit_Twitter_Assignment/backend
EnvironmentFile=/home/ubuntu/NatHabit_Twitter_Assignment/backend/.env
ExecStart=/home/ubuntu/NatHabit_Twitter_Assignment/venv/bin/gunicorn core.wsgi:application
--workers 3 --access-logfile - --bind fd://0
Restart=always
[Install]
WantedBy=multi-user.target
### Enable & Start Gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
## 11. Configure Nginx
### Create Nginx Config File
sudo nano /etc/nginx/sites-available/nathabit.conf
Paste:
server {
listen 80;
server_name 56.228.24.118;
location / {
include proxy_params;
proxy_pass http://unix:/run/gunicorn.sock;
}
}
### Enable the Site
sudo ln -s /etc/nginx/sites-available/nathabit.conf /etc/nginx/sites-enabled/
### Restart Nginx
sudo systemctl restart nginx
n Your Django app should now be live on your EC2 instance!