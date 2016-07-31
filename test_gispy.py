import unittest
from gispy import *


class PointTestCase(unittest.TestCase):

    def setUp(self):
        self.coords = [10.00, 20.00]
        self.point = Point(self.coords)

    def test_coords(self):
        self.assertEqual(self.point.coords(), self.coords)

    def test_reproject(self):
        reprojected = self.point.reproject('4326', '2180')
        reverse = reprojected.reproject('2180', '4326')
        first = [round(x) for x in self.point.coords()]
        second = [round(x) for x in reverse.coords()]
        self.assertEquals(first, second)

if __name__ == '__main__':
    unittest.main()
