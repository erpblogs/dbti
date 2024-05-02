#!/bin/bash

# Set default values if no arguments provided

module_name="${1:-custom_hr}"
db_name="${2:-dbti_dev}"
container_name="odoo17-dev"

# Execute the Docker command
sudo docker exec -it "$container_name" /bin/bash -c "odoo -c /etc/odoo/odoo.conf --http-port=9999 -d $db_name -u $module_name --stop-after-init"

echo "Upgrade successful"

sudo docker restart $container_name

echo "reload successful"