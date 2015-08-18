#!/usr/bin/env python

"""Omnifocus to Kanban

Usage:
  of-to-kb.py (--trello | --leankit)
  of-to-kb.py -h | --help
  of-to-kb.py --version

"""

import logging
import logging.config
import os

from docopt import docopt

from omnifocus import Omnifocus
from kanban_board import LeanKit, Trello


def main():
    opts = docopt(__doc__)
    logging.debug("Current working directory: %s", os.getcwd())

    board = None

    if opts['--trello']:
        logging.info("Connecting to Trello board")
        board = Trello()
    elif opts['--leankit']:
        logging.info("Connecting to Leankit board")
        board = LeanKit()
    else:
        exit(-1)

    omnifocus = Omnifocus()
    external_ids = board.find_completed_card_ids()
    omnifocus.close_tasks([external_id for external_id in external_ids])

    tasks = omnifocus.flagged_tasks()
    new_tasks = []
    for task in tasks:
        identifier = task['identifier']
        if not board.card_exists(identifier):
            logging.debug(u'Adding %s to list of tasks to sync with board', identifier)
            new_tasks.append(task)
        else:
            logging.debug(u'Ignoring %s since it exists on the board', identifier)

    if len(new_tasks) > 0:
        board.add_cards(new_tasks)
    else:
        logging.info("Board is up to date - no cards to sync")


if __name__ == '__main__':
    logging.config.fileConfig('log.conf')
    main()
