#!/bin/bash

for PID in `ps -ef | grep phi_start | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done

for PID in `ps -ef | grep etl_start | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done

for PID in `ps -ef | grep trh_start | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done

for PID in `ps -ef | grep chromedriver | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done

for PID in `ps -ef | grep chromium-browse | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done
