#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2017 Stephane Caron <stephane.caron@lirmm.fr>
#
# This file is part of pymanoid <https://github.com/stephane-caron/pymanoid>.
#
# pymanoid is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# pymanoid is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pymanoid. If not, see <http://www.gnu.org/licenses/>.

"""
This example shows three contact-stability conditions: the static-equilibrium
COM polygon, the dynamic ZMP support area, and the 3D COM acceleration cone.
See <https://scaron.info/research/tro-2016.html> for details.
"""

import IPython

from numpy import zeros

import pymanoid

from pymanoid import Stance
from pymanoid.gui import PointMassWrenchDrawer
from pymanoid.gui import draw_polygon
from pymanoid.misc import matplotlib_to_rgb, norm

com_height = 0.9  # [m]
z_polygon = 2.


class SupportPolygonDrawer(pymanoid.Process):

    """
    Draw the static-equilibrium polygon of a contact set.

    Parameters
    ----------
    stance : Stance
        Contacts and COM position of the robot.
    z : scalar, optional
        Altitude of drawn area in the world frame.
    color : tuple or string, optional
        Area color.
    """

    def __init__(self, stance, z=0., color=None):
        if color is None:
            color = (0., 0.5, 0., 0.5)
        if type(color) is str:
            color = matplotlib_to_rgb(color) + [0.5]
        super(SupportPolygonDrawer, self).__init__()
        self.color = color
        self.contact_poses = {}
        self.handle = None
        self.stance = stance
        self.z = z
        #
        self.update_contact_poses()
        self.update_polygon()

    def clear(self):
        self.handle = None

    def on_tick(self, sim):
        if self.handle is None:
            self.update_polygon()
        for contact in self.stance.contacts:
            if norm(contact.pose - self.contact_poses[contact.name]) > 1e-10:
                self.update_contact_poses()
                self.update_polygon()
                break

    def update_contact_poses(self):
        for contact in self.stance.contacts:
            self.contact_poses[contact.name] = contact.pose

    def update_polygon(self):
        self.handle = None
        try:
            vertices = self.stance.compute_static_equilibrium_polygon()
            self.handle = draw_polygon(
                [(x[0], x[1], self.z) for x in vertices],
                normal=[0, 0, 1], color=self.color)
        except Exception as e:
            print "SupportPolygonDrawer:", e

    def update_z(self, z):
        self.z = z
        self.update_polygon()


class StaticWrenchDrawer(PointMassWrenchDrawer):

    """
    Draw contact wrenches applied to a robot in static-equilibrium.

    Parameters
    ----------
    stance : Stance
        Contacts and COM position of the robot.
    """

    def __init__(self, stance):
        super(StaticWrenchDrawer, self).__init__(stance.com, stance)
        stance.com.pdd = zeros((3,))
        self.stance = stance

    def find_supporting_wrenches(self, sim):
        return self.stance.find_static_supporting_wrenches()


class COMSync(pymanoid.Process):

    def __init__(self, stance, com_above):
        super(COMSync, self).__init__()
        self.com_above = com_above
        self.stance = stance

    def on_tick(self, sim):
        self.stance.com.set_x(self.com_above.x)
        self.stance.com.set_y(self.com_above.y)


if __name__ == "__main__":
    sim = pymanoid.Simulation(dt=0.03)
    robot = pymanoid.robots.JVRC1('JVRC-1.dae', download_if_needed=True)
    sim.set_viewer()
    sim.viewer.SetCamera([
        [0.60587192, -0.36596244,  0.70639274, -2.4904027],
        [-0.79126787, -0.36933163,  0.48732874, -1.6965636],
        [0.08254916, -0.85420468, -0.51334199,  2.79584694],
        [0.,  0.,  0.,  1.]])
    robot.set_transparency(0.25)

    com_above = pymanoid.Cube(0.02, [0.05, 0.04, z_polygon], color='b')

    stance = Stance.from_json('../stances/double.json')
    stance.bind(robot)
    robot.ik.solve()

    com_sync = COMSync(stance, com_above)
    polygon_drawer = SupportPolygonDrawer(stance, z_polygon)
    wrench_drawer = StaticWrenchDrawer(stance)

    sim.schedule(robot.ik)
    sim.schedule_extra(com_sync)
    sim.schedule_extra(polygon_drawer)
    sim.schedule_extra(wrench_drawer)
    sim.start()

    print """
COM static-equilibrium polygon
==============================

Ready to go! The GUI displays the COM static-equilibrium polygon in green. You
can move the blue box (in the plane above the robot) around to make the robot
move its center of mass. Contact wrenches are displayed at each contact (green
dot is COP location, arrow is resultant force). When the COM exists the
static-equilibrium polygon, you should see the background turn red as no
feasible contact wrenches can be found.

Enjoy :)
"""

    if IPython.get_ipython() is None:
        IPython.embed()
