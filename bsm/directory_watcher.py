import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Log dosyasının yolu
LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"

# Event Handler Sınıfı
class WatcherHandler(FileSystemEventHandler):
    def process(self, event):
        event_type = event.event_type
        file_path = event.src_path
        file_name = os.path.basename(file_path)  # Dosya adını al

        log_entry = {
            "event": event_type,
            "file_name": file_name,
            "file_path": file_path,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        print(log_entry)  # Konsola yazdır
        self.write_log(log_entry)

    def write_log(self, entry):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)
        
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=4)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_moved(self, event):
        log_entry = {
            "event": "moved",
            "file_name": os.path.basename(event.src_path),
            "source_path": event.src_path,
            "destination_path": event.dest_path,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(log_entry)
        self.write_log(log_entry)

if __name__ == "__main__":
    path = "/home/ubuntu/bsm/test"  # İzlenecek dizin
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    print(f"İzleme başlatıldı: {path}")
    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
