import shutil
import logging

import time

import re
import json

from pathlib import Path

from watchdog import events
from watchdog.observers import Observer

logging.basicConfig(level=logging.DEBUG)

class FileMove():
    def __init__(self, file, dt):
        self.file = file
        self.dt = dt
        
    def move_file(self):
        shutil.move(self.file, self.dt)
        
    def retry_move(self):
        t = 0
        while True:
            if t > 100:
                raise TimeoutError
            t += 1
            try:
                self.move_file()
                logging.info(f"Successfully moved the file '{Path(self.file).name}' to: '{self.dt}'")
                break
            except (PermissionError, FileNotFoundError):
                pass          
            logging.info("waiting")
            time.sleep(5)

class FileWatcher(events.FileSystemEventHandler):
    
    def __init__(self):
        super().__init__()
        with open("config.json", "r") as f:
            self.lesson_path = json.load(f)
    
    def catch_handler(self, event: events.FileSystemEvent):
        file_path = str(event.src_path)
        tokens = re.split("[ -.]", Path(file_path).name)
        if Path(file_path).suffix == ".tmp" or Path(file_path).suffix == ".crdownload":
            return
        for token in tokens:
            cls = self.lesson_path.get(token.lower())
            if cls:
                file_move = FileMove(file_path, cls)
                file_move.retry_move()
    
    def on_moved(self, event: events.DirMovedEvent | events.FileMovedEvent) -> None:
        self.catch_handler(event)

    def on_created(self, event: events.DirCreatedEvent | events.FileCreatedEvent) -> None:
        self.catch_handler(event)
            
event_handler = FileWatcher()

observer = Observer()
observer.schedule(event_handler, path="C:/Users/admin/Downloads", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
finally:
    observer.stop()
    observer.join()