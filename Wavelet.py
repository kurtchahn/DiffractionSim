import numpy as np




class Huygens():

    wavenumber = 0


    def __init__(self, wavenumber):

        self.wavenumber = wavenumber

    
    def return_field(self, xPos, yPos, zPos, xAperture, yAperture):

        distance = np.sqrt((xPos-xAperture)**2 + (yPos-yAperture)**2 + zPos**2)
        field = -1j * self.wavenumber * np.exp(1j * self.wavenumber * distance) / (2 * np.pi * distance)

        return field
    



class Fresnel():

    wavenumber = 0


    def __init__(self, wavenumber):

        self.wavenumber = wavenumber

    
    def return_field(self, xPos, yPos, zPos, xAperture, yAperture):

        coefficient = (-1j * self.wavenumber) / (2 * np.pi * zPos)

        exponent1 = 1j * self.wavenumber * zPos
        exponent2 = (1j * self.wavenumber * (xPos**2+yPos**2)) / (2 * zPos)
        exponent3 = (-1j * self.wavenumber * (xPos*xAperture+yPos*yAperture)) / zPos
        exponent4 = (1j * self.wavenumber * (xAperture**2+yAperture**2)) / (2 * zPos)

        field = coefficient * np.exp(exponent1+exponent2+exponent3+exponent4)

        return field
    



class Fraunhofer():

    wavenumber = 0


    def __init__(self, wavenumber):

        self.wavenumber = wavenumber


    def return_field(self, xPos, yPos, zPos, xAperture, yAperture):

        coefficient = (-1j * self.wavenumber) / (2 * np.pi * zPos)

        exponent1 = 1j * self.wavenumber * zPos
        exponent2 = (1j * self.wavenumber * (xPos**2+yPos**2)) / (2 * zPos)
        exponent3 = (-1j * self.wavenumber * (xPos*xAperture+yPos*yAperture)) / zPos

        field = coefficient * np.exp(exponent1+exponent2+exponent3)

        return field