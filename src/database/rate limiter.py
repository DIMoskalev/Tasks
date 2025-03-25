import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, limit=5, period=3):
        self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
        self.limit = limit
        self.period = period

    def test(self) -> bool:
        current_time = time.time()
        key = "rate_limiter"

        self.redis_client.zremrangebyscore(key, 0, current_time - self.period)

        request_count = self.redis_client.zcard(key)

        if request_count < self.limit:
            self.redis_client.zadd(key, {current_time: current_time})
            self.redis_client.expire(key, self.period)
            return True
        else:
            return False


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print(time.time())
            print("Rate limit exceed!")
        else:
            print(time.time())
            print("All good")

