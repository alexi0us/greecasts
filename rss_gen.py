# -*- coding: utf-8 -*-
import os
import common
import datetime
import logging
from stat import  ST_SIZE, ST_MTIME


class RssGenerator:
    now = datetime.datetime.now()
    cmn = common.common_functions()
    base_directory = cmn.config_section_map("home")['base_dir']

    def __init__(self):
        self.cmn = common.common_functions()

    def formatDate(self, dt):
        """
        Returns the date in correct format for podcast
        """
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # get the item/@type based on file extension
    def getItemType(self, fileExtension):
        """
        Returns the media type of the podcast.
        Support for multiple podcast formats e.g. video, audio
        """
        if fileExtension == "aac":
            mediaType = "audio/mpeg"
        elif fileExtension == "mp4":
            mediaType = "video/mpeg"
        else:
            mediaType = "audio/mpeg"
            return mediaType

    def createxml(self, name):
        """
        Function for generating the xml podcast file
        """
        xml_dict = self.cmn.config_section_map(name)

        rssTitle = xml_dict['rss_title']

        rssDescription = xml_dict['rss_description']
        rssSiteURL = xml_dict['base_url']
        rssItemURL = xml_dict['podcast_dir_url']
        rssLink = rssSiteURL + xml_dict['podcast_location']
        rssImageUrl = xml_dict['image_url']
        rssTtl = "60"
        rssWebMaster = "greecast@ymail.com"
        now = datetime.datetime.now()
        rootdir = self.base_directory + name
        outputFilename = self.base_directory + xml_dict['xml_file']
        episode_title = xml_dict['episode_title']
        episode_desc = xml_dict['episode_desc']

        print "Updating : " + outputFilename

        # open rss file
        outputFile = open(outputFilename, "w")

        # write rss header
        outputFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        outputFile.write("<rss version=\"2.0\">\n")
        outputFile.write("<channel>\n")
        outputFile.write("<title>" + rssTitle + "</title>\n")
        outputFile.write("<description>" + rssDescription + "</description>\n")
        outputFile.write("<link>" + rssLink + "</link>\n")
        outputFile.write("<ttl>" + rssTtl + "</ttl>\n")
        outputFile.write("<image><url>" + rssImageUrl + "</url><title>"\
                          + rssTitle + "</title><link>" \
                          + rssLink + "</link></image>\n")
        outputFile.write("<copyright>mart 2012</copyright>\n")
        outputFile.write("<lastBuildDate>" + self.formatDate(now) \
                         + "</lastBuildDate>\n")
        outputFile.write("<pubDate>" + self.formatDate(now) + "</pubDate>\n")
        outputFile.write("<webMaster>" + rssWebMaster + "</webMaster>\n")

        for fileName in os.listdir(self.base_directory + name):
            logging.debug("fileName: " + fileName)
            fileNameBits = fileName.split(".")
            logging.debug(fileNameBits)
            if len(fileNameBits) == 2:
                if fileNameBits[1] != "xml":
                    logging.info("Creating xml entry for: %s", fileNameBits[0])
                    path = os.path.join(os.getcwd() + '/' + name)
                    fullPath = os.path.join(path, fileName)
                    logging.debug("fullpath is: %s", fullPath)
                    # get the stats for the file
                    fileStat = os.stat(fullPath)
                    # find the path relative to the starting folder, e.g. /subFolder/file
                    relativePath = fullPath[len(rootdir):]
                    audio_length = self.cmn.get_podcast_duration(fullPath)
                    logging.info("Duration for %s is %s", \
                                  fileName, audio_length)

                    # write rss item
                    outputFile.write("<item>\n")
                    outputFile.write("<title>" + fileNameBits[0][15:17] \
                        + "/" + fileNameBits[0][17:19]\
                        + "/" + fileNameBits[0][21:23]
                        + " " + episode_title + "</title>\n")
                    outputFile.write("<description>" + episode_desc\
                                      + "</description>\n")
                    outputFile.write("<link>" + rssItemURL + relativePath\
                                      + "</link>\n")
                    outputFile.write("<guid>" + rssItemURL + relativePath\
                                      + "</guid>\n")
                    outputFile.write("<pubDate>"\
                        + self.formatDate(\
                        datetime.datetime.fromtimestamp(fileStat[ST_MTIME]))\
                                      + "</pubDate>\n")
                    outputFile.write("<duration>" + audio_length\
                                      + "</duration>\n")
                    outputFile.write("<enclosure url=\"" + rssItemURL\
                                      + relativePath + "\" length=\""\
                                      + str(fileStat[ST_SIZE]) + "\" type=\""\
                                      + self.getItemType(\
                                       fileNameBits[len(fileNameBits) - 1])\
                                      + "\" />\n")
                    outputFile.write("</item>\n")

        outputFile.write("</channel>\n")
        outputFile.write("</rss>")
        outputFile.close()
        print "Operation completed"
        logging.info("Podacast xml updated.")
