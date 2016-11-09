#!/bin/sh
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/my_project.conf
sudo /etc/init.d/nginx restart
