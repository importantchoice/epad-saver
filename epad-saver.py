#!/usr/bin/python3

"""
    This script downloads the content of etherpads.

    Padfile layout definition:
    "^TITLE\s <BASEURL>$"
"""

import argparse # Parse CLI arguments
import re # extract pad title from baseurl
from requests import get # download pad content
from datetime import datetime # get timestamp for filename
import os # get filenames for duplicity check

# Default messages for new documents; Used to detect empty pads
welcomeMessages = [ 
                    "WELCOME TO RISEUP'S ETHERPAD!" # Riseup
                  ]

def getEntryTitle(entry):
    """Extracts pad title from padfile"""
    result = re.search('^(.*)\s+<.*>\s*', entry)
    if result:
        return result.group(1)
    else:
        raise Exception("Unable to extract pad title from padfile")


def getEntryURL(entry):
    """Extracts pad url from padfile"""
    result = re.search('^.*<(.*)>\s*', entry)
    if result:
        return result.group(1)
    else:
        raise Exception("Unable to extract pad url from padfile")


def getTitleFromBaseUrl(baseurl):
    """Extracts the pad title from a given baseurl"""

    result = re.search('http[s]*://.*/(.*)/*', baseurl)
    if result:
        return result.group(1)
    else:
        raise Exception("Unable to extract pad title from baseurl")

def getFileName(workingdir, title):
    """Generates the file name for a downloaded pad dump"""
    # build timestamp which is appended to the file to avoid overwriting an existing dump
    dt = datetime.now()
    timestamp = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) + "-" + str(dt.hour) + "-" + str(dt.minute) + "-" + str(dt.second)
    # return filename
    return workingdir + "/" + title + "-" + timestamp + ".txt"

def baseURLcleanup(baseurl):
    """Cleans up the baseurl from unwanted features"""
    return baseurl.rstrip("/")

def contentIsEmpty(content, welcomeMessages):
    """Check if the downloaded pad is empty"""
    content = content.decode('utf-8')

    if content == "":
        return True
    for message in welcomeMessages:
        if content.startswith(message):
            return True

def contentChanged(content, workingdir):
    """Check if downloaded content has changed"""
    for filename in os.listdir(workingdir):
        existingFile = open(workingdir + "/" + filename)
        if content.decode('utf-8') == existingFile.read():
            return False
    return True

# Parse cli arguments
parser = argparse.ArgumentParser(description='Save your Etherpads')
parser.add_argument('-b', '--baseurl', dest='baseurl', help='BaseURL of the pad you like to save')
parser.add_argument('-t', '--title', dest='title', help='Title of the pad')
parser.add_argument('-f', '--padfile', dest='padfile', help='Path to a file containing a list of etherpads')
parser.add_argument('-w', '--workingdir', dest='workingdir', default=".", help='Path to the directory the pad(s) are saved into; Default: .')
parser.add_argument('-s', '--no-duplicate-check', dest='duplicateCheck', action='store_false', help="turn off the duplicate check")
# Sample file generation not implemented yet
# parser.add_argument('-g', '--generate-padfile', dest='genPadFile', help='Generate sample pad file to given destination')
args = parser.parse_args()

workingdir = os.path.abspath(args.workingdir)
duplicateCheck = args.duplicateCheck

# Get urls and titles to download
urls = []

# Get url and title which might be provided
if args.baseurl:
    baseurl = baseURLcleanup(args.baseurl)

    if args.title:
        title = args.title
    else:
        title = getTitleFromBaseUrl(baseurl)
    urls.append([baseurl, title])

if args.padfile:
    with open(args.padfile) as f:
            padfileContent = f.readlines()
            for entry in padfileContent:
                title = getEntryTitle(entry)
                baseurl = getEntryURL(entry)

                # cleanup baseurl
                baseurl = baseURLcleanup(baseurl)

                urls.append( [ baseurl, title ] )

# Download urls
for url, title in urls:
    print("Working on " + url)
    # expand url to get the txt version
    url = url + "/export/txt"
    content = get(url).content

    # check if downloaded pad is empty
    if contentIsEmpty(content, welcomeMessages):
        print("  Empty pad detected! Skipping...")
        continue

    # check if content has not changed
    if duplicateCheck and not contentChanged(content, workingdir):
        print("  Content has not changed! Skipping...")
        continue

    # save downloaded content
    filename = getFileName(workingdir, title)
    with open(filename, "wb") as saveFile:
        saveFile.write(content)
