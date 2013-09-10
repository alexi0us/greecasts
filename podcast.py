#!/usr/bin/env python

import rss_gen
import ConfigParser
import common
import chatzinikolaou
import logging


def main():
	logging.basicConfig(filename='podcast.log', format='%(asctime)s %(message)s',  level=logging.INFO)

	cmn = common.common_functions()
	chatz = chatzinikolaou.chatzinikolaou_functions()

	url_chatz = cmn.config_section_map("chatzinikolaou")['url_chatz']

	if chatz.chatz_is_file_downloaded() == False:
		cmn.ensure_directory_structure('chatzinikolaou')
		main_page_html = cmn.get_html_and_split_lines(url_chatz)
		chatz_download_url = chatz.find_actual_download_url(main_page_html)
		download_page_html = cmn.get_html_and_split_lines(chatz_download_url)
		cmn.download_all_available_files(download_page_html,'chatzinikolaou')
		cmn.concat_files_and_move("chatzinikolaou")
		rssgen = rss_gen.RssGenerator()
		rssgen.createxml("chatzinikolaou")
		logging.info("New episode file found and podcast updated")
	else:
		logging.info("Exiting")

# url_download_mega = "http://www.megatv.com/megagegonota/summary.asp?catid=27377&subid=2&pubid=29981910"
# mega_download_page_html = cmn.get_html_and_split_lines(url_download_mega)
# mega.download_mp4_file(mega_download_page_html)

if __name__ == '__main__':
    main()
