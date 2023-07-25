#!/bin/bash
# Parse all types of source files
# Load parsed files into Impala tables
#./etl_start.py --mode=parse --type=ipg
#./etl_start.py --mode=parse --type=ipa
#./etl_start.py --mode=parse --type=ad
#./etl_start.py --mode=parse --type=att
#./etl_start.py --mode=parse --type=fee
/usr/bin/python etl_start.py --mode=parse --type=td
#./kill_proc.sh
