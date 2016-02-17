# Introduction #

Finding the path

Finding the right Spherical Mercartor Projection

# Details #

Finding the right Spherical Mercartor Projection

Get this:
http://spatialreference.org/ref/sr-org/6627/postgis/

Change the proj4text definition.  Swap out the following string:

```
'+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs '
```
to
```
"+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs"
```

Then, swap out all instances of the number 6627 to 900913

So your finished sql command should look like this:

```
INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 900913, 'sr-org', 900913, '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs', 'PROJCS["Google Mercator",GEOGCS["WGS 84",DATUM["World Geodetic System 1984",SPHEROID["WGS 84",6378137.0,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0.0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.017453292519943295],AXIS["Geodetic latitude",NORTH],AXIS["Geodetic longitude",EAST],AUTHORITY["EPSG","4326"]],PROJECTION["Mercator_1SP"],PARAMETER["semi_minor",6378137.0],PARAMETER["latitude_of_origin",0.0],PARAMETER["central_meridian",0.0],PARAMETER["scale_factor",1.0],PARAMETER["false_easting",0.0],PARAMETER["false_northing",0.0],UNIT["m",1.0],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","900913"]]');
```

Then, go into the database:

psql djangonewsroom

and paste the command above.


---


add the following line to /usr/share/gdal/cubewerx\_extra.wkt

```
900913,PROJCS["Google Maps Global Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Mercator_2SP"],PARAMETER["standard_parallel_1",0],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs"]]
```