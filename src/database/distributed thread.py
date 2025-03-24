import signal
import time
import datetime
import unittest
from threading import Thread

import redis


def timeout_handler(signum, frame):
    raise TimeoutError("Processing time exceeded")


class RedisLock:
    def __init__(self, lock_key, timeout):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.lock_key = lock_key
        self.timeout = timeout

    def set_lock(self):
        if self.r.set(self.lock_key, 'locked', ex=self.timeout, nx=True):
            return True
        else:
            return False

    def release_lock(self):
        if self.r.get(self.lock_key) == 'locked':
            self.r.delete(self.lock_key)
            return True
        else:
            return False


def single(max_processing_time: datetime.timedelta):

    def decorator(func):

        def wrapper(*args, **kwargs):
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            lock = RedisLock(func.__name__, int(max_processing_time.total_seconds()))
            if not lock.set_lock():
                raise RuntimeError("Function is already processing")

            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                total_time = time.time() - start_time
                if total_time > max_processing_time.total_seconds():
                    raise RuntimeError("Timeout")
                return result
            finally:
                signal.alarm(0)
                lock.release_lock()

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    time.sleep(5)


class TestSingle(unittest.TestCase):

    @single(max_processing_time=datetime.timedelta(seconds=2))
    def process_transaction(self):
        time.sleep(5)

    def test_func_running_exception(self):
        thread = Thread(target=process_transaction)
        thread.start()
        time.sleep(1)

        with self.assertRaises(RuntimeError) as e:
            self.process_transaction()
        self.assertEqual(str(e.exception), "Function is already processing")

        thread.join(timeout=1)


if __name__ == "__main__":
    unittest.main()
