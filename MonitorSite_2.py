# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:31:14 2016

@author: Brian D. Taylor
"""
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import json

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def check_last_modified(url, minutes):
    r = requests.get(url)
    dstring =  r.headers['Last-Modified']
    d0 = datetime.strptime(dstring, "%a, %d %b %Y %H:%M:%S %Z")
    tdelta = datetime.now()- d0
    if tdelta.total_seconds() < minutes*60:
        modified = True
    else:
        modified = False
    return modified
    

def get_site_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def is_internet_reachable():
    '''Checks Google then Yahoo just in case one is down'''
    if get_site_status('https://www.google.com') == 'down' and get_site_status('https://www.yahoo.com') == 'down':
        return False
    return True  
        
def parse_site(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml') 
    blog= soup.find('div', class_='main section')
    postdates = blog.find_all('div', class_='date-outer')
    d= {}
    datelist=[]
    for dposts in postdates:
        try:
            dates = dposts.find('h2', class_='date-header').text.strip()
            dt = datetime.strptime(dates, "%A, %B %d, %Y")
        except:
            dt =''
        titles = dposts.find_all('h3', class_='post-title entry-title')
        contents = dposts.find_all('div', class_='post-body entry-content')
        titles = [xx.text.strip() for xx in titles]
        contents = [xx.text.strip() for xx in contents]
        datelist.append({'date':dt, 'titles': titles, 'contents': contents} )
    d['posts']=datelist
    return d

def find_changes(url):
    print('no')

out = parse_site('http://blog.miahomeowners.com')
outb = parse_site('http://blog.miahomeowners.com')
out2 = parse_site('http://blog.miahomeowners.com/p/maintenance.html')
#

#Check to see if the Internet is broken
url1= 'http://blog.miahomeowners.com'
url2 = 'http://blog.miahomeowners.com/p/maintenance.html'

if is_internet_reachable():
    print('we has da internets')
    if get_site_status(url1):
        if check_last_modified(url1,60):
            data1 = parse_site(url1)
            find_changes(url1)
        else:
            print('no modifications')
    else:
        print('page not available')
        
    if get_site_status(url2):
        if check_last_modified(url2, 60):
             data2 = parse_site(url2)
             find_changes(url2)
        else:
            print('no modifications')
    else:
        print('page not available')
            



