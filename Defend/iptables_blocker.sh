#!/bin/bash
while read line
do
	iptables -A INPUT -s $line -j DROP
done < sanitized_online_ips
