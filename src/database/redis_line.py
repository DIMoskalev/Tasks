import redis
import json


class RedisQueue:
    def __init__(self, queue_name: str):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.queue_name = queue_name

    def publish(self, msg: dict):
        self.r.rpush(self.queue_name, json.dumps(msg))  # Преобразуем словарь в json и добавляем в очередь

    def consume(self) -> dict:
        msg = self.r.lpop(self.queue_name)  # Получаем сообщение из очереди и переводим его обратно в словарь
        if msg is not None:
            if msg:
                return json.loads(msg)
            else:
                return None


if __name__ == '__main__':
    q = RedisQueue('test')
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
