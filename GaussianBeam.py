import numpy as np



def return_incident_field(xPos, yPos, waistRadius):

    field = np.exp(-(xPos**2 + yPos**2) / waistRadius**2)

    return field