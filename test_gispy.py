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
        first = [round(_) for _ in self.point.coords()]
        second = [round(_) for _ in reverse.coords()]
        self.assertEquals(first, second)

    def test_to_geojson(self):
        geojson = self.point.to_geojson()
        dict_geojson = json.loads(geojson)
        dict_coords = dict_geojson['features'][0]['geometry']['coordinates']
        self.assertEquals(dict_coords, self.point.coords())

    def test_to_text(self):
        to_text = self.point.to_text()
        point = Point([float(_) for _ in to_text.split(';')])
        self.assertEquals(point.coords(), self.point.coords())

    def test_to_csv(self):
        to_csv = self.point.to_csv()
        point = Point([float(_) for _ in to_csv.split(';')])
        self.assertEquals(point.coords(), self.point.coords())

    def test_to_shp(self):
        to_shp = self.point.to_shp()
        point = Point([float(_) for _ in to_shp.split(';')])
        self.assertEquals(point.coords(), self.point.coords())

if __name__ == '__main__':
    unittest.main()
