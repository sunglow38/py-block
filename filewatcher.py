import sys
import glob
import time
# import subprocess
import hashlib
import os
import requests
import urllib.request
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


BUF_SIZE = 65536
sha256 = hashlib.sha256()

def hash(file):
    fp = file
    if os.path.isfile(fp):
        with open(fp, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha256.update(data)
    return sha256.hexdigest()


class Watcher:
    DIRECTORY_TO_WATCH = r'C:\Users\Alec\data'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            h = hash(event.src_path)
            url = 'http://127.0.0.1:5000/transactions/onCreation'
            payload = {'File Hash': h, 'File Path': event.src_path, 'Signature': '1'}
            headers = {'content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers)

            print("Received created event - %s." % event.src_path)
            print('Hash of file: %s' % h)
            # r = requests.post(r'http://127.0.0.1', data={'File Hash'})

            print(response)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()


