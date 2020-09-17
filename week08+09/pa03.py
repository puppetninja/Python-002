#!/usr/bin/env python3
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
import time
from functools import wraps


def my_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time_begin = time.time()
        func(*args, **kwargs)
        time_end = time.time()
        print("%s execution time: %ss" % (func.__name__,
                                          time_end - time_begin))
    return wrapper


@my_timer
def test_func1():
    print(f'{test_func1.__name__} is gonna sleep 1 sec.')
    time.sleep(1)


@my_timer
def test_func2(name='Bob', age=30):
    print(f'{name} is {age} years old')


if __name__ == '__main__':
    test_func1()
    test_func2()
