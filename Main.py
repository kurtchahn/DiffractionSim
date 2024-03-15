import numpy as np
import matplotlib.pyplot as plt

import Simulation
import RegionFuncs




NUMBERPOINTS = 257
WAVELENGTH = 632.8e-9

SLITWIDTH = (0.040) * (25.4/1000) # m


def main():

    aperture = RegionFuncs.Slit(SLITWIDTH/2)

    xPositions = np.linspace(-0.004, 0.004, NUMBERPOINTS)

    sim = Simulation.Aperture(waistRadius=5e-3,
                              wavelength=WAVELENGTH,
                              xRange=SLITWIDTH/2,
                              yRange=10*SLITWIDTH,
                              apertureFunction=aperture.is_in_region)
    

    diffractionPattern = sim.return_figure_total_intensity(xPositions=xPositions,
                                                           yPos=0,
                                                           zPos=540e-3,
                                                           waveletType="Fresnel",
                                                           numberPoints=NUMBERPOINTS)



if __name__ == "__main__":

    main()
    plt.show()