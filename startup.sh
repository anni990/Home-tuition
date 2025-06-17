#!/bin/bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - 
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list 
apt-get update 
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev
cd /home/site/wwwroot
pip install -r requirements.txt
gunicorn --bind=0.0.0.0 --timeout 600 run:app