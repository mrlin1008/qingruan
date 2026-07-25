#!/bin/bash
cd /Users/mrlin/Desktop/qingruan/changting_hunan_platform_v2
/usr/local/bin/python3 daily_bidding_update.py >> daily_update.log 2>&1
echo "" >> daily_update.log
