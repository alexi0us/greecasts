import rss_gen
import ConfigParser
import common
import chatzinikolaou
import logging

logging.basicConfig(filename='podcast.log', format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)

cmn = common.common_functions()
chatz = chatzinikolaou.chatzinikolaou_functions()
# mega = megatv.megatv_functions()

url_chatz = cmn.config_section_map("chatzinikolaou")['url_chatz']

if chatz.chatz_is_file_downloaded() == False:
	chatz.ensure_directory_structure()
	main_page_html = cmn.get_html_and_split_lines(url_chatz)
	chatz_download_url = chatz.find_actual_download_url(main_page_html)
	download_page_html = cmn.get_html_and_split_lines(chatz_download_url)
	chatz.download_all_available_files(download_page_html)
	chatz.concat_files_and_move("chatzinikolaou")
	rssgen = rss_gen.RssGenerator()
	rssgen.createxml("chatzinikolaou")
	logging.info("New episode file found and podcast updated")
else:
	logging.info("File already exist")

# url_download_mega = "http://www.megatv.com/megagegonota/summary.asp?catid=27377&subid=2&pubid=29981910"
# mega_download_page_html = cmn.get_html_and_split_lines(url_download_mega)
# mega.download_mp4_file(mega_download_page_html)
