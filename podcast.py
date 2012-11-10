from glob import iglob
import shutil
import rss_gen
import ConfigParser
import common
import chatzinikolaou

cmn = common.common_functions()
chatz = chatzinikolaou.chatzinikolaou_functions()


base_url = cmn.config_section_map("chatzinikolaou")['base_url']
url_chatz = cmn.config_section_map("chatzinikolaou")['url_chatz']
dropbox_dir = cmn.config_section_map("chatzinikolaou")['dropbox_dir_chatz']

	
chatz.ensure_directory_structure()
main_page_html = cmn.get_html_and_split_lines(url_chatz)
chatz_download_url = chatz.find_actual_download_url(main_page_html)
download_page_html = cmn.get_html_and_split_lines(chatz_download_url)
chatz.download_all_available_files(download_page_html)
chatz.concat_files_and_move("chatzinikolaou")
rssgen = rss_gen.RssGenerator()
rssgen.createxml()
