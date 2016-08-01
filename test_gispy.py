import unittest
from gispy import *


class PointTestCase(unittest.TestCase):

    def setUp(self):
        self.path = './test'
        self.filename = 'test'
        self.properties = {'name': 'Punkt', 'wartosc': 3}
        self.in_epsg = 4326
        self.out_epsg = 2180
        self.coords = [10.00, 20.00]
        self.point = Point(self.coords, self.properties)

    def test_coords(self):
        self.assertEqual(self.point.coords(), self.coords)
        self.assertEqual(self.point.props(), self.properties)

    def test_reproject(self):
        reprojected = self.point.reproject(self.in_epsg, self.out_epsg)
        reverse = reprojected.reproject(self.out_epsg, self.in_epsg)
        first = [round(_) for _ in self.point.coords()]
        second = [round(_) for _ in reverse.coords()]
        self.assertEqual(first, second)

    def test_to_geojson(self):
        geojson = self.point.to_geojson(path=self.path, filename=self.filename)
        geojson_dict = json.loads(geojson)
        return_coords = geojson_dict['features'][0]['geometry']['coordinates']
        with open(self.path + '/' + self.filename + '.geojson', 'r') as infile:
            in_str = ''
            for row in infile:
                in_str += row.rstrip()
            out_dict = json.loads(in_str)
            file_coords = out_dict['features'][0]['geometry']['coordinates']
        self.assertEqual(file_coords, self.point.coords())
        self.assertEqual(return_coords, self.point.coords())

    def test_to_text(self):
        to_text = self.point.to_text(path=self.path, filename=self.filename)
        return_coords = [float(_) for _ in to_text.split(';')]
        file_coords = None
        with open(self.path + '/' + self.filename + '.txt', 'r') as infile:
            for row in infile:
                file_coords = [float(_) for _ in row.split(';')]
        self.assertEqual(file_coords, self.point.coords())
        self.assertEqual(return_coords, self.point.coords())

    def test_to_csv(self):
        to_csv = self.point.to_csv(path=self.path, filename=self.filename)
        return_coords = [float(_) for _ in to_csv.split(';')]
        file_coords = None
        with open(self.path + '/' + self.filename + '.csv', 'r') as infile:
            reader = csv.reader(infile, delimiter=';', quotechar='"')
            for row in reader:
                file_coords = [float(_) for _ in row]
        self.assertEqual(file_coords, self.point.coords())
        self.assertEqual(return_coords, self.point.coords())

    def test_to_shp(self):
        to_shp = self.point.to_shp(path=self.path, filename=self.filename)
        return_coords = [float(_) for _ in to_shp.split(';')]
        shp = shapefile.Reader(self.path + '/' + self.filename)
        geom_type = shp.shapes()[0].shapeType
        self.assertEqual(return_coords, self.point.coords())
        self.assertEqual(geom_type, 1)

if __name__ == '__main__':
    unittest.main()
