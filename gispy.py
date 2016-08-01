import os
import json
import csv
import shapefile
from pyproj import Proj, transform


class Point(object):

    def __init__(self, coordinates, properties={}):
        self.coordinates = coordinates
        if not self.coordinates:
            raise AttributeError('Coordinates not found')
        elif not isinstance(self.coordinates, list):
            raise TypeError('Coordinates are not a list')
        elif len(self.coordinates) != 2:
            raise ValueError('It is not pair of coordinates')
        elif not all(isinstance(_, float) for _ in self.coordinates):
            raise ValueError('Coordinates are not floats')
        self.properties = properties
        if not isinstance(self.properties, dict):
            raise TypeError('Properties are not a dict')

    def __str__(self):
        obj = 'Coordinates: %s\n' % self.coordinates
        if self.properties:
            kv = []
            for k, v in self.properties.iteritems():
                kv.append(': '.join([str(k), str(v)]))
            return obj + '\n'.join(kv)
        return obj

    def coords(self):
        return self.coordinates

    def props(self):
        return self.properties

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
