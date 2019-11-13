#!/bin/bash

set -e
export LC_ALL=en_US.UTF-8
if [ $# -ne 8 ];then
	echo "Usage: $0 <uwsgi-port> <grpc-long-host> <grpc-long-port> <grpc-medium-host> <grpc-medium-port> <grpc-short-host> <grpc-short-port> <num-workers>";
	exit 1;
fi

port=$1
grpc_long_host=$2
grpc_long_port=$3
grpc_medium_host=$4
grpc_medium_port=$5
grpc_short_host=$6
grpc_short_port=$7
workers=$8

sed -i "s/short_host.*/short_host = ${grpc_short_host}/g" ./config/my.conf
sed -i "s/short_port.*/short_port = ${grpc_short_port}/g" ./config/my.conf
sed -i "s/medium_host.*/medium_host = ${grpc_medium_host}/g" ./config/my.conf
sed -i "s/medium_port.*/medium_port = ${grpc_medium_port}/g" ./config/my.conf
sed -i "s/long_host.*/long_host = ${grpc_long_host}/g" ./config/my.conf
sed -i "s/long_port.*/long_port = ${grpc_long_port}/g" ./config/my.conf
sed -i "s/bind.*/bind = '0.0.0.0:${port}'/g" ./config/gunicorn.py
sed -i "s/workers.*/workers = ${workers}/g" ./config/gunicorn.py


source ./pypath.sh

# start log agent from entry command
/etc/init.d/scribeagent3 start

gunicorn -c ./config/gunicorn.py server:server

