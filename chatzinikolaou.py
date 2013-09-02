import os
import datetime
import sys
import common
import shutil
from glob import iglob



class chatzinikolaou_functions:
	cmn = common.common_functions()
	now = datetime.datetime.now()
	base_url = cmn.config_section_map("chatzinikolaou")['base_url']
	
	
	def ensure_directory_structure(self):
		if not os.path.exists('tmp'):
		    os.makedirs('tmp')
		if not os.path.exists('chatzinikolaou'):
			os.makedirs('chatzinikolaou')
			
			
	def download_all_available_files(self,html_download_lines):
		for line in html_download_lines:
			if "mp3" in line and "audiofile" in line:
				url_proc = line.split("\"")
				url = url_proc[3]
				#print url_proc
				filename = url_proc[0][:-11].decode('utf-8')
				filename = filename[11:].replace(' ', '') + ".mp3"
				self.cmn.download_file(url,filename)
				
	def find_actual_download_url(self,html_lines):
		download_page = 'empty'
		for line in html_lines:
			if self.now.strftime("%d/%m/%Y") in line or "02/09/2012" in line:
				print self.now.strftime("%d-%m-%Y")
				# print "Found in : " +line
				process_a = line.split('href=\"')
				for link in process_a:
					if link.startswith("DefaultArthro"):
						process_c = link.split('\">')
						download_page = process_c[0]
						podtitle = process_c[1][:-10].decode('utf-8')
		if download_page == 'empty':
			print "No podcast found for: "	+ self.now.strftime("%d/%m/%Y")
			print "Exiting..."
			sys.exit()
		else:			
			return self.base_url + download_page
			
			
	def concat_files_and_move(self,name):
		complete_audio_file = name + '_' + self.now.strftime("%d%m%Y")+'.mp3'
		path_complete_audio_file = os.getcwd() + '/'+ name +'/' + complete_audio_file
		destination = open(path_complete_audio_file , 'wb')
		for filename in sorted(iglob(os.path.join(os.getcwd() + '/tmp/', '*.mp3'))):
			file_concat = filename.split("/")
			print file_concat[-1]
			shutil.copyfileobj(open(filename, 'rb'), destination)
		destination.close()
		#Remove tmp files
		for filename in sorted(iglob(os.path.join(os.getcwd() + '/tmp/', '*.mp3'))):
			try:
				os.remove(filename)
			except OSError:
				pass

