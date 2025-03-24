import signal
import time
import threading
import datetime


def timeout_handler(signum, frame):
    raise TimeoutError("Processing time exceeded")


def single(max_processing_time: datetime.timedelta):
    def decorator(func):
        lock = threading.Lock()
        is_processing = False

        def wrapper(*args, **kwargs):
            nonlocal is_processing
            if not lock.acquire(blocking=False):
                raise RuntimeError('Already processing')

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(max_processing_time.total_seconds()))

            try:
                is_processing = True
                start_time = time.time()
                result = func(*args, **kwargs)
                total_time = time.time() - start_time
                if total_time > max_processing_time.total_seconds():
                    raise TimeoutError("Processing time exceeded")
                return result
            finally:
                signal.alarm(0)
                if is_processing:
                    is_processing = False
                    lock.release()

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(seconds=2))
def process_transaction():
    time.sleep(5)


if __name__ == "__main__":
    try:
        print(time.time())
        process_transaction()

    except RuntimeError as e:
        print("Timeout")

    finally:
        print(time.time())
