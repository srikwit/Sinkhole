import json
import requests
import urllib3
import time
import datetime

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}

urls=["https://adaway.org/hosts.txt",\
        "https://hosts-file.net/ad_servers.txt",\
        "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext",\
        "http://winhelp2002.mvps.org/hosts.txt",\
        "http://sysctl.org/cameleon/hosts",\
        "http://someonewhocares.org/hosts/hosts",\
        "http://www.malwaredomainlist.com/hostslist/hosts.txt",\
        "http://securemecca.com/Downloads/hosts.txt",\
        "https://sites.google.com/site/logroid/files/hosts.txt",\
        "https://raw.githubusercontent.com/eladkarako/hosts.eladkarako.com/master/_raw__hosts.txt",\
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",\
        "https://raw.githubusercontent.com/yous/YousList/master/hosts.txt"]

def domain_fetcher():
    with open("unsanitized_hosts.txt","a+") as unsanitized_hosts:
        for host in urls:
            try:
                response = requests.get(host,headers,verify=False)
                if response.status_code == 200:
                    unsanitized_hosts.write(response.text)
            except Exception as e:
                print("Couldn't connect to "+host)


def domain_sanitizer():
    unique_domains = set()
    with open("unsanitized_hosts.txt","r+") as unsanitized_hosts:
        for entry in unsanitized_hosts:
            non_empty_entry = entry.rstrip("\r\n")
            if len(non_empty_entry) == 0:
                continue
            else:
                #Remove comments
                if non_empty_entry.startswith("#"):
                    continue
                else:
                    if non_empty_entry.startswith("127.0.0.1") or non_empty_entry.startswith("0.0.0.0"):
                        unique_domains.add(non_empty_entry.split()[1])
                    else:
                        unique_domains.add(non_empty_entry)
    wrong_domains = set(['0.0.0.0','127.0.0.1'])
    for domain in wrong_domains:
        if domain in unique_domains:
            unique_domains.remove(domain)
    with open("sanitized_hosts.txt","a+") as sanitized_hosts:
        for domain in unique_domains:
            sanitized_hosts.write(domain+"\r\n")

def generate_hosts_file_contents():
    with open("hosts.txt","a+") as hosts:
        with open("sanitized_hosts.txt","r+") as sanitized_hosts:
            for host in sanitized_hosts:
                hosts.write("127.0.0.1 "+host)

domain_fetcher()
domain_sanitizer()
generate_hosts_file_contents()
