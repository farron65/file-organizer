import shutil
import logging

import time

import re
import json

from pathlib import Path

from watchdog import events
from watchdog.observers import Observer

logging.basicConfig(level=logging.DEBUG)

class MyEventHandler(events.FileSystemEventHandler):
    
    def __init__(self):
        super().__init__()
        with open("config.json", "r") as f:
            self.classes = json.load(f)
    
    def catch_handler(self, event: events.FileSystemEvent):
        file_path = str(event.src_path)
        file: str = Path(file_path).name
        tokens = re.split("[ -.]", file)
        for token in tokens:
            cls = self.classes.get(token.lower())
            if cls:
                logging.debug(f"Found lesson {file} with a path: {cls}")
                t = 0
                while True:
                    if t > 100:
                        raise TimeoutError
                    t += 1
                    try:
                        shutil.move(file_path, f"{cls}/{file}")
                        logging.info("Successfully moved the file")
                        break
                    except PermissionError:
                        pass
                    
                    logging.info("waiting")
                    time.sleep(5)
    
    def on_moved(self, event: events.DirMovedEvent | events.FileMovedEvent) -> None:
        self.catch_handler(event)

    def on_created(self, event: events.DirCreatedEvent | events.FileCreatedEvent) -> None:
        self.catch_handler(event)

event_handler = MyEventHandler()

observer = Observer()
observer.schedule(event_handler, path="C:/Users/admin/Downloads", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()