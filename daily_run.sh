#! /bin/bash
while true
do
	hour=$(date +"%H")
	minute=$(date +"%M")
	if [ $hour -eq 0 ] && [ $minute -eq 0 ]; then
		python3 update_daily_records.py >update_log.txt 2>update_log.txt	
	fi
	sleep 60
done