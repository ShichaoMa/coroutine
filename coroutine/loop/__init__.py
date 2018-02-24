# -*- coding:utf-8 -*-
import time

from coroutine.loop.event_loop import EventLoop
from ..components.future import Future
from ..components.generator_adapter import GeneratorAdapter, Coroutine


def coroutine(func):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__()
        self.gen = GeneratorAdapter(func(*args, **kwargs))

    def send(self, result):
        try:
            return self.gen.send(result)
        except (GeneratorExit, StopIteration) as e:
            self.set_result(e.args[0] if e.args else None)
            raise

    def throw(self, typ, val=None, tb=None):
        return self.gen.throw(typ, val, tb)

    def __iter__(self):
        return iter(self.gen)

    def __await__(self):
        # await关键字是和async配套的，这里不使用。
        pass

    cls = type(func.__name__,
               (Future, Coroutine),
               {"__init__": __init__,
                "send": send,
                "throw": throw,
                "__iter__": __iter__,
                "__await__": __await__})

    return cls


def sleep(seconds):
    future = Future()

    def callback():
        future.set_result(None)

    EventLoop.instance().call_at(time.time() + seconds, callback)
    Return((yield future))


def get_buffer(socket):
    future = Future()

    def callback(fd_obj, events):
        future.set_result(fd_obj.recv(1024))

    EventLoop.instance().add_handler(socket, callback, EventLoop.READ)
    Return((yield future))


def Return(val):
    raise StopIteration(val)
