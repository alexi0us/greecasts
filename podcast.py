#!/usr/bin/env python

import rss_gen
import common
import chatzinikolaou
import logging
import ellinofreneia


def main():
    logging.basicConfig(filename = 'podcast.log', \
                        format = '%(asctime)s %(message)s', level = logging.INFO)

    cmn = common.common_functions()
    chatz = chatzinikolaou.chatzinikolaou_functions()
    url_chatz = cmn.config_section_map("chatzinikolaou")['url']

    if chatz.chatz_is_file_downloaded() == False:
        cmn.ensure_directory_structure('chatzinikolaou')
        main_page_html = cmn.get_html_and_split_lines(url_chatz)
        chatz_download_url = chatz.find_actual_download_url(main_page_html)
        download_page_html = cmn.get_html_and_split_lines(chatz_download_url)
        cmn.download_all_available_files(download_page_html, 'chatzinikolaou')
        cmn.concat_files_and_move("chatzinikolaou")
        rssgen = rss_gen.RssGenerator()
        rssgen.createxml("chatzinikolaou")
        logging.info("New chatzinikolaou episode file found and podcast updated")
    else:
        logging.info("Exiting")

    ellin = ellinofreneia.ellinofreneia_functions()
    ellin_chatz = cmn.config_section_map("ellinofreneia")['url']

    if ellin.ellin_is_file_downloaded() == False:
        cmn.ensure_directory_structure('ellinofreneia')
        main_page_html = cmn.get_html_and_split_lines(ellin_chatz)
        ellin_download_url = ellin.find_actual_download_url(main_page_html)
        download_page_ellin_html = cmn.get_html_and_split_lines(ellin_download_url)
        cmn.download_all_available_files(download_page_ellin_html, 'ellinofreneia')
        cmn.concat_files_and_move("ellinofreneia")
        rssgen = rss_gen.RssGenerator()
        rssgen.createxml("ellinofreneia")
        logging.info("New ellinofreneia episode file found and podcast updated")
    else:
        logging.info("Exiting")

if __name__ == '__main__':
    main()
