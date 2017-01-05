#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Filename: main.py
# Author:   KuoE0 <kuoe0.tw@gmail.com>
#
# Copyright (C) 2017
#
# Distributed under terms of the MIT license.

"""

"""
import sys
import sqlite3
import os.path
import time
from colored import fg, attr
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DatabaseUpdated(FileSystemEventHandler):

    def __init__(self, _db_path):
        self.db_path = _db_path
        self.last_message = ""

    def on_modified(self, event):
        new_message = self.get_lastest_message()
        if new_message == self.last_message:
            return
        print(new_message)
        self.last_message = new_message

    def get_lastest_message(self):
        cmd = "SELECT chatname,timestamp,author,from_dispname,body_xml FROM Messages ORDER BY id DESC"
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(cmd)
        chatname, timestamp, author, from_dispname, body_xml = c.fetchone()
        displayname = self.get_displayname_of_chatname(chatname)
        displayname = "{0}{1}{2}".format(fg(9), displayname, attr('reset'))
        from_dispname = "{0}{1}{2}".format(
            fg(10), from_dispname, attr('reset'))
        body_xml = "{0}{1}{2}".format(fg(11), body_xml, attr('reset'))
        return "{0} / {1} / {2}".format(displayname, from_dispname, body_xml)

    def get_displayname_of_chatname(self, chatname):
        cmd = "SELECT displayname FROM Conversations WHERE identity='{0}'".format(
            chatname)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(cmd)
        displayname = c.fetchone()[0]
        return displayname

if __name__ == "__main__":
    db_path = sys.argv[1]
    event_handler = DatabaseUpdated(db_path)
    observer = Observer()
    observer.schedule(event_handler, os.path.dirname(db_path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
