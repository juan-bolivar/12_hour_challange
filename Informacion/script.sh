#!/bin/bash



date_1=$(date --date=$1 +'%s')
date_2=$(date --date=$2 +'%s')

curl -o $3 https://finance.yahoo.com/quote/BTC-USD/history?period1=$date_1&period2=$date_2&interval=1d&filter=history&frequency=1d
