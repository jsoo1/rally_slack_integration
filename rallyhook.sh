#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

case "$1" in
    build)
        # conf file check
        if [[ ! -f "$DIR"/.rallyhook.json ]]; then
            printf "Setup the app with a .rallyhook.json file\n"
            exit 1
        fi

        # virtualenv
        if [[ ! -d "$DIR"/venv/bin ]]; then
            mkdir "$DIR"/venv
            virtualenv "$DIR"/venv
        fi
        source "$DIR"/venv/bin/activate
        pip install pyral flask slacker gunicorn
        deactivate

        # TODO get a domain name so we can get real certs?
        if [[ ! -f "$DIR"/rallyhook.pem ]] || [[ ! -f "$DIR"/cert.pem ]]; then
            openssl req \
                    -x509 \
                    -newkey rsa:4096 \
                    -keyout rallyhook.pem \
                    -out cert.pem \
                    -days 365
            openssl rsa -in rallyhook.pem -out rallyhook.pem
            printf "Created certs\n"
        fi

        # log files
        if [[ ! -d "$DIR"/.log ]]; then
            logfile="$DIR"/.log
            mkdir "$logfile"
            touch \
                "$logfile"/error.log \
                "$logfile"/access.log
        fi

        printf "Ready... ??\n";;

    start)
        "$DIR"/venv/bin/gunicorn \
              --daemon \
              --bind 0.0.0.0:5050 \
              --certfile "$DIR"/cert.pem \
              --keyfile "$DIR"/rallyhook.pem \
              --access-logfile "$DIR"/.log/access.log \
              --error-logfile "$DIR"/.log/error.log \
              --pid "$DIR"/.pid \
              rallyhook:app;;

    restart)
        pid=$(cat "$DIR"/.pid)
        kill -HUP "$pid"
        printf "Restarted rallyhook, pid: %s\n" "$pid"

esac
