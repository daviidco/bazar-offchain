#!/bin/bash

set -a
source .flaskenv
set +a

# Start Gunicorn
echo Starting Gunicorn.
gunicorn -w 4 -b 0.0.0.0:5000 application:application &

# Start Nginx
echo Starting Nginx.
nginx -g "daemon off;"
