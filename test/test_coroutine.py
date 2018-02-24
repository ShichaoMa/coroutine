import socket
from coroutine import EventLoop, sleep, coroutine, get_buffer, Return


@coroutine
def sum(a, b):
    print("Sum start. %s + %s" % (a, b))
    yield sleep(1)
    result = yield a + b
    print("Sum stop. %s + %s" % (a, b))
    Return(result)


@coroutine
def multi(a, b):
    print("Multi start. %s x %s" % (a, b))
    yield sleep(2)
    result = yield a * b
    print("Multi stop. %s x %s" % (a, b))
    Return(result)


@coroutine
def aaddbthenmutilc(a, b, c):
    sum_result = yield sum(a, b)
    multi_result = yield multi(sum_result, c)
    Return(multi_result)


@coroutine
def aaddcthenmutilb(a, b, c):
    sum_result = yield sum(a, c)
    multi_result = yield multi(sum_result, b)
    Return(multi_result)


@coroutine
def socket_coroutine():
    print("socket_coroutine start. ")
    client = socket.socket()
    client.connect(("", 1234))
    buffer = yield get_buffer(client)
    client.close()
    print("socket_coroutine stop. ")
    Return(buffer)


@coroutine
def normal():
    a = yield 1
    print("Get a: %s" % a)
    b = yield 2
    print("Get b: %s" % b)
    c = yield 3
    print("Get c: %s" % c)
    Return(c)


if __name__ == "__main__":
    coroutine0 = normal()
    coroutine1 = aaddbthenmutilc(1, 2, 3)
    coroutine2 = aaddcthenmutilb(1, 2, 3)
    coroutine3 = sum(44, 55)
    coroutine4 = multi(99, 10)
    coroutine5 = socket_coroutine()
    loop = EventLoop.instance()
    loop.run_until_complete(coroutine0, coroutine1, coroutine2, coroutine3, coroutine4, coroutine5)
    print(coroutine0.result())
    print(coroutine1.result())
    print(coroutine2.result())
    print(coroutine3.result())
    print(coroutine4.result())
    print(coroutine5.result())
