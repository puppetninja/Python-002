#!/usr/bin/env python3
from abc import ABCMeta, abstractmethod
import unittest


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def animal_type(self):
        return self._animal_type

    @animal_type.setter
    def animal_type(self, value):
        animal_type_range = ('食肉', '食草', '杂食')
        if value not in animal_type_range:
            raise ValueError(
                f'animal type has to be one of {animal_type_range}'
            )
        else:
            self._animal_type = value

    @property
    def body_type(self):
        return self._body_type

    @body_type.setter
    def body_type(self, value):
        body_type_range = ('小', '中', '大', '特大')
        if value not in body_type_range:
            raise ValueError(
                f'animal type has to be one of {body_type_range}'
            )
        else:
            self._body_type = value

    @property
    def personality(self):
        return self._personality

    @personality.setter
    def personality(self, value):
        self._personality = value

    def is_dangerous_animal(self):
        return self._body_type != '小' and \
            self._animal_type == '食肉' and \
            self._personality == '凶猛'


class Cat(Animal):
    _sound = '喵'

    def __init__(self, name, animal_type, body_type, personality):
        self.name = name
        self.animal_type = animal_type
        self.body_type = body_type
        self.personality = personality

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def good_for_pet(self):
        return '是' if self.personality != '凶猛' else '否'

    @property
    def sound(self):
        return type(self)._sound

    def __repr__(self):
        return '猫 {}: {}, {}, {}, 叫声:{}, 合适做宠物:{}'.\
                format(self.name,
                       self.animal_type, self.body_type, self.personality,
                       self.sound, self.good_for_pet)


class Dog(Animal):
    _sound = '汪'

    def __init__(self, name, animal_type, body_type, personality):
        self.name = name
        self.animal_type = animal_type
        self.body_type = body_type
        self.personality = personality

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def good_for_pet(self):
        return '是' if self.personality != '凶猛' else '否'

    @property
    def sound(self):
        return type(self)._sound

    def __repr__(self):
        return '狗 {}: {}, {}, {}, 叫声:{}, 合适做宠物:{}'.\
                format(self.name,
                       self.animal_type, self.body_type, self.personality,
                       self.sound, self.good_for_pet)


class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animals = set()

    def add_animal(self, animal):
        if animal in self.animals:
            print("动物:{} 已经在动物园里了".format(animal))
        else:
            if isinstance(animal, Cat):
                self.Cat = property(lambda self: True)
            if isinstance(animal, Dog):
                self.Dog = property(lambda self: True)
            self.animals.add(animal)

    def __repr__(self):
        return '动物园 {}: 动物列表-{}'.format(self.name, self.animals)


class ZooTest(unittest.TestCase):
    def test_animal(self):
        self.assertRaises(TypeError, Animal)

    def test_cat(self):
        cat1 = Cat('大橘', '食肉', '大', '温顺')
        cat2 = Cat('狸花', '食肉', '小', '凶猛')

        self.assertRaises(ValueError, Cat, '大橘', '食腐', '大', '温顺')

        self.assertEqual('猫 大橘: 食肉, 大, 温顺, 叫声:喵, 合适做宠物:是', str(cat1))
        self.assertNotEqual('猫 起司: 食肉, 大, 温顺, 叫声:喵, 合适做宠物:是', str(cat1))

        self.assertEqual('猫 狸花: 食肉, 小, 凶猛, 叫声:喵, 合适做宠物:否', str(cat2))
        self.assertNotEqual('猫 狸花: 杂食, 小, 凶猛, 叫声:喵, 合适做宠物:否', str(cat2))

    def test_dog(self):
        dog1 = Dog('大黄', '杂食', '大', '温顺')
        dog2 = Dog('小黑', '食肉', '小', '逗比')

        self.assertRaises(ValueError, Dog, '大黄', '食腐', '大', '温顺')

        self.assertEqual('狗 大黄: 杂食, 大, 温顺, 叫声:汪, 合适做宠物:是', str(dog1))
        self.assertNotEqual('猫 起司: 食肉, 大, 温顺, 叫声:喵, 合适做宠物:是', str(dog1))

        self.assertEqual('狗 小黑: 食肉, 小, 逗比, 叫声:汪, 合适做宠物:是', str(dog2))
        self.assertNotEqual('狗 二哈: 食肉, 小, 逗比, 叫声:汪, 合适做宠物:否', str(dog2))

    def test_zoo(self):
        z = Zoo('时间动物园')
        cat1 = Cat('大橘', '食肉', '大', '温顺')
        dog1 = Dog('小黑', '食肉', '小', '逗比')
        self.assertEqual('动物园 时间动物园: 动物列表-set()', str(z))

        z.add_animal(cat1)
        self.assertTrue(hasattr(z, 'Cat'))
        self.assertFalse(hasattr(z, 'Dog'))

        z.add_animal(dog1)
        self.assertTrue(hasattr(z, 'Cat'))
        self.assertTrue(hasattr(z, 'Dog'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
