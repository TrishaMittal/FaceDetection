'''
Created on 11-Nov-2013

@author: raghavan
'''
import math
from pyimage import PyImage

class Color(object):
    '''
    classdocs
    '''


    def __init__(self, rgb):
        '''
        Precompute and keep the normalized values for r, g and b calculated from the raw rgb values given in the argument rgb.
        Raw rgb - (R, G, B) where all three are integers in the range 0-255
        Also have the total raw RGB in case you want to recover the raw rgb values
        The other attribute (apart from total, and normalized rgb values) you would need is intensity - total/3
        '''
        # Your code
        self.total = (rgb[0] + rgb[1] + rgb[2])
        if rgb == (0, 0, 0):
            self.R = self.G = self.B =  (1.0/math.sqrt(3))
        else:
            self.R = rgb[0] / (self.total*1.0) 
            self.G = rgb[1] / (self.total*1.0)
            self.B = rgb[2] / (self.total*1.0 )
        self.RGB=(rgb[0], rgb[1], rgb[2])
        self.intensity = self.total / 3.0

    def hue(self):
        '''
        Return the hue in radians - calculated as atan((sqrt(3)*(green-blue))/((red-green) + (red-blue)))
        The color values in the formula are the normalized color values
        You need to check if the denominator is zero and if it is return the appropriate value for the atan.
        '''
        # Your code
        if ((self.R - self.G) + (self.R - self.B)) == 0:
            return math.pi/2.0
        return math.atan((math.sqrt(3)*(self.G - self.B))/((self.R - self.G) + (self.R - self.B))*1.0)

    def hue_degrees(self):
        '''
        Return the hue in degrees
        '''
        # Your code
       
        return self.hue() * (180.0/math.pi)

    def rgb_abs(self):
        '''
        Recover and return the raw RGB values as a triple of integers
        '''
        # Your code
        return self.RGB
   
