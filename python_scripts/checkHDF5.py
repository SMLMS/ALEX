'''######################################################################
# File Name:
# Project:
# Version:
# Creation Date:
# Created By:
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import phconvert


class checkHDF5():
    def __init__(self, filename):
        self._filename = filename
        phconvert.hdf5.assert_valid_photon_hdf5
        phconvert.hdf5.assert_valid_photon_hdf5(self._filename,
                                                warnings=True,
                                                verbose=True,
                                                strict_description=True,
                                                require_setup=True,
                                                skip_measurement_specs=False)