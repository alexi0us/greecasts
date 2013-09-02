# import libraries
import os
import sys
import datetime
import time
import shutil

dropbox_dir = '/Users/koussou/Dropbox-pod/Dropbox/Apps/Pancake.io/greecast/chatzinikolaou/'


# import constants from stat library
from stat import * # ST_SIZE ST_MTIME

class RssGenerator:

	# format date method
	def formatDate(self,dt):
	    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


	# get the item/@type based on file extension
	def getItemType(self,fileExtension):
	    if fileExtension == "aac":
	         mediaType = "audio/mpeg"
	    elif fileExtension == "mp4":
	         mediaType = "video/mpeg" 
	    else:
	         mediaType = "audio/mpeg" 
	    return mediaType


	def createxml(self):

		rssTitle = "Realfm - Nikos Chatzinikolaou"
		rssDescription = "OI kathimerines ekpompes tou Nikou Chatzinikolaou sto RealFm"
		# the url where the podcast items will be hosted
		rssSiteURL = "https://www.real.gr"
		# the url of the folder where the items will be stored
		rssItemURL = "http://ec2-54-217-81-147.eu-west-1.compute.amazonaws.com/chatzinikolaou"
		# the url to the podcast html file
		rssLink = rssSiteURL + "rss/chatzinikolaou.xml"
		# url to the podcast image
		rssImageUrl = "http://www.real.gr/files/New%20folder%20(1)/xatzinikolaou_button.jpg"
		# the time to live (in minutes)
		rssTtl = "60"
		# contact details of the web master
		rssWebMaster = "greecast@ymail"
		#record datetime started
		now = datetime.datetime.now()
		
		
		rootdir = "/home/ubuntu/greecasts/chatzinikolaou"
		
		outputFilename = "/home/ubuntu/greecasts/chatzinikolaou/chatzinikolaou.xml"
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
		outputFile.write("<image><url>" + rssImageUrl + "</url><title>" + rssTitle + "</title><link>" + rssLink + "</link></image>\n")
		outputFile.write("<copyright>mart 2012</copyright>\n")
		outputFile.write("<lastBuildDate>" + self.formatDate(now) + "</lastBuildDate>\n")
		outputFile.write("<pubDate>" + self.formatDate(now) + "</pubDate>\n")
		outputFile.write("<webMaster>" + rssWebMaster + "</webMaster>\n")


		# walk through all files and subfolders 
		for path, subFolders, files in os.walk(rootdir):
    
		    for file in files:
 
		        # split the file based on "." we use the first part as the title and the extension to work out the media type
		        fileNameBits = file.split(".")
			if fileNameBits[1] != "xml":
		            # get the full path of the file
		            fullPath = os.path.join(path, file)
		            # get the stats for the file
		            fileStat = os.stat(fullPath)
		            # find the path relative to the starting folder, e.g. /subFolder/file
		            relativePath = fullPath[len(rootdir):]


		            # write rss item
		            outputFile.write("<item>\n")
		            outputFile.write("<title>" + fileNameBits[0].replace("_", " ") + "</title>\n")
		            outputFile.write("<description>A description</description>\n")
		            outputFile.write("<link>" + rssItemURL + relativePath + "</link>\n")
		            outputFile.write("<guid>" + rssItemURL + relativePath + "</guid>\n")
		            outputFile.write("<pubDate>" + self.formatDate(datetime.datetime.fromtimestamp(fileStat[ST_MTIME])) + "</pubDate>\n")
		            outputFile.write("<enclosure url=\"" + rssItemURL + relativePath + "\" length=\"" + str(fileStat[ST_SIZE]) + "\" type=\"" + self.getItemType(fileNameBits[len(fileNameBits)-1]) + "\" />\n")
		            outputFile.write("</item>\n")


        
		# write rss footer
		outputFile.write("</channel>\n")
		outputFile.write("</rss>")
		outputFile.close()
		shutil.copyfile(outputFilename , "chatzinikolaou.xml")
		print "complete"


