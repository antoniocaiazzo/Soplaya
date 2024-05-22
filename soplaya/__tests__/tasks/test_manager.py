from typing import Generator
from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture
def testing_task_factory():
    class TestingTaskFactory:
        @staticmethod
        def get() -> Generator[MagicMock, None, None]:
            with patch("soplaya.tasks.manager.Task", autospec=True) as mock_task:
                yield mock_task

    yield TestingTaskFactory()


@pytest.mark.parametrize(
    "max_consumers, errors",
    (
        (1, []),
        (1, [ZeroDivisionError()]),
        (7, []),
        (3, [ZeroDivisionError(), ValueError(), NotImplementedError()]),
    ),
    ids=["Basic case", "Consumer error", "Many consumers", "Many errors"],
)
def test_task_manager_basic_case(testing_task_factory, max_consumers, errors):
    testing_task = next(testing_task_factory.get())
    testing_task.reset_mock(return_value=True, side_effect=True)
    testing_task.id = "uno"
    testing_task.get_max_consumers.return_value = max_consumers
    if len(errors) > 0:
        testing_task.consumer.side_effect = errors

    from soplaya.tasks.manager import TaskManager

    manager = TaskManager()
    manager.start_task(testing_task)
    manager.cleanup()

    result = manager.get_task_result("uno")
    assert result.task_id == "uno"
    assert result.done
    assert result.errors == errors

    testing_task.producer.assert_called_once()
    testing_task.get_max_consumers.assert_called_once()
    assert testing_task.consumer.call_count == max_consumers


def test_task_manager_reused_case(testing_task_factory):
    tasks = {}

    from soplaya.tasks.manager import TaskManager

    manager = TaskManager()

    for task_id in ["uno", "due", "tre"]:
        testing_task = next(testing_task_factory.get())
        testing_task.reset_mock(return_value=True, side_effect=True)
        testing_task.id = task_id
        testing_task.get_max_consumers.return_value = 1
        tasks[task_id] = testing_task

        manager.start_task(testing_task)

    manager.cleanup()

    for task_id, testing_task in tasks.items():
        result = manager.get_task_result(task_id)
        assert result.task_id == task_id
        assert result.done
        assert result.errors == []

        testing_task.producer.assert_called_once()
        testing_task.get_max_consumers.assert_called_once()
        testing_task.consumer.assert_called_once()

    # checking against a subtle init error where threads share the same pipeline and event
    assert manager._TaskManager__tasks["uno"].task_args != manager._TaskManager__tasks["due"].task_args
    assert manager._TaskManager__tasks["due"].task_args != manager._TaskManager__tasks["tre"].task_args
