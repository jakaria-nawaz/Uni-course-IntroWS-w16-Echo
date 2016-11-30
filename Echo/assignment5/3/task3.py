# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 00:40:12 2016

"""

import socket
from urllib.parse import urlparse
import os
import sys
import re
import numpy
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
import time

global totalLinks #list - for per page
global totalWebpages #list - for per page
global internalLinks #list - for per page
global externalLinks #list - for per page
global allInternalLinks #list - for links in the file
#global internalLinksIndex
#global timeout

def main():
    global totalLinks
    global totalWebpages
    global internalLinks
    global externalLinks
    totalLinks = []
    totalWebpages = []
    internalLinks = []
    externalLinks = []
    #urlRaw = input('Please enter the URL : \n')
    #duration = input('Please enter running time : \n')

    #globals


    #step 0 - first run init : create file (a) to save all internal links found in all pages and (ii) to save all visited links

    #with open('allVisitedLinks.txt', 'wb') as allVisitedFile:
    #    allVisitedFile.write("".encode())

    #step 1 : get target url and get its content ----------------------

    targetFirstUrl = input('Please enter the URL : \n')

    #URL has to be filtered by urlparse
    #urlParsed = urlparse(targetFirstUrl)
    #print (urlParsed)

    internalLinksIndex = 0
    firstTime = 1
    with open('allInternalLinks.txt', 'a') as allLinkFile:
        allLinkFile.write(targetFirstUrl)
    timeout = time.time() + 60*.10   # 1 minutes from now
    traverse_loop(internalLinksIndex, timeout, firstTime)
# foin = open('allInternalLinks.txt', encoding="utf8")
# fileContentIn = foin.read()
# foin.close()
# allInternalLinks = fileContentIn.split(',')
# print("\n\n All the link in the file: \n\n")
# print(allInternalLinks)
# print("\n\n The last link in the file: \n\n")
# print(allInternalLinks[-1])
# print("\n\n")
def traverse_loop(internalLinksIndex,timeout,firstTime):
    while True:
        if time.time() > timeout:
        #if test == 5 or time.time() > timeout:
            # print("Total Links List: "+totalLinks+"\n")
            # print("Total Webpages List: "+totalWebpages+"\n")
            # print("Total Internal Links List: "+internalLinks+"\n")
            # print("Total External Links List: "+externalLinks+"\n")
            break
        else:
            foin = open('allInternalLinks.txt', encoding="utf8")
            fileContentIn = foin.read()
            foin.close()
            allInternalLinks = fileContentIn.split(',')
            targetUrl = allInternalLinks[internalLinksIndex]

            #internalLinksIndex = internalLinksIndex+1

            #break
            urlParsed = urlparse(targetUrl)
            traverse_site(targetUrl, urlParsed, internalLinksIndex, timeout, firstTime)

def traverse_site(targetUrl, urlParsed, internalLinksIndex, timeout, firstTime):
    global totalLinks
    global totalWebpages
    global internalLinks
    global externalLinks
    #check if the url is already in the allVisitedLinks file. if not continue
    fo = open('allVisitedLinks.txt', encoding="utf8")
    fileContent = fo.read()
    fo.close()
    #print(file)
    r=fileContent.find(targetUrl)
    #print(fileContent)
    #print(r)
    if r == -1:
        #continue
        #print('inside if: new site found')

        #Getting IP from Parsed URL
        myIp = socket.gethostbyname(urlParsed.netloc)

        #Initializing Socket
        mySoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Connecting to Server using IP
        mySoc.connect((myIp,80))

        #Send HTTP GET request to server
        getRequest="GET / HTTP/1.0\n\n"
        # formating this request string in bytes SOCK_STREAM
        getFormatted=getRequest.encode()

        myGet=bytes(getRequest, 'utf-8')

        mySoc.send(myGet)

        # firstDataPart contains data from http header - Comment by Nawaz
        # firstDataPart contains the page header - Comment by Romio
        firstDataPart = mySoc.recv(100)
        firstDataPart=firstDataPart.decode('utf-8')
        #checking if the site is alive and ok -if not ok halt
        foundResult = firstDataPart.find('OK')

        allData=bytes("", 'utf-8')
        dataBuffer = None

        if foundResult != -1:
            print('site connected '+targetUrl+": ")
            with open('allVisitedLinks.txt', 'a') as allVisitedFile:
                if firstTime == 1:
                    allVisitedFile.write(targetUrl)
                    firstTime = 0
                else:
                    allVisitedFile.write(","+targetUrl)
                    firstTime = 0
            while dataBuffer!=bytes("", 'utf-8'):
                dataBuffer = mySoc.recv(100000)
                allData +=dataBuffer

            decodedData=allData.decode('utf-8')

            allData = firstDataPart+decodedData
            #allDataPlain = allData.decode('utf-8')
            #encodedData=bytes(allData, 'utf-8')
            #writing the html file to disk
            # with open('index.html', 'wb') as downloadedFile:
            #     downloadedFile.write(allData.encode())
            #     print("end done")

            theExternal = re.findall(r'(http[^"]+)', str(allData)) #external links
            allLinks = re.findall(r'<a href="([^"]+)".*?>', str(allData)) #including internal and external links
            theInternal = [x for x in allLinks if x not in theExternal] #only internal links to traverse

            linklist = re.findall(r'<link.*? href="([^"]+)".*?>', str(allData))
            stylelist = re.findall(r'@import "([^"]+)";', str(allData))
            scriptlist = re.findall(r'<script .*? src="([^"]+)".*?>', str(allData))

            # totalLinks.append(len(allLinks)+len(linklist)+len(stylelist)+len(scriptlist))
            # totalWebpages.append(len(allLinks))
            # internalLinks.append(len(theInternal))
            # externalLinks.append(len(theExternal))
            #print(theExternal)
            #print("\n")
            # print(totalWebpages)
            # print("\n")
            # print(internalLinks)
            # print("\n")
            # print(externalLinks)
            # print("\n")

            for p in theInternal:
                #print(p)
                with open('allInternalLinks.txt', 'a') as allLinkFile:
                    allLinkFile.write(","+"http://141.26.208.82/"+p)

            internalLinksIndex = internalLinksIndex+1
            traverse_loop(internalLinksIndex,timeout,firstTime)

        else:
            #print("Somthing wrong!")
            internalLinksIndex = internalLinksIndex+1
            traverse_loop(internalLinksIndex,timeout,firstTime)
        #print(type(allData))

    else:
        internalLinksIndex = internalLinksIndex+1
        traverse_loop(internalLinksIndex,timeout, firstTime)

        #step 3 : start on next link from the allInternalLinks file    ----------------------
        # (i) check target line number on visited text file from global split counter

if __name__ == '__main__':
    main()
