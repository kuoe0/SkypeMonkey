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
        self.last_timestamp = int(time.time())

    def on_modified(self, event):
        self.print_new_messages()

    def print_new_messages(self):
        cmd = "SELECT convo_id,timestamp,author,from_dispname,body_xml FROM Messages WHERE timestamp > {0} ORDER BY id".format(
            self.last_timestamp)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(cmd)
        messages = c.fetchall()

        for msg in messages:
            convo_id, timestamp, author, from_dispname, body_xml = msg
            self.last_timestamp = timestamp
            displayname = self.get_conversation_name(convo_id)
            displayname = "{0}{1}{2}".format(fg(9), displayname, attr('reset'))
            from_dispname = "{0}{1}{2}".format(
                fg(10), from_dispname, attr('reset'))
            body_xml = "{0}{1}{2}".format(fg(11), body_xml, attr('reset'))
            print("{0} / {1} / {2}".format(displayname, from_dispname, body_xml))

    def get_conversation_name(self, convo_id):
        cmd = "SELECT displayname FROM Conversations WHERE id={0}".format(
            convo_id)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(cmd)
        displayname = c.fetchone()[0]
        return displayname

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: skypeMonkey.py3 [path of Skype database])")
    else:
        db_path = sys.argv[1]
        event_handler = DatabaseUpdated(db_path)
        observer = Observer()
        observer.schedule(event_handler, os.path.dirname(
            db_path), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
