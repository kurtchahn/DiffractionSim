import numpy as np
import matplotlib.pyplot as plt

import GaussianBeam
import Wavelet

import sys




class Obstacle():
    """
    Input values in meters \n
    xRange, yRange provide a rectangle significantly larger than aperture \n
    recommend 10x \n
    ----------------------
    Simulates diffraction pattern for circular obstacle \n
    Assume use of Gaussian beam
    """

    waistRadius = 0
    wavelength = 0
    
    xRange = 0
    yRange = 0

    obstacleFunction = None

    def __init__(self, waistRadius, wavelength, xRange, yRange, obstacleFunction):

        self.waistRadius = waistRadius
        self.wavelength = wavelength
        self.xRange = xRange
        self.yRange = yRange
        self.obstacleFunction = obstacleFunction
    

    def return_figure_incident_intensity(self, numberPoints, yAperture=0):
        """
        yAperture value in meters \n
        -------------------------
        Returns figure of incident gaussian beam intensity along x \n
        """

        xAperture = np.linspace(-3*self.waistRadius, 3*self.waistRadius, numberPoints)
        
        intensities = np.abs( GaussianBeam.return_incident_field(xAperture, yAperture, self.waistRadius) )**2
        intensitiesPlaneWave = ( GaussianBeam.return_incident_field(xAperture, yAperture, 10*self.waistRadius) )**2
        
        figure = plt.figure(0, figsize=(6,4))
        ax = figure.add_axes([0.1, 0.3, 0.8, 0.6])

        xAperture *= 1000 # mm / m

        ax.plot(xAperture, intensities, color="blue", label=f"Gaussian Beam, w = {self.waistRadius*1000} mm")
        ax.plot(xAperture, intensitiesPlaneWave, color="orange", label=f"Approximated Plane Wave, w = {10*self.waistRadius*1000} mm")
        ax.set_xlabel("Position Along Aperture (mm)")
        ax.set_ylabel(r"$I\propto\left|E\right|^2$")
        ax.set_xlim(xAperture[0], xAperture[-1])
        ax.set_ylim(0, 1.1)
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.5))
        ax.grid()
        ax.set_title(r"Gaussian Beam Intensity at Aperture ($z=0$)")

        return figure


    def return_total_field(self, xPos, yPos, zPos, wavletType, numberPoints):
        """
        Input values in meters \n
        waveletType takes str 'Huygens', 'Fresnel', 'Fraunhofer' \n
        --------------------------------------------------------
        Returns total field at point
        """

        xAperture = np.linspace(-self.xRange, self.xRange, numberPoints)
        yAperture = np.linspace(-self.yRange, self.yRange, numberPoints)

        dx = np.abs(xAperture[0] - xAperture[1])
        dy = np.abs(yAperture[0] - yAperture[1])

        xAperture, yAperture = np.meshgrid(xAperture, yAperture)

        positionsAperture = self.obstacleFunction(xAperture, yAperture)
        incidentField = GaussianBeam.return_incident_field(xAperture, yAperture, self.waistRadius)

        wavenumber = 2*np.pi / self.wavelength
        waveletField = None

        match wavletType:

            case "Huygens":
                wavelet = Wavelet.Huygens(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case "Fresnel":
                wavelet = Wavelet.Fresnel(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case "Fraunhofer":
                wavelet = Wavelet.Fraunhofer(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case _:
                raise Exception("Invalid Wavelet Type")
        

        fields = (1 - positionsAperture) * incidentField * waveletField * dx * dy
        totalField = np.sum(fields)

        return totalField
    

    def return_figure_total_intensity(self, xPositions, yPos, zPos, waveletType, numberPoints):
        """
        Input values in meters \n
        xPositions is an array of x positions \n
        waveletType takes str 'Huygens', 'Fresnel', 'Fraunhofer' \n
        --------------------------------------------------------
        Returns figure of normalized intensity along x (diffraction pattern)
        """

        intensities = []
        for xPos in xPositions:

            intensity = np.abs( self.return_total_field(xPos, yPos, zPos, waveletType, numberPoints) )**2
            intensities.append(intensity)


        intensities = np.array(intensities)
        intensities /= np.max(intensities)

        figure = plt.figure(0, figsize=(6,4))
        ax = figure.add_axes([0.1, 0.3, 0.8, 0.6])

        xPositions *= 1000 # mm / m

        ax.plot(xPositions, intensities, color="blue")
        ax.set_xlabel(r"Screen Position Along  $x$ (mm)")
        ax.set_ylabel(r"Normalized Intensity $\frac{I}{I_0}$")
        ax.set_xlim(xPositions[0], xPositions[-1])
        ax.set_ylim(0, 1.1)
        ax.grid()
        ax.set_title(f"Normalized Diffraction Pattern from Obstacle, y={yPos} m, z={zPos} m")

        return figure




class Aperture():
    """
    Input values in meters \n
    xRange, yRange provide a rectangle covering entire aperture \n
    ----------------------------------------------------
    Simulates diffraction pattern for aperture \n
    Assume use of Gaussian beam
    """

    waistRadius = 0
    wavelength = 0

    xRange = 0
    yRange = 0

    apertureFunction = None


    def __init__(self, waistRadius, wavelength, xRange, yRange, apertureFunction):

        self.waistRadius = waistRadius
        self.wavelength = wavelength
        self.xRange = xRange
        self.yRange = yRange
        self.apertureFunction = apertureFunction
    

    def return_figure_incident_intensity(self, numberPoints, yAperture=0):
        """
        yAperture value in meters \n
        -------------------------
        Returns figure of incident gaussian beam intensity along x \n
        """

        xAperture = np.linspace(-3*self.waistRadius, 3*self.waistRadius, numberPoints)
        
        intensities = np.abs( GaussianBeam.return_incident_field(xAperture, yAperture, self.waistRadius) )**2
        intensitiesPlaneWave = ( GaussianBeam.return_incident_field(xAperture, yAperture, 10*self.waistRadius) )**2
        
        figure = plt.figure(0, figsize=(6,4))
        ax = figure.add_axes([0.1, 0.3, 0.8, 0.6])

        xAperture *= 1000 # mm / m

        ax.plot(xAperture, intensities, color="blue", label=f"Gaussian Beam, w = {self.waistRadius*1000} mm")
        ax.plot(xAperture, intensitiesPlaneWave, color="orange", label=f"Approximated Plane Wave, w = {10*self.waistRadius*1000} mm")
        ax.set_xlabel("Position Along Aperture (mm)")
        ax.set_ylabel(r"$I\propto\left|E\right|^2$")
        ax.set_xlim(xAperture[0], xAperture[-1])
        ax.set_ylim(0, 1.1)
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.5))
        ax.grid()
        ax.set_title(r"Gaussian Beam Intensity at Aperture ($z=0$)")

        return figure
    

    def return_total_field(self, xPos, yPos, zPos, wavletType, numberPoints):
        """
        Input values in meters \n
        waveletType takes str 'Huygens', 'Fresnel', 'Fraunhofer' \n
        --------------------------------------------------------
        Returns total field at point
        """

        xAperture = np.linspace(-self.xRange, self.xRange, numberPoints)
        yAperture = np.linspace(-self.yRange, self.yRange, numberPoints)

        dx = np.abs(xAperture[0] - xAperture[1])
        dy = np.abs(yAperture[0] - yAperture[1])

        xAperture, yAperture = np.meshgrid(xAperture, yAperture)

        positionsAperture = self.apertureFunction(xAperture, yAperture)
        incidentField = GaussianBeam.return_incident_field(xAperture, yAperture, self.waistRadius)

        wavenumber = 2*np.pi / self.wavelength
        waveletField = None

        match wavletType:

            case "Huygens":
                wavelet = Wavelet.Huygens(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case "Fresnel":
                wavelet = Wavelet.Fresnel(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case "Fraunhofer":
                wavelet = Wavelet.Fraunhofer(wavenumber)
                waveletField = wavelet.return_field(xPos, yPos, zPos, xAperture, yAperture)
            case _:
                raise Exception("Invalid Wavelet Type")
        

        fields = positionsAperture * incidentField * waveletField * dx * dy
        totalField = np.sum(fields)

        return totalField
    

    def return_figure_total_intensity(self, xPositions, yPos, zPos, waveletType, numberPoints):
        """
        Input values in meters \n
        xPositions is an array of x positions \n
        waveletType takes str 'Huygens', 'Fresnel', 'Fraunhofer' \n
        --------------------------------------------------------
        Returns figure of normalized intensity along x (diffraction pattern)
        """

        intensities = []
        for xPos in xPositions:

            intensity = np.abs( self.return_total_field(xPos, yPos, zPos, waveletType, numberPoints) )**2
            intensities.append(intensity)


        intensities = np.array(intensities)
        intensities /= np.max(intensities)

        figure = plt.figure(0, figsize=(6,4))
        ax = figure.add_axes([0.1, 0.3, 0.8, 0.6])

        xPositions *= 1000 # mm / m

        ax.plot(xPositions, intensities, color="blue")
        ax.set_xlabel(r"Screen Position Along  $x$ (mm)")
        ax.set_ylabel(r"Normalized Intensity $\frac{I}{I_0}$")
        ax.set_xlim(xPositions[0], xPositions[-1])
        ax.set_ylim(0, 1.1)
        ax.grid()
        ax.set_title(f"Normalized Diffraction Pattern from Aperture, y={yPos} m, z={zPos} m")

        return figure