import unittest
from fun import Lens, compose_optics
from fun.optics import Equals

class Address(Equals):

    def __init__(self, street, number):
        self.street = street
        self.number = number

    def __repr__(self):
        return "{} {}".format(self.number.val, self.street.name)

class Street(Equals):

    def __init__(self, name):
        self.name = name

class Number(Equals):

    def __init__(self, val):
        self.val = val

class LensTests(unittest.TestCase):

    def test_identity(self):
        value = {"id": 1}
        self.assertEqual(Lens.get(value), {"id": 1})

    def test_getattr(self):
        value = Address(Street("Ferndale"), Number(123))
        self.assertEqual(Lens.street.name.get(value), "Ferndale")

    def test_getitem(self):
        value = {"address": {"street": "Ferndale", "number": 123}}
        lens = Lens["address"]["street"]
        self.assertEqual(lens.get(value), "Ferndale")

    def test_setattr(self):
        value = Address(Street("Ferndale"), Number(123))
        expected = Address(Street("Nanaimo"), Number(123))
        lens = Lens.street.name
        self.assertEqual(lens.set(value, "Nanaimo"), expected)

    def test_setitem(self):
        value = {"address": {"street": "Ferndale", "number": 123}}
        expected = {"address": {"street": "Ferndale", "number": 456}}
        lens = Lens["address"]["number"]
        self.assertEqual(lens.set(value, 456), expected)

    def test_setitem_func(self):
        value = {"address": {"street": "Ferndale", "number": 123}}
        expected = {"address": {"street": "Ferndale", "number": 124}}
        lens = Lens["address"]["number"]
        self.assertEqual(lens.setf(value, lambda a: a+1), expected)

    def test_compose(self):
        lens0 = Lens["address"]
        lens1 = Lens["number"]
        lens2 = compose_optics(lens0, lens1)
        self.assertEqual(lens2, Lens["address"]["number"])

    def test_get_for_all(self):
        value = [{"id": 0, "color": "red"},
                 {"id": 1, "color": "blue"},
                 {"id": 2, "color": "yellow"}]
        lens = Lens.for_all["color"]
        self.assertEqual(lens.get(value), ["red", "blue", "yellow"])

    def test_set_for_all(self):
        value = [{"id": 0, "color": "red"},
                 {"id": 1, "color": "blue"},
                 {"id": 2, "color": "yellow"}]
        expected = [{"id": 0, "color": "apple"},
                    {"id": 1, "color": "apple"},
                    {"id": 2, "color": "apple"}]
        lens = Lens.for_all["color"]
        self.assertEqual(lens.set(value, "apple"), expected)

    def test_setf_for_all(self):
        value = [{"id": 0, "color": "red"},
                 {"id": 1, "color": "blue"},
                 {"id": 2, "color": "yellow"}]
        expected = [{"id": 0, "color": "RED"},
                    {"id": 1, "color": "BLUE"},
                    {"id": 2, "color": "YELLOW"}]
        lens = Lens.for_all["color"]
        self.assertEqual(lens.setf(value, str.upper), expected)

if __name__ == "__main__":
    unittest.main()

