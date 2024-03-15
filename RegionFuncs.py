import numpy as np




class Circle():

    radius = 0


    def __init__(self, radius):

        self.radius = radius

    
    def is_in_region(self, xPos, yPos):

        return np.sqrt(xPos**2 + yPos**2) < self.radius
    



class Square():
    
    xRange = 0
    yRange = 0


    def __init__(self, xRange, yRange):

        self.xRange = xRange
        self.yRange = yRange

    
    def is_in_region(self, xPos, yPos):

        return np.abs(xPos) < self.xRange and np.abs(yPos) < self.yRange
    



class Slit():
    
    xRange = 0


    def __init__(self, xRange):

        self.xRange = xRange

    
    def is_in_region(self, xPos, yPos):

        return np.abs(xPos) < self.xRange