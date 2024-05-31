from queue import Queue
from threading import Event
from typing import Generator

import pytest


@pytest.fixture
def task_plumbing() -> Generator[tuple[Queue, Event], None, None]:
    pipeline = Queue()
    end_task = Event()

    yield pipeline, end_task

    pipeline.empty()
    end_task.clear()


def test_import_from_csv(app, db, task_plumbing: tuple[Queue, Event], test_dataset_path: str) -> None:
    pipeline, end_task = task_plumbing

    from soplaya.tasks.import_from_csv import ImportFromCSVTask

    task = ImportFromCSVTask("test", csv_path=test_dataset_path, chunk_size=3)

    task.producer(pipeline, end_task)

    assert pipeline.qsize() == 3
    assert end_task.is_set()

    task.consumer(pipeline, end_task)

    assert pipeline.qsize() == 0
