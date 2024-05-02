#!/bin/bash

source_dir=/home/savvycom/odoo-docker/odoo-addons-dev
container_name=odoo17-dev

cd $source_dir && git reset --hard HEAD && git pull --rebase 

echo "Upgrade code successful"

sudo docker restart $container_name

echo "reload successful"
