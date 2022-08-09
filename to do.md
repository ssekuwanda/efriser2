heroku
git push heroku master
heroku run python manage.py migrate

BACKUP DOWNLOAD from Heroku
heroku pg:backups:capture
heroku pg:backups:download

insertion to local postgres [first create the db in local]
postgres@douglas:~$ pg_restore -d bdoprime -v -h localhost -p 5432 -U ssekuwanda '/home/douglas/Documents/DOUGLAS/CODE/bdoprime/latest.dump' 