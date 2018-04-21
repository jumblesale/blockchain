#!/usr/bin/env bash

python $1 &
python_pid=$!

ssh -fNT -R 80:localhost:8080 -p 2222 ssh.localhost.run
ssh_pid=$!

function ctrl_c() {
    echo "exiting..."
    echo ${python_pid}
    echo ${ssh_pid}
    kill ${python_pid} ${ssh_pid}
}

trap ctrl_c SIGINT

tail -f logs/log.log
