# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Updated for python 3
#
# Used macports to install
#  python36
#  py36-numpy
#  py36-readline
#  py36-tkinter
#
# CS 251
# Spring 2019
# Eli Decker
# Project 4

import tkinter as tk
import os
import math
import random
import numpy as np

class View:
    """create a class to build and manage the display"""
    def __init__(self):
        self.reset()

    def reset(self):
            """ Sets the default values for the view. """
            self.vrp = np.matrix([0.5, 0.5, 1])
            self.vpn = np.matrix([0, 0, -1])
            self.vup = np.matrix([0, 1, 0])
            self.u = np.matrix([-1, 0, 0])
            self.extent = [1., 1., 1.]
            self.screen = [400., 400.]
            self.offset = [20., 20.]

    def build(self):
        """Returns a view matrix given the current viewing parameters"""
        # Generate a 4x4 identity matrix, which will be the basis for the view matrix.
        vtm = np.identity( 4, float )
        # Generate a translation matrix to move the VRP to the origin and then premultiply the vtm by the translation matrix.
        t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
                    [0, 1, 0, -self.vrp[0, 1]],
                    [0, 0, 1, -self.vrp[0, 2]],
                    [0, 0, 0, 1] ] )

        vtm = t1 * vtm

        # Calculate the view reference axes tu, tvup, tvpn.
        tu = np.cross(self.vup, self.vpn)
        tvup = np.cross(self.vpn, tu)
        tvpn = self.vpn.copy()

        # Normalize the view axes tu, tvup, and tvpn to unit length.

        # if this doesn't work, create my own normalize function
        tu = self.normalize(tu)
        tvup = self.normalize(tvup)
        tvpn = self.normalize(tvpn)

        # Copy the orthonormal axes tu, tvup, and tvpn back to self.u, self.vup and self.vpn.
        self.u = tu.copy()
        self.vup = tvup.copy()
        self.vpn = tvpn.copy()

        # Use the normalized view reference axes to generate the rotation matrix 
        # to align the view reference axes and then premultiply M by the rotation.
        r1 = np.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
                    [ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
                    [ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )

        vtm = r1 * vtm

        # Translate the lower left corner of the view space to the origin.
        # extent of the view volume in the X and Y view axes.
        vtm = self.T( 0.5*self.extent[0], 0.5*self.extent[1], 0 ) * vtm

        vtm = self.S( -self.screen[0] / self.extent[0], -self.screen[1] / self.extent[1], 1.0 / self.extent[2] ) * vtm

        vtm = self.T( self.screen[0] + self.offset[0], self.screen[1] + self.offset[1], 0 ) * vtm

        return vtm

    
    def T(self, tx, ty, tz):
        t1 = np.matrix( [[ 1.0, 0.0, 0.0, tx ],
                    [ 0.0, 1.0, 0.0, ty ],
                    [ 0.0, 0.0, 1.0, tz ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        return t1
    def S(self, tx, ty, tz):
        s1 = np.matrix( [[ tx, 0.0, 0.0, 0.0 ],
                    [ 0.0, ty, 0.0, 0.0 ],
                    [ 0.0, 0.0, tz, 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        return s1

    def normalize(self, vec):
        """Returns a normalized vector."""
        length = math.sqrt( vec[0,0]*vec[0,0] + vec[0,1]*vec[0,1] + vec[0,2]*vec[0,2] )
        vnorm = vec / length
        return vnorm

    # Create a clone method for your View object that makes a duplicate View object and returns it. 
    def clone(self):
        copy = View()
        copy.vrp = self.vrp.copy()
        copy.vpn = self.vpn.copy()
        copy.vup = self.vup.copy()
        copy.u = self.u.copy()
        copy.extent = self.extent[:]
        copy.screen = self.screen[:]
        copy.offset = self.offset[:]
        return copy

    def rotateVRC(self, vupAngle, uAngle):
        """The two angles are how much to rotate about the VUP axis and how much to rotate about the U axis. 
        The process you want to follow is to translate the center of rotation (the middle of the extent volume) 
        to the origin, rotate around the Y axis, rotate around the X axis, then translate 
        back by the opposite of the first translation."""

        # Make a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin. Put it in t1.
        t1 = np.matrix( [[1.0, 0.0, 0.0, -1*( self.vrp[0,0] + self.vpn[0,0] * self.extent[2] * 0.5 )],
                    [0.0, 1.0, 0.0, -1*( self.vrp[0,1] + self.vpn[0,1] * self.extent[2] * 0.5 )],
                    [0.0, 0.0, 1.0, -1*( self.vrp[0,2] + self.vpn[0,2] * self.extent[2] * 0.5 )],
                    [0.0, 0.0, 0.0, 1.0] ] )
        # Make an axis alignment matrix Rxyz using u, vup and vpn.
        Rxyz = np.matrix( [[ self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0 ],
                    [ self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0 ],
                    [ self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        # Make a rotation matrix about the Y axis by the VUP angle, put it in r1.
        r1 = np.matrix( [[ np.cos(vupAngle), 0.0, np.sin(vupAngle), 0.0 ],
                    [ 0.0, 1.0, 0.0, 0.0 ],
                    [ -1*np.sin(vupAngle), 0.0, np.cos(vupAngle), 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        # Make a rotation matrix about the X axis by the U angle. Put it in r2.
        r2 = np.matrix( [[ 1.0, 0.0, 0.0, 0.0 ],
                    [ 0.0, np.cos(uAngle), -1*np.sin(uAngle), 0.0 ],
                    [ 0.0, np.sin(uAngle), np.cos(uAngle), 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        # Make a translation matrix that has the opposite translation from step 1.
        t2 = np.matrix( [[1, 0, 0, ( self.vrp[0,0] + self.vpn[0,0] * self.extent[2] * 0.5 )],
                    [0, 1, 0, ( self.vrp[0,1] + self.vpn[0,1] * self.extent[2] * 0.5 )],
                    [0, 0, 1, ( self.vrp[0,2] + self.vpn[0,2] * self.extent[2] * 0.5 )],
                    [0, 0, 0, 1] ] )
        # Make a numpy matrix where the VRP is on the first row, with a 1 in the homogeneous coordinate, 
        # and u, vup, and vpn are the next three rows, with a 0 in the homogeneous coordinate.
        tvrc = np.matrix( [[ self.vrp[0, 0], self.vrp[0, 1], self.vrp[0, 2], 1.0 ],
                    [ self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0 ],
                    [ self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0 ],
                    [ self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ] ] )
        # Execute the following: tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
        tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
        # Then copy the values from tvrc back into the VPR, U, VUP, and VPN fields and normalize U, VUP, and VPN.
        self.vrp = tvrc[0,0:3]
        self.u = tvrc[1,0:3]
        self.vup = tvrc[2,0:3]
        self.vpn = tvrc[3,0:3]

        #normalize
        self.u = self.normalize(self.u)
        self.vup = self.normalize(self.vup)
        self.vpn = self.normalize(self.vpn)




    def main(self):
        print( 'Entering main loop')

        print(self.build())

