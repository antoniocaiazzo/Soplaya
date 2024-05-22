import queue
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from typing import Callable


class Task(ABC):

    def __init__(self, task_id: str):
        self.__id = task_id

    @abstractmethod
    def producer(self, pipeline: queue.Queue, event_end: threading.Event):
        pass

    @abstractmethod
    def consumer(self, pipeline: queue.Queue, event_end: threading.Event):
        pass

    @staticmethod
    def get_max_consumers() -> int:
        return 7

    @property
    def id(self):
        return self.__id


@dataclass
class TaskRunContext:
    task: Task
    task_args: dict = field(default_factory=lambda: {"pipeline": queue.Queue(), "event_end": threading.Event()})
    futures: list[Future] = field(default_factory=list)
    errors: list[Exception] = field(default_factory=list)

    def append_future(self, future: Future):
        self.futures.append(future)
        future.add_done_callback(self.__future_is_done)

    def __future_is_done(self, future: Future):
        try:
            future.result()
        except Exception as e:
            self.errors.append(e)

    def check_all_futures_done(self) -> bool:
        return all(f.done() for f in self.futures)


@dataclass
class TaskRunResult:
    task_id: str
    done: bool
    errors: list[Exception]


class TaskManager:

    def __init__(self):
        self.__tasks: dict[str, TaskRunContext] = {}
        self.__pool = ThreadPoolExecutor()

    def __run_with_context(self, fun: Callable, run_context: TaskRunContext):
        future = self.__pool.submit(fun, **run_context.task_args)
        run_context.append_future(future)

    def start_task(self, task: Task):
        run_context = TaskRunContext(task)
        self.__tasks[task.id] = run_context

        self.__run_with_context(task.producer, run_context)
        for c in range(max(1, task.get_max_consumers())):
            self.__run_with_context(task.consumer, run_context)

    def get_task_result(self, task_id: str) -> TaskRunResult:
        run_context = self.__tasks.get(task_id)
        result = TaskRunResult(run_context.task.id, run_context.check_all_futures_done(), run_context.errors)
        return result

    def cleanup(self):
        self.__pool.shutdown()
