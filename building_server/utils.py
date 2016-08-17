# -*- coding: utf-8 -*-


class Box3D(object):

    def __init__(self, str):
        self.str = str

    def aslist(self):
        return "[" + self.str[6:len(self.str)-1].replace(" ", ",") + "]"

    def geojson(self):
        p = Property("bbox", self.aslist())
        return p.geojson()


class Property(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def geojson(self):
        return '"{0}" : {1}'.format(self.name, self.value)


class PropertyCollection(object):

    def __init__(self):
        self.properties = []

    def add(self, property):
        self.properties.append(property)

    def geojson(self):
        json = ""

        for property in self.properties:
            if json:
                json = "{0}, {1}".format(json, property.geojson())
            else:
                json = property.geojson()

        json = '"properties" : {{{0}}}'.format(json)

        return json


class Feature(object):

    def __init__(self, id, properties, geometry):
        self.id = id
        self.properties = properties
        self.geometry = geometry

    def geojson(self):
        json = ('{{ {0}, {1}, {2}, {3} }}'
                .format(self._geojson_type(), self._geojson_id(),
                        self._geojson_properties(), self._geojson_geometry()))
        return json

    def _geojson_type(self):
        return '"type" : "Feature"'

    def _geojson_id(self):
        return '"id" : "lyongeom.{0}"'.format(self.id)

    def _geojson_properties(self):
        return self.properties.geojson()

    def _geojson_geometry(self):
        return '"geometry" : {0}'.format(self.geometry)


class FeatureCollection(object):

    def __init__(self):
        self.features = []
        self.epsg = 3946

    def add(self, feature):
        self.features.append(feature)

    def geojson(self):
        json = ('{{ {0}, {1}, {2} }}'
                .format(self._geojson_type(), self._geojson_crs(),
                        self._geojson_features()))
        return json

    def _geojson_type(self):
        return '"type" : "FeatureCollection"'

    def _geojson_crs(self):
        json = ('"crs" : {{ "type" : "name",'
                '"properties" : {{"name" : "EPSG{0}"}}}}'
                .format(self.epsg))
        return json

    def _geojson_features(self):
        json = ""

        for feature in self.features:
            if json:
                json = "{0}, {1}".format(json, feature.geojson())
            else:
                json = feature.geojson()

        json = '"features" : [{0}]'.format(json)

        return json
