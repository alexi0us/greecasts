"""
This class implements all common methods for downloading and handling the 
audio files.
"""
import os
import datetime
import shutil
import ConfigParser
import urllib2
import logging
import sys
from mutagen.mp3 import MP3
from glob import iglob


class common_functions:
    """
    Current time to use as a timpestamp fro podcasts
    """
    now = datetime.datetime.now()

    def get_html_and_split_lines(self, url):
        """
        Download the html code of a webpage and split it into lines
        """
        logging.debug('Downloading page and split html to separate lines')
        req = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0'\
        +' (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17'\
        +' (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"})
        logging.debug("Request header %s" + str(req.header_items()))
        logging.debug("Request url: %s" + str(req.get_full_url()))
        url_content = urllib2.urlopen(req)
        raw_html = url_content.read()
        html_lines = raw_html.split('\n')
        #logging.debug('html page lines:  %s', html_lines)
        return html_lines

    def config_section_map(self, section):
        """
        Returns a dictionary of the given config map value
        """
        config = ConfigParser.ConfigParser()
        config.read("pod.conf")
        options = config.options(section)
        dict1 = {}
        for option in options:
            try:
                dict1[option] = config.get(section, option)
                if dict1[option] == -1:
                    logging.debug("skip: %s" % option)
            except:
                logging.error("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def download_file(self, url, program, file_name):
        """
        Downloads the file and store it locally
        """
        u = urllib2.urlopen(url)
        f = open(os.getcwd() + '/' + program + '/tmp/' + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logging.info('Start downloading %s', file_name)
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            bufferv = u.read(block_sz)
            if not bufferv:
                break
            file_size_dl += len(bufferv)
            f.write(bufferv)
            status = r"%10d  [%3.2f%%]" % (file_size_dl,\
                                            file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
            print status,
        f.close()
        logging.info('Download completed for %s', file_name)
        return True

    def ensure_directory_structure(self, name):
        """
        Making sure that the directory structure for storing the
        podcasts is correct.
        """
        logging.info('Checking directory structure for %s', name)
        if not os.path.exists(name + '/tmp'):
            os.makedirs(name + '/tmp')
        logging.info('Directory structure checked for %s', name)

    def download_all_available_files(self, html_download_lines, program):
        """
        Extract the available mp3 files and call download_file function for
        each one of them
        """
        for line in html_download_lines:
            if "mp3" in line and "audiofile" in line:
                url_proc = line.split("\"")
                url = url_proc[3]
                #loggging.debbug(url_proc)
                filename = url_proc[0][:-11].decode('utf-8')
                filename = filename[11:].replace(' ', '') + ".mp3"
                self.download_file(url, program, filename)

    def concat_files_and_move(self, name):
        """
        Concatenate the downloaded files and move the result file in the
        correct location
        """
        complete_audio_file = name + '_' + self.now.strftime("%d%m%Y") + '.mp3'
        path_complete_audio_file = os.getcwd() + '/' + name \
        + '/' + complete_audio_file
        logging.info('Scanning tmp folder for available files')
        destination = open(path_complete_audio_file, 'wb')
        for filename in sorted(iglob(os.path.join(os.getcwd()\
            + '/' + name + '/tmp/', '*.mp3'))):
            file_concat = filename.split("/")
            logging.info('Concatenating file %s', file_concat[-1])
            shutil.copyfileobj(open(filename, 'rb'), destination)
        destination.close()
        #Remove tmp files
        for filename in sorted(iglob(os.path.join(os.getcwd() \
                                            + '/' + name + '/tmp/', '*.mp3'))):
            try:
                logging.info('Removing tmp file %s', filename)
                os.chmod(filename, 777)
                os.remove(filename)
            except OSError:
                pass

    def get_podcast_duration(self, fileName):
        logging.debug("Calculating mp3 duration for %s", fileName)
        audio = MP3(fileName)
        duration = datetime.timedelta(seconds = audio.info.length)
        audio_length = ':'.join(str(duration).split(':')[:2])
        if audio_length:
            return audio_length
        else:
            logging.error("Something went wrong. Podcast has duration 0")
            logging.info("Exiting")
            sys.exit()