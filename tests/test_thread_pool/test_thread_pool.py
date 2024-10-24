import pytest
import time
import threading
from queue import Queue
from project.thread_pool.thread_pool import ThreadPool


def simple_task(results, task_num, delay=0.25):
    time.sleep(delay)
    results.put(f"Task {task_num} completed")


def test_num_threads():
    num_threads = 4
    pool = ThreadPool(num_threads)
    assert (
        threading.active_count() == num_threads + 1
    ), f"Expected {num_threads + 1} active threads, found {threading.active_count()}"
    pool.dispose()


def test_thread_disposal():
    num_threads = 2
    pool = ThreadPool(num_threads)

    results = Queue()

    for i in range(3):
        pool.enqueue(lambda i=i: simple_task(results, i))

    pool.dispose()

    for thread in pool.threads:
        assert not thread.is_alive(), "Thread should be terminated after dispose."

    with pytest.raises(RuntimeError):
        pool.enqueue(lambda: simple_task(results, 2))


def test_enqueue_tasks():

    num_threads = 3
    delay = 0.1
    n = 12

    pool = ThreadPool(num_threads)
    results = Queue()

    start_time = time.time()
    for i in range(n):
        pool.enqueue(lambda i=i: simple_task(results, i, delay=delay))

    pool.dispose()
    end_time = time.time()

    total_time = end_time - start_time

    # Time if concurrent: delay * n /  num_threads = 0.4 < 0.5.
    # Time if sequencial: delay * n = 1.2 > 0.5.

    assert (
        total_time < 0.5
    ), f"Tasks should have been executed concurrently, but took {total_time:.2f}s"

    completed_tasks = []
    while not results.empty():
        completed_tasks.append(results.get())

    assert (
        len(completed_tasks) == n
    ), f"Expected {n} tasks completed, got {len(completed_tasks)}"
    assert all(f"Task {i} completed" in completed_tasks for i in range(n))
