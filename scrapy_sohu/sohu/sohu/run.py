#from scrapy import cmdline
#cmdline.execute(['scrapy','crawl','sohu'])
import time
import os


while True:
    os.system("scrapy crawl sohu")
    time.sleep(300)
