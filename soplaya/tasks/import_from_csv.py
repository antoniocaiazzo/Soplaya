import csv
import queue
import threading

from more_itertools import chunked

from soplaya.context import app, db
from soplaya.models.Report import Report
from soplaya.tasks.manager import Task

default_chunk_size = 32


class ImportFromCSVTask(Task):

    def __init__(self, task_id: str, **kwargs):
        super().__init__(task_id)
        self.__csv_path = kwargs["csv_path"]
        self.__chunk_size = kwargs.get("chunk_size", default_chunk_size)

    def producer(self, pipeline: queue.Queue, event_end: threading.Event):
        while not event_end.is_set():
            with open(self.__csv_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                i = 0
                for chunk_rows in chunked(reader, self.__chunk_size):
                    pipeline.put(chunk_rows)
                    i += 1
            event_end.set()

    def consumer(self, pipeline: queue.Queue, event_end: threading.Event):
        with app.app_context():
            while not event_end.is_set() or not pipeline.empty():
                rows: list[dict] = pipeline.get()
                for row in rows:
                    report = Report(**row)
                    db.session.merge(report)
                db.session.commit()
