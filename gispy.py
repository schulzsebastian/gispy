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
        obj = 'Point object\nCoordinates: %s\n' % self.coordinates
        if self.properties:
            kv = [': '.join([k, v]) for k, v in self.properties.iteritems()]
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
        return Point(list(transform(in_proj, out_proj, x, y)), self.properties)

    def to_geojson(self, **kwargs):
        path = kwargs.get('path', None)
        if not path:
            path = '.'
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                raise ValueError('Path is invalid.')
        filename = kwargs.get('filename', None)
        if not str(filename):
            filename = 'Point'
        data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": self.properties,
                    "geometry": {
                        "type": "Point",
                        "coordinates": self.coordinates
                    }
                }
            ]
        }
        with open(path + '/' + str(filename) + '.geojson', 'w') as outfile:
            json.dump(data, outfile, indent=4,
                      sort_keys=True, separators=(',', ':'))
        return self

    def to_text(self, **kwargs):
        if self.properties:
            data = 'coord_x;coord_y;' + \
                ';'.join([k for k, v in self.properties.iteritems()]) + '\n'
            data += ';'.join([str(_) for _ in self.coordinates]) + ';'
            data += ';'.join([v for k, v in self.properties.iteritems()])
        else:
            data += ';'.join([str(_) for _ in self.coordinates])
        path = kwargs.get('path', None)
        if not path:
            path = '.'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = kwargs.get('filename', None)
        if not filename:
            filename = 'Point'
        with open(path + '/' + filename + '.txt', 'w') as outfile:
            outfile.write(data)
        return self

    def to_csv(self, **kwargs):
        data = [['coord_x', 'coord_y'], [_ for _ in self.coordinates]]
        if self.properties:
            for k, v in self.properties.iteritems():
                data[0].append(k)
                data[1].append(v)
        else:
            data = [_ for _ in self.coordinates]
        path = kwargs.get('path', None)
        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            filename = kwargs.get('filename', None)
            if not filename:
                filename = 'Point'
            with open(path + '/' + filename + '.csv', 'w') as outfile:
                writer = csv.writer(outfile, delimiter=';', quotechar='"')
                writer.writerows(data)
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
