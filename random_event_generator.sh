#!/bin/bash

var1='docker-compose exec mids ab -n 1 -H "Host: ' 
var2='" http://localhost:5000/'
var3="purchase"
var4="create_guild"
var5="join_guild"
sl="/"
users=(user1@gmail.com user2@yahoo.com user3@hotmail.com user4@aol.com user5@comcast.com
       user6@att.com user7@tmobil.com user8@dell.com user9@tmb.com user10@xto.com)
weapons=(sword spear axe hammer)
chara=(light heavy large medium)
guild=(bandits warriors rangers knights farmers assesins spies spartans army sailors)
while true; do
	#Dummy1
	ru=$(($RANDOM%10))
	eval $var1${users[ru]}$var2
	#Dummy2
	ru=$(($RANDOM%10))
        eval $var1${users[ru]}$var2$var3
	#Dummy3
	ru=$(($RANDOM%10))
	rw=$(($RANDOM%4))
	eval $var1${users[ru]}$var2$var3$sl${weapons[rw]}
	#Purchase
	ru=$(($RANDOM%10))
	rw=$(($RANDOM%4))
	rc=$(($RANDOM%4))
	eval $var1${users[ru]}$var2$var3$sl${weapons[rw]}$sl${chara[rc]}
	#Dummy4
	ru=$(($RANDOM%10))
	eval $var1${users[ru]}$var2$var4
	#create
	ru=$(($RANDOM%10))
	rg=$(($RANDOM%10))
	eval $var1${users[ru]}$var2$var4$sl${guild[rg]}
	#Dummy5
	ru=$(($RANDOM%10))
	eval $var1${users[ru]}$var2$var5
	#create
	ru=$(($RANDOM%10))
	rg=$(($RANDOM%10))
	eval $var1${users[ru]}$var2$var5$sl${guild[rg]}

	sleep 10
done
