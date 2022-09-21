heroku
git push heroku master
heroku run python manage.py migrate

BACKUP DOWNLOAD from Heroku
heroku pg:backups:capture
heroku pg:backups:download

insertion to local postgres [first create the db in local]
postgres@douglas:~$ pg_restore -d bdoprime -v -h localhost -p 5432 -U ssekuwanda '/home/douglas/Documents/DOUGLAS/CODE/bdoprime/latest.dump'

git reset --hard HEAD
git pull

chris@server# ssh-keygen -t rsa -b 4096 -C "joe@example.com"
chris@server# cat .ssh/id_rsa.pub

sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
sudo nginx -t && sudo systemctl restart nginx

libpangocairo-1.0-0 in requirements.txt