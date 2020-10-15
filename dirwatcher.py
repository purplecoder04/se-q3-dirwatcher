#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Erica best ,help from Peter Mayor"

import sys
import signal
import os
import time
import argparse
import logging
exit_flag = False
watch_dict = {}

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def search_for_magic(filename, start_line, magic_string, path):
    """[This the function the open an file and search for the magic string]

    Args:
        filename ([str]): [the filename is the file that is being search]
        start_line ([int]): [is the start line of the file]
        magic_string ([str]): [the word that being found]
        path ([str]): [the path that is being searched]
    """
    with open(path + "/" + filename) as f:
        found_lines = []
        for line_num, line_string in enumerate(f):
            if line_num < start_line:
                continue
            found_index = line_string.find(magic_string)
            watch_dict[filename] = line_num + 1
            if found_index != -1:
                found_lines.append(line_num + 1)
        if len(found_lines) > 0:
            logging.info(
                f"New magic_string detected:{filename},line#'s{found_lines}")
    return


def watch_directory(path, magic_string, extension, interval):
    """[this function will watch a directory and logger any changes
    found in that directory]

    Args:
        path ([str]): [the path to the directory]
        magic_string ([str]): [description]
        extension ([str]): [the type of extension to watch for]
    """
    if not os.path.isdir(path):
        logger.warning("Directory{path} does not exist")
        return
    filelist = os.listdir(path)
    for key, value in watch_dict.items():
        if key not in filelist:
            logger.info(f"file deleted:{key}")
            watch_dict.pop(key)
    for file_name in filelist:
        if file_name not in watch_dict and file_name.endswith(extension):
            logger.info(f"New File added {file_name}")
            watch_dict[file_name] = 0
        search_for_magic(file_name, watch_dict[file_name], magic_string, path)
    return


def create_parser():
    """[this function setup parser  for command line argument]

    """
    parser = argparse.ArgumentParser(description='well change later')
    parser.add_argument('-d', "--dir", help='directory to be watched')
    parser.add_argument('-i', "--int", type=int, default=1,
                        help='seconds between polling')
    parser.add_argument('-e', "--ext", default='.txt',
                        help='extension to be watched')
    parser.add_argument("text", help='magic text string to look look for')
    args = parser.parse_args()
    return args


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped
    here as well (SIGHUP?)
    Basically, it just sets a global flag, and main()
    will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    if signal.Signals(sig_num).name == 'SIGINT':
        logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True
    if signal.Signals(sig_num).name == 'SIGTERM':
        logger.warning('Received ' + signal.Signals(sig_num).name)
    logger.info("""
     ____________________\n
    Exiting the Program
    ________________________\n""")


def main(args):
    """[this function runs the while loop, flag,time.sleep and signal]

    Args:
        args ([any type]): [depends on what is used]
    """
    args = create_parser()
    # search_for_magic("test.txt", 0, args.text)
    # watch_directory(args.dir, args.text, args.ext, args.int)
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    logger.info("""
    ______________________________________________________________________\n
    Starting the to watch directory {args.dir} for text of <{args.text}>
    ______________________________________________________________________\n
    """)

    while not exit_flag:
        try:
            watch_directory(args.dir, args.text, args.ext, args.int)
            # print(watch_dict)
            # call my directory watching function
            pass
        except Exception as e:
            # print(e)
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
