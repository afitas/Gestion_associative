#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $DIR/../../.venv/bin/activate
cd $DIR/../../EPLF/EPLF && $DIR/../../.venv/bin/gunicorn -c /home/ubuntu/Gestion_associative/EPLF/deploy/gunicorn.conf.py  -m 007 wsgi:application
