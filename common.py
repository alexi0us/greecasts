import os
import sys
import datetime
import time
import shutil
import ConfigParser
import urllib2



class common_functions:
	
	def get_html_and_split_lines(self,url):
		req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"}) 
		url_content = urllib2.urlopen(req)
		raw_html = url_content.read()
		html_lines = raw_html.split('\n')
		return html_lines
	
	def config_section_map(self,section):
		config = ConfigParser.ConfigParser()
		config.read("pod.conf")
		options = config.options(section)
		dict1 = {}
		for option in options:
			try:
				dict1[option] = config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1
	
	def download_file(self,url,file_name):
		u = urllib2.urlopen(url)
		f = open(os.getcwd() + '/tmp/'+file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_name, file_size)
		file_size_dl = 0
		block_sz = 8192
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break
		    file_size_dl += len(buffer)
		    f.write(buffer)
		    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		    status = status + chr(8)*(len(status)+1)
		    print status,
		f.close()
		return True	