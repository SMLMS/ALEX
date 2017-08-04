'''######################################################################
# File Name: makeHDF5.py
# Project:
# Version:
# Creation Date: 2017/04/11
# Created By: Karoline
# Company: Goethe University of Frankfurt
# Institute: Institute of Physical and Theoretical Chemistry
# Department: Single Molecule Biophysics
# License: GPL3
#####################################################################'''
import phconvert as phc
phc.__version__


class makeHDF5():
    def __init__(self, dictionary, data, filename):
        self._dict = dictionary
        self._data = data
        self._filename = filename + '.hf5'
        self.makeFile()

    def makeFile(self):
        timestamps = self._data         # data goes here, ndarray
        timestamps.sort()
        timestamps_unit = self._dict.getitem("timestamps_unit")     # 10 ns, units are always S.I.

        detectors = self._dict.getitem("detectors")

        description = self._dict.getitem("description")

        author = self._dict.getitem("author")
        author_affiliation = self._dict.getitem("author_affiliation")

        sample_name = self._dict.getitem("sample_name")
        buffer_name = self._dict.getitem("buffer_name")
        dye_names = self._dict.getitem("dye_names")   # Comma separates names of fluorophores

        photon_data = dict(
            timestamps=timestamps,
            detectors=detectors,
            timestamps_specs={'timestamps_unit': timestamps_unit})

        setup = dict(
            # Mandatory fields
            num_pixels=2,                   # using 2 detectors
            num_spots=1,                    # a single confocal excitation
            num_spectral_ch=2,              # donor and acceptor detection
            num_polarization_ch=1,          # no polarization selection
            num_split_ch=1,                 # no beam splitter
            modulated_excitation=False,     # CW excitation, no modulation
            lifetime=False,                 # no TCSPC in detection

            # Optional fields
            excitation_wavelengths=[532e-9, 640e-9],            # List of excitation wavelenghts
            excitation_cw=[True],                               # List of booleans, True if wavelength is CW
            detection_wavelengths=[580e-9, 640e-9],             # Nominal center wavelength each for detection ch
        )

        provenance = dict(
            filename='raw data',
            software='Karolines Projekt')

        identity = dict(
            author=author,
            author_affiliation=author_affiliation)

        measurement_specs = dict(
            measurement_type='smALEX',
            detectors_specs={'spectral_ch1': [0],            # list of donor's detector IDs
                             'spectral_ch2': [1]}            # list of acceptor's detector IDs
        )

        photon_data['measurement_specs'] = measurement_specs

        data = dict(
            description=description,
            photon_data=photon_data,
            setup=setup,
            identity=identity,
            provenance=provenance
        )

        phc.hdf5.save_photon_hdf5(data, h5_fname=self._filename, overwrite=True)
