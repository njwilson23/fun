import unittest
from fun import Lens, compose_optics

class Address(object):
    def __init__(self, street, number):
        self.street = street
        self.number = number

class Street(object):
    def __init__(self, name):
        self.name = name

class Number(object):
    def __init__(self, val):
        self.val = val

class LensTests(unittest.TestCase):

    def test_identify(self):
        value = {"id": 1}
        self.assertEqual(Lens.get(value), {"id": 1})

    #def test_getattr(self):
    #    value = Address(Street("Ferndale"), Number(123))
    #    self.assertEqual(Lens.street.name.get(value), "Ferndale")

    def test_getitem(self):
        value = {"address": {"street": "Ferndale", "number": 123}}
        lens = Lens["address"]["street"]
        self.assertEqual(lens.get(value), "Ferndale")

    def test_setitem(self):
        value = {"address": {"street": "Ferndale", "number": 123}}
        expected = {"address": {"street": "Ferndale", "number": 456}}
        lens = Lens["address"]["number"]
        self.assertEqual(lens.set(value, 456), expected)

    def test_compose(self):
        lens0 = Lens["address"]
        lens1 = Lens["number"]
        lens2 = compose_optics(lens0, lens1)
        self.assertEqual(lens2, Lens["address"]["number"])


if __name__ == "__main__":
    unittest.main()

