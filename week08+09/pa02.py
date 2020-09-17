#!/usr/bin/env python3
#
# 自定义一个 python 函数，实现 map() 函数的功能。
# python2 与 python3 map 返回的不同
# https://docs.python.org/zh-cn/3/library/functions.html#map
#
# map(function, iterable, ...)
# 返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。 如果传入了额外的
# iterable 参数，function 必须接受相同个数的实参并被应用于从所有可迭代对象中并行获取的项
# 当有多个可迭代对象时，最短的可迭代对象耗尽则整个迭代就将结束。 对于函数的输入已经是参数元组
# 的情况，请参阅
import unittest


def my_map(func, iterable):
    return (func(i) for i in iterable)


def test_func1(x: int):
    return x*x


def test_func2(x: str):
    return f'hello {x}'


class myMapTests(unittest.TestCase):
    # 将generator转化成list进行比较
    def test_list(self):
        test_list1 = [1, 2, 3]
        test_list2 = ['bob', 'alice', 'cameron']
        self.assertEqual(list(map(test_func1, test_list1)),
                         list(my_map(test_func1, test_list1)))
        self.assertEqual(list(map(test_func2, test_list2)),
                         list(my_map(test_func2, test_list2)))

    def test_tuple(self):
        test_tup1 = (1, 2, 3)
        test_tup2 = ('bob', 'alice', 'cameron')
        self.assertEqual(list(map(test_func1, test_tup1)),
                         list(my_map(test_func1, test_tup1)))
        self.assertEqual(list(map(test_func2, test_tup2)),
                         list(my_map(test_func2, test_tup2)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
