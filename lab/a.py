async def test1(x):
    await x

def test2():
    return 3

import inspect

def test3():
    yield 1

print(inspect.iscoroutine(test1(1)))