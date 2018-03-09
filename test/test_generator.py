from coroutine import Return
from coroutine.components.generator_adapter import GeneratorAdapter


def fun():
    a = yield 111
    print("Got a: ", a)
    b = yield 222
    print("Got b: ", b)
    Return(a + b)


def bar():
    c = yield 333
    print("Got c: ", c)
    d = yield fun()
    print("Got d: ", d)
    e = yield fun()
    print("Got e", e)
    Return(c + d + e)

#
# def yield_from_bar():
#     c = yield 333
#     print("Got c: ", c)
#     d = yield from fun()
#     print("Got d: ", c)
#     return c + d


def test_only_yield():
    co = GeneratorAdapter(bar())
    print("Got 333", co.send(None))
    print("Got 111", co.send(3))
    print("Got 222", co.send(1))
    print("Got 111", co.send(6))
    print("Got 222", co.send(5))
    try:
        co.send(2)
    except StopIteration as e:
        print(e.args)


# def test_yield_from():
#     co = yield_from_bar()
#     # debugger()
#     print("Got 333", co.send(None))
#     print("Got 111", co.send(3))
#     print("Got 222", co.send(1))
#     try:
#         co.send(2)
#     except StopIteration as e:
#         print(e.args)

#test_yield_from()
test_only_yield()