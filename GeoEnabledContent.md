# Introduction #

The goal of this page is to present the geographic information that a user could add to its content (Story, ...) and the different implementations.
First of all let us define what is **geographic information**, in this document this expression will be used to represent the following kind of information :
  * Point : It can be used to represent a particular point on a map. It is usually represented by longitude, latitude, projection and/or address (see below)
  * Line : It can be used to represent a trail on a map. It is a set of Points
  * Polygon : it can be used to represent a area on a map. It is a closed line.

If the simplest way to define a line and a polygon is probably to draw it on a map the question is a bit more open for Point. I see 3 ways to define a point on a map :
  * the user can click on a map. This information will then be converted as Lat/Lon.
  * enter an address and use a [geocoder](http://code.google.com/p/geopy/) to define the lat/Lon in the background.
  * enter an address and use a [geocoder](http://code.google.com/p/geopy/) to move the the map to the area of interest then the user will be able to select the Point.
The last approach is a mix of the first 2 and is particularly interesting because the geocoder are not always accurate. However this lead to a question : "Which information do you want to save the database ?" Do we want to keep : Lat/Long or the address or both.

# what for ? #

Once we have this geographic information we need to define what do we want to do with it. The first use case and probably the more obvious is to display it somewhere on the detail page of the object. i.e On the detail page of a Story we could have a map localizing it.
Then we could also setup a "geo search" on the public web site in order to search for content located in a particular zone of interest. A similar service could also be provided on a subscription based :  "I want to receive every day/week all the content located in my zone of interest"


# Implementations #

I see 2 alternatives possible in order to store the geographic information.
**dedicated application related to the other django application by a generic relation. [geotagging](https://launchpad.net/django-geotagging) is an example of this approach** Add geo attributes (Point, Line, Polygon) to all the django application we want to "geo enabled"

# Open Questions #

  * which geographic information do we want to manage ? Address, Point, Line, Polygon
  * which Map do we want to use? Google map, Open street map
  * Do we need [geodjango](http://geodjango.org/docs/) (spatial query) ?