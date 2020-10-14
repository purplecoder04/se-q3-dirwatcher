#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Erica best , Peter Mayor"

import sys
import signal
import os
import time
import argparse
import logging
exit_flag = False
logging.basicConfig(
                format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG )
logger = logging.getLogger(__name__)


def search_for_magic(filename, start_line, magic_string):
    with open(filename) as f:
        for line_num, line_string in enumerate(f):
            if line_string.find(magic_string) != -1:
                print(filename, line_num)
    return


def watch_directory(path, magic_string, extension, interval):
    filelist = os.listdir(path)
    for file_name in filelist:
        search_for_magic(path + "/" + file_name, 0, magic_string)
    return


def create_parser():
    parser = argparse.ArgumentParser(description='well change later')
    parser.add_argument('-d', "--dir", help='directory to be watched')
    parser.add_argument('-i', "--int", default=1,
                        help='seconds between polling')
    parser.add_argument('-e', "--ext", default='.txt',
                        help='extension to be watched')
    parser.add_argument("text", help='magic text string to look look for')
    args = parser.parse_args()
    return args


def signal_handler(sig_num, frame):
    if signal.Signals(sig_num).name == 'SIGINT':
        logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main(args):
    args = create_parser()
    # search_for_magic("test.txt", 0, args.text)
    # watch_directory(args.dir, args.text, args.ext, args.int)
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            watch_directory(args.dir, args.text, args.ext, args.int)
            # call my directory watching function
            pass
        except Exception as e:
            print(e)
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(args.int)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
