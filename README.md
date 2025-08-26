
------------Steps for deploy on EC2 server---------------------------------

1- sudo apt-get update & upgrade

2 - sudo apt-get install vim python3 python3-pip python3-dev pkg-config libmysqlclient-dev nginx

3- git clone https://github.com/TheBabaYagaa/NatHabit_Twitter_Assignment.git
4- cd NatHabit_Twitter_Assignment

5- sudo apt install python3-venv 

6- create vitual env-
python3 -m venv venv

7- activate
source venv/bin/activate

cd backend 

8- pip install -r requirements.txt

9- python manage.py migrate
10- python manage.py runserver 0.0.0.0:8000

11- install GUNICORN(Inside venv)
   pip install gunicorn

12- gunicorn --bind 0.0.0.0:8000 core.wsgi:application --chdir backend

13- Deactivate virtual enviorment
    deactivate

14- Create a Gunicorn Socket
   sudo vi /etc/systemd/system/gunicorn.socket
----------------------------------------------
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

------------------
15- Create a gunicorn.service File:

sudo vi /etc/systemd/system/gunicorn.service

---------------------------------------------
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/NatHabit_Twitter_Assignment/backend
ExecStart=/home/ubuntu/NatHabit_Twitter_Assignment/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
-------------------------------------------------------------------
16- Start gunicorn enable gunicorn as a service(to start automatically along with operating system in case instance is restarted)

sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

17- Create a nginx configuration file 
sudo nano /etc/nginx/sites-available/nathabit.conf


server {
    listen 80;
    server_name 56.228.24.118;

   

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

18- Enable the configuration above to enable site by creating a symbolic link to configuration file
sudo ln -s /etc/nginx/sites-available/nathabit.conf /etc/nginx/sites-enabled/

19- Restart Nginx
sudo systemctl restart nginx


