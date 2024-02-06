#! /bin/bash
while true
do
	hour=$(date +"%H")
	minute=$(date +"%M")
	if [ $hour -eq 17 ] && [ $minute -eq 43 ]; then
		python3 lambda_function.py >log.txt 2>error.txt	
	fi
	sleep 60
done
