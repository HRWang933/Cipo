#!/bin/bash

for PID in `ps -ef | grep trh_scraper | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done

for PID in `ps -ef | grep chromium | awk '{print $2}'`
do
    echo $PID
    kill -9 $PID
done
