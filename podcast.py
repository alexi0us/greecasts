import urllib2
import datetime
from glob import iglob
import shutil
import sys
import os
import rss_gen
import ConfigParser

def config_section_map(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def ensure_directory_structure():
	if not os.path.exists('tmp'):
	    os.makedirs('tmp')
	if not os.path.exists('chatzinikolaou'):
		os.makedirs('chatzinikolaou')

def download_file(url,file_name):
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

def find_actual_download_url(html_lines):
	download_page = 'empty'
	for line in html_lines:
		if now.strftime("%d/%m/%Y") in line or "19/10/2012" in line:
			print now.strftime("%d-%m-%Y")
			# print "Found in : " +line
			process_a = line.split('href=\"')
			for link in process_a:
				if link.startswith("DefaultArthro"):
					process_c = link.split('\">')
					download_page = process_c[0]
					podtitle = process_c[1][:-10].decode('utf-8')
	if download_page == 'empty':
		print "No pod cast found for: "	+ now.strftime("%d/%m/%Y")
		print "Exiting..."
		sys.exit()
	else:			
		return base_url + download_page	

def get_html_and_split_lines(url):
	url_content = urllib2.urlopen(url)
	raw_html = url_content.read()
	html_lines = raw_html.split('\n')
	return html_lines
	
def download_all_available_files(html_download_lines):
	for line in html_download_lines:
		if "mp3" in line and "audiofile" in line:
			url_proc = line.split("\"")
			url = url_proc[3]
			filename = url_proc[0][:-11].decode('utf-8')
			filename = filename[11:].replace(' ', '') + ".mp3"
			download_file(url,filename)		

def concat_files_and_move(name):
	complete_audio_file = name + '_' + now.strftime("%d%m%Y")+'.mp3'
	path_complete_audio_file = os.getcwd() + '/'+ name +'/' + complete_audio_file
	destination = open(path_complete_audio_file , 'wb')
	for filename in iglob(os.path.join(os.getcwd() + '/tmp/', '*.mp3')):
		print filename
		shutil.copyfileobj(open(filename, 'rb'), destination)
	destination.close()
	shutil.copyfile(path_complete_audio_file , dropbox_dir + "audio/"+ complete_audio_file)

now = datetime.datetime.now()
config = ConfigParser.ConfigParser()
config.read("pod.conf")

base_url = config_section_map("chatzinikolaou")['base_url']
url_chatz = config_section_map("chatzinikolaou")['url_chatz']
dropbox_dir = config_section_map("chatzinikolaou")['dropbox_dir_chatz']

# base_url='http://www.real.gr/'
# url_chatz="http://www.real.gr/DefaultArthro.aspx?Page=category&catID=64"
# dropbox_dir = '/Users/koussou/Dropbox-pod/Dropbox/Apps/Pancake.io/greecast/chatzinikolaou/'	
	
ensure_directory_structure()
main_page_html = get_html_and_split_lines(url_chatz)
chatz_download_url = find_actual_download_url(main_page_html)
download_page_html = get_html_and_split_lines(chatz_download_url)
download_all_available_files(download_page_html)
concat_files_and_move("chatzinikolaou")
rssgen = rss_gen.RssGenerator()
rssgen.createxml()
