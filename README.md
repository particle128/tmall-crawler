Tmall goods Crawler
===

## Introduction
The crawler is used to grab information of goods in [www.tmall.com](http://www.tmall.com)

## Requirements
```
sudo pip install beautifulsoup
sudo pip install requests
```

## Configuration
fields in config.txt:    
* max: the maximum number of goods you would like to grab. 
Because of tmall's restriction, the upper bound is 6000. If you want to get more goods information, modify the source code a little bit.  
* keyword: the keyword of goods
Only one keyword is supported for the moment.  

## Usage
```
python main.py
```
The results will be saved in `record[mmddhhMMss].txt` in the current directory 
