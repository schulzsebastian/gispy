import json
from pyproj import Proj, transform


class Point(object):

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __str__(self):
        return "Point object: %s" % self.coordinates

    def coords(self):
        return self.coordinates

    def reproject(self, in_epsg, out_epsg):
        in_proj = Proj(init="epsg:" + str(in_epsg))
        out_proj = Proj(init="epsg:" + str(out_epsg))
        x, y = self.coordinates[0], self.coordinates[1]
        return Point([i for i in transform(in_proj, out_proj, x, y)])

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
            with open(path + '/Point.geojson', 'w') as outfile:
                json.dump(data, outfile, indent=4,
                          sort_keys=True, separators=(',', ':'))
        return json.dumps(data)
