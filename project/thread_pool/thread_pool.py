from threading import Thread, Lock, Event
from typing import List, Callable, Set
from concurrent.futures import ThreadPoolExecutor
from itertools import product


class ThreadPool:
    """
    A class for managing a pool of threads that can execute tasks concurrently.

    Attributes:
        num_threads : int
            The number of worker threads in the pool.
        tasks : List
            A list that holds tasks (functions) to be executed by the worker threads.
        threads : List[Thread]
            A list of the threads in the pool.
        is_active : bool
            A flag indicating if the thread pool is active and can accept new tasks.
        task_event : threading.Event
            An event used to signal when new tasks are available for worker threads to process.
            The event is set whenever a new task is enqueued and cleared when there are no tasks to process.

        lock : threading.Lock
            A lock to ensure thread-safe access to the task list, preventing race conditions
            when tasks are being added, removed, or accessed by worker threads.

    Methods:
        __init__(num_threads: int) -> None:
            Initializes the ThreadPool with a fixed number of worker threads and starts them.

        worker() -> None:
            A worker thread that processes tasks from the queue. Runs in a loop until the thread pool is disposed.

        enqueue(task: Callable) -> None:
            Adds a new task to the queue to be executed by an available worker thread.

        dispose() -> None:
            Signals all worker threads to finish their current tasks and terminate. Prevents new tasks from being added.
    """

    def __init__(self, num_threads: int) -> None:
        """
        Initializes the ThreadPool with a given number of threads and starts each one.

        Parameters:
        ----------
        num_threads : int
            The number of worker threads to be created and managed by the pool.
        """

        self.num_threads: int = num_threads
        self.tasks: List[Callable | None] = []
        self.threads: List[Thread] = []
        self.is_active: bool = True
        self.lock: Lock = Lock()
        self.task_event: Event = Event()

        for _ in range(num_threads):
            thread = Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def worker(self) -> None:
        """
        Worker method run by each thread.

        Continuously waits for tasks from the queue and executes them. Terminates when
        the thread pool is disposed and the shutdown signal (None) is received.
        """

        while self.is_active or self.tasks:
            with self.lock:
                if self.tasks:
                    task = self.tasks.pop(0)
                else:
                    task = None

            if task:
                try:
                    task()
                finally:
                    self.task_event.clear()
            else:
                if self.is_active:
                    self.task_event.wait()

    def enqueue(self, task: Callable) -> None:
        """
        Adds a task to the queue to be executed by a worker thread.

        Parameters:
        ----------
        task : Callable
            A callable function representing the task to be executed.

        Raises:
        -------
        RuntimeError
            If the thread pool is inactive and cannot accept new tasks.
        """

        if not self.is_active:
            raise RuntimeError("ThreadPool is inactive. Cannot enqueue new tasks.")

        with self.lock:
            self.tasks.append(task)

        self.task_event.set()

    def dispose(self) -> None:
        """
        Disposes of the thread pool by signaling all worker threads to finish their tasks and terminate.
        It also prevents new tasks from being added to the pool.
        """
        if self.is_active == False:
            return

        self.task_event.set()
        self.is_active = False

        for thread in self.threads:
            thread.join()
