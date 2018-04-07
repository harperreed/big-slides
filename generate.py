#!/usr/bin/env python
# encoding: utf-8

import logging
import markdown2
from optparse import OptionParser
import re
import sys
import os
import urllib2

from slugify import slugify

logging.basicConfig(format="%(message)s",level=logging.INFO)


def main():
    parser = OptionParser()
    parser.add_option("-a", "--action", dest="action",)

    parser.add_option( "--name",
        dest="name",
        help="presentation name")

    parser.add_option("--url",
        dest="url",
        help="URL of html presentation")



    parser.add_option( "--width",
        dest="width",
        help="width of rendered slide image",
        default='1920')

    parser.add_option("--height",
        dest="height",
        help="height of rendered slide image",
        default='1080')

    (options, args) = parser.parse_args()

    options.slug = slugify(unicode(options.name), separator="_")
    options.directory_name = options.slug + "-"+options.width+"x"+options.height
    options.exec_path = os.path.dirname(__file__)
    print options.exec_path


    if options.action == "generate-slides":
        logging.info("Generating slide images")

        logging.debug("Settings")
        logging.debug("\tName: "+options.name)
        logging.debug("\tSlug: "+options.slug)
        logging.debug("\tURL: "+options.url)
        logging.debug("\tDirectory: "+options.directory_name)
        logging.debug("\tImage dimensions: "+options.width + "x" + options.height)

        logging.info("Downloading " + options.url)
        logging.info("Saving images ")
        

        if not os.path.exists(options.directory_name):
            os.makedirs(options.directory_name)

        logging.info("Launching renderer")
        cmd = "node "+options.exec_path+"/big-renderer/renderer.js -f '" + options.url + "' --slideDir '"+options.directory_name+"' -w '"+options.width+"' -h '"+options.height+"' "
        
        os.system(cmd)
    elif options.action == "generate-pptx":
        print "pptx"
        #python /Users/harper/Dropbox/Documents/talks/bin/preso_gen.py -r ./ -s ./$(VAR)_-1920x1080/ --name $(VAR)

if __name__ == '__main__':
    main()
