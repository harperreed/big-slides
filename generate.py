#!/usr/bin/env python3

import logging
import os
import subprocess
import argparse
from slugify import slugify

logging.basicConfig(format="%(message)s", level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", dest="action", help="Action to be taken (generate-html, generate-slides, generate-pptx)")
    parser.add_argument("--name", dest="name", help="Presentation name")
    parser.add_argument("--url", dest="url", help="URL of html presentation")
    parser.add_argument("--width", dest="width", help="Width of rendered slide image", default='1920')
    parser.add_argument("--height", dest="height", help="Height of rendered slide image", default='1080')

    args = parser.parse_args()

    args.slug = slugify(args.name, separator="_")
    args.directory_name = f"{args.slug}-{args.width}x{args.height}"
    args.exec_path = os.path.dirname(__file__)

    if args.action == "generate-html":
        logging.info("Generating HTML")
        cmd = f"python3 {args.exec_path}/bigpy/big.py -s {args.name}.md"
        subprocess.run(cmd, shell=True)

    elif args.action == "generate-slides":
        logging.info("Generating slide images")
        logging.debug("Settings")
        logging.debug(f"\tName: {args.name}")
        logging.debug(f"\tSlug: {args.slug}")
        logging.debug(f"\tURL: {args.url}")
        logging.debug(f"\tDirectory: {args.directory_name}")
        logging.debug(f"\tImage dimensions: {args.width}x{args.height}")

        logging.info(f"Downloading {args.url}")
        logging.info("Saving images")

        if not os.path.exists(args.directory_name):
            os.makedirs(args.directory_name)

        logging.info("Launching renderer")
        cmd = f"python3 {args.exec_path}/big-renderer/renderer.py --presentationFile '{args.url}' --slideDir '{args.directory_name}' --width '{args.width}' --height '{args.height}'"
        subprocess.run(cmd, shell=True)

    elif args.action == "generate-pptx":
        logging.info("Generating PDF")
        cmd = f"python3 {args.exec_path}/big-pptx/images_to_pptx.py -r ./ -s ./{args.directory_name}/ --name {args.name}"
        subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()
