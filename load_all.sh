#!/bin/bash
# Load all types of source files
#./etl_start.py --mode=load --type=ipg
#./etl_start.py --mode=load --type=ipa
#./etl_start.py --mode=load --type=ad
#./etl_start.py --mode=load --type=att
#./etl_start.py --mode=load --type=fee
/usr/bin/python etl_start.py --mode=load --type=td
#./kill_proc.sh


