heroku
git push heroku main
heroku run python manage.py migrate

# Offline enabler
sudo timedatectl set-timezone Africa/Nairobi

apt install libaio1 numactl
apt install openjdk-8-jdk openjdk-8-jre
cat >> /etc/environment <<EOL
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
JRE_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
EOL
source /etc/environment
dpkg-reconfigure dash
  <No>

sudo su

heroku run bash

BACKUP DOWNLOAD from Heroku
heroku pg:backups:capture
heroku pg:backups:download

insertion to local postgres [first create the db in local]
postgres@douglas:~$ pg_restore -d bdoprime -v -h localhost -p 5432 -U ssekuwanda '/home/douglas/Documents/DOUGLAS/CODE/bdoprime/latest.dump'

git config --global user.name "imrancs058" 
git config --global user.email "imrancs058@yahoo.com"
git reset --hard HEAD
git pull

chris@server# ssh-keygen -t rsa -b 4096 -C "joe@example.com"
chris@server# cat .ssh/id_rsa.pub

sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
sudo nginx -t && sudo systemctl restart nginx

libpangocairo-1.0-0 in requirements.txt

# Generating public/privatekeys
cd ~/.ssh
ssh-keygen
cat id_rsa.pub | xclip