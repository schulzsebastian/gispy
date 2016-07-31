import os
import json
import csv
import shapefile
from pyproj import Proj, transform


class Point(object):

    def __init__(self, coordinates):
        self.coordinates = coordinates
        if not self.coordinates:
            raise AttributeError('Argument not found')
        elif not isinstance(self.coordinates, list):
            raise TypeError('Argument is not a list')
        elif len(self.coordinates) != 2:
            raise ValueError('Argument is not a pair of coordinates')
        elif not all(isinstance(_, float) for _ in self.coordinates):
            raise ValueError('Coordinates are not floats')

    def __str__(self):
        return "Point object: %s" % self.coordinates

    def coords(self):
        return self.coordinates

    def reproject(self, in_epsg, out_epsg):
        in_proj = Proj(init="epsg:" + str(in_epsg))
        out_proj = Proj(init="epsg:" + str(out_epsg))
        x, y = self.coordinates[0], self.coordinates[1]
        return Point(list(transform(in_proj, out_proj, x, y)))

    def to_geojson(self, **kwargs):
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Point",
                        "coordinates": self.coordinates
                    }
                }
            ]
        }
        path = kwargs.get('path', None)
        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            filename = kwargs.get('filename', None)
            if not filename:
                filename = 'Point'
            with open(path + '/' + filename + '.geojson', 'w') as outfile:
                json.dump(data, outfile, indent=4,
                          sort_keys=True, separators=(',', ':'))
        return json.dumps(data)

    def to_text(self, **kwargs):
        data = ';'.join([str(_) for _ in self.coordinates])
        path = kwargs.get('path', None)
        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            filename = kwargs.get('filename', None)
            if not filename:
                filename = 'Point'
            with open(path + '/' + filename + '.txt', 'w') as outfile:
                outfile.write(data)
        return data

    def to_csv(self, **kwargs):
        data = ';'.join([str(_) for _ in self.coordinates])
        path = kwargs.get('path', None)
        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            filename = kwargs.get('filename', None)
            if not filename:
                filename = 'Point'
            with open(path + '/' + filename + '.csv', 'w') as outfile:
                writer = csv.writer(outfile, delimiter=';', quotechar='"')
                writer.writerow(self.coordinates)
        return data

    def to_shp(self, **kwargs):
        w = shapefile.Writer(shapefile.POINT)
        w.point(self.coordinates[0], self.coordinates[1])
        path = kwargs.get('path', None)
        filename = kwargs.get('filename', None)
        if not filename:
            filename = 'Point'
        if path:
            w.save(path + '/' + filename)
        else:
            w.save('./' + filename)
        data = ';'.join([str(_) for _ in self.coordinates])
        return data
