#!/bin/sh
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/my_project.conf
sudo ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/hello.conf
sudo ln -s /home/box/web/etc/qa.conf /etc/gunicorn.d/qa.conf
sudo /etc/init.d/gunicorn restart
sudo /etc/init.d/nginx restart
