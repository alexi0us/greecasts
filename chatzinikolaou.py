import os
import datetime
import sys
import common
import shutil
from glob import iglob
import logging



class chatzinikolaou_functions:
	cmn = common.common_functions()
	now = datetime.datetime.now()
	base_url = cmn.config_section_map("chatzinikolaou")['base_url']
	base_directory = cmn.config_section_map("home")['base_dir']
			
			

				
	def find_actual_download_url(self,html_lines):
		download_page = 'empty'
		for line in html_lines:
			if self.now.strftime("%d/%m/%Y") in line: #or "02/09/2013" in line:
				#logging.debug(line)
				logging.info('A podcast found for %s', self.now.strftime("%d-%m-%Y"))
				process_a = line.split('href=\"')
				for link in process_a:
					if link.startswith("DefaultArthro"):
						process_c = link.split('\">')
						download_page = process_c[0]
						podtitle = process_c[1][:-10].decode('utf-8')
		if download_page == 'empty':
			logging.info("No podcast found for: %s", self.now.strftime("%d/%m/%Y") )
			logging.info("Exiting")
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
				os.chmod(filename, 777)
				os.remove(filename)
			except OSError:
				pass

        def chatz_is_file_downloaded(self):
		flag = False
		complete_audio_file = "chatzinikolaou" + '_' + self.now.strftime("%d%m%Y")+'.mp3'
		rootdir = self.base_directory + "chatzinikolaou"
		for path, subFolders, files in os.walk(rootdir):
			for file in files:
				if file == complete_audio_file:
					logging.info('File with name %s already exists.', complete_audio_file)
					flag = True	
                return flag
