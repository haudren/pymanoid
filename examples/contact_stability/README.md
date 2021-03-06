# Contact-stability conditions

<img align="right" src="../../doc/source/images/static_equilibrium_polygon.png" width="300" />
    
Contact-stability areas and volumes are conditions used to prevent contacts
from slipping or detaching during motion. These examples illustrate the
static-equilibrium COM polygon, multi-contact ZMP support areas and the 3D cone
of COM accelerations.

## COM static-equilibrium polygon

This example illustrates the polygon of COM positions that the robot can hold
in static equilibirum, which was derived in [this
paper](https://doi.org/10.1109/TRO.2008.2001360). You can move contacts by
selecting them in the OpenRAVE GUI. Contact wrenches are computed at each
contact to support the robot in static-equilibrium. Try moving the blue box (in
the plane above the robot) around, and see what happens when it exits the
polygon.

## Multi-contact ZMP support areas

This example displays the ZMP support area under a given set of contacts. The
derivation of this area is detailed in [this
paper](https://scaron.info/research/tro-2016.html). It depends on both contact
locations and the position of the center of mass, so when you move it or its
projection (blue box) you will see the blue area change as well.

## COM acceleration cones

When the robot regulates its angular momentum, it can only produce a certain
set of COM accelerations under given contacts. This set is actually a 3D cone,
as derived in [this paper](https://scaron.info/research/humanoids-2016.html).
Like ZMP support areas, this cone depends on both contact locations and the
position of the center of mass, so that when you move it or its projection
(blue box) you will see its shape change as well.
