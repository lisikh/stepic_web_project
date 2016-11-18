#!/bin/sh
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/my_project.conf
sudo ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/hello.conf
sudo ln -s /home/box/web/etc/qa.conf /etc/gunicorn.d/qa.conf
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/nginx restart
sudo /etc/init.d/mysql restart
mysql -uroot -e "create database qa"
mysql -uroot -e "create user 'sa' identified by 'qa'"
mysql -uroot -e "grant all on qa.* to 'sa'"
/home/box/web/ask/manage.py syncdb
