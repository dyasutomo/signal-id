# Generate and manipulate three-d Boolean arrays for purposes of
# signal identification.

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# IMPORTS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

# python
import time
import copy

# numpy, scipy, Matplotlib
import numpy as np

import matplotlib.pyplot as plt

from scipy.ndimage import histogram
from scipy.ndimage import binary_dilation
from scipy.ndimage import binary_erosion
from scipy.ndimage import label, find_objects

# astropy

# radio tools
from spectral_cube import SpectralCube, SpectralCubeMask, read

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# BASE CLASS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

class RadioMask(object):
    """
    Holds a binary array with associated metadata.
    """
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Attributes and Properties
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    
    # Current version of the array
    _value = None    

    # Previous version of the array
    _backup = None

    # Toggles 
    _implicit_backup = True
    
    # The associated cube
    _linked_data = None

    # TBD: noise

    # TBD: beam

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Construction
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def __init__(
        self,
        data=None,
        thresh=None
        ):

        if isinstance(data, SpectralCube):
                self.from_spec_cube(data, thresh=thresh)

        if isinstance(data, str):
            self.from_file(data)

        if isinstance(data, np.ndarray):
            self.from_array(data)

    def from_file(self, fname, thresh=None):
        cube = read(fname)
        self.from_spec_cube(cube, thresh=None)
        
    def from_spec_cube(self, cube, thresh=None):
        self._linked_data = cube
        self._value = cube._mask.include
        if thresh is not None:
            self._value *= cube > thresh

    def from_array(self, array, thresh=None):
        self._linked_data = array
        self._value = np.isfinite(array)
        if thresh is not None:
            self._value *= cube > thresh        

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Output
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def copy(self):
        """
        Return a copy.
        """
        return copy.deepcopy(self)
        
    def as_spec_cube(self,scale=True):
        """
        Return a spectral cube. Use scale to change type.
        """
        if isinstance(self._linked_data, SpectralCube):
            return SpectralCube(self._value*scale,
                                wcs=self._linked_data.wcs)
        return  SpectralCube(self._value*scale,
                             wcs=self._linked_data.wcs)

    def write(self,fname,scale=1):
        """
        Write to a file. Default to using ints.
        """
        # So wasteful...
        cube = self.as_spec_cube(self, scale=scale)
        cube.write(fname)
                
    def attach_to_cube(self,cube=None,empty=np.nan):
        """
        Attach the mask to a cube.
        """
        if cube is None:
            cube = self._linked_data
            
        if isinstance(cube,SpectralCube):
            # Bad
            cube._mask = self._value
            return

        if isinstance(cube,np.ndarray):
            if cube.shape == self._value.shape:
                # Replace False with NaNs
                cube = np.where(self._value, cube, empty)
                return
        
        print "Cube insufficiently specified."

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Expose the value
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def as_array(self):
        """
        Expose the values.
        """
        return self._value

    def as_indices(self):
        """
        As a tuple of indices where True, useful for indexing.
        """
        return np.where(self._value)

    def as_index_array(self,coordaxis=0):
        """
        As a numpy array of True indices. Optionally specify the axis for
        the coordinates (0 or 1)
        """
        if coordaxis == 0:
            return np.vstack(np.where(self._value))
        else:
            return np.vstack(np.where(self._value)).transpose()
        
    def twod(self, axis=0, sum=False):
        """
        Return a two-dimensional version of the mask.
        """
        if self._value.ndim == 2:
            return self._value     
        if sum:
            return (np.max(self._value, axis=axis))
        else:
            return (np.sum(self._value, axis=axis))

    # Slices, Subcube suggestions
        
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Undo/Redo
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def enable_backup(self):
        self._implict_backup = True

    def disable_backup(self):
        self._implict_backup = False

    def backup(self):
        self._backup = self._value

    def undo(self):
        temp = self._backup
        self._backup = self._value
        self._value = temp

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # MANIPULATION
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # Invert
    
    # Dilation
    
    # Erosion
    
    # Opening

    # Closing
    
    # Reject on volume/area/extent

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Mask generation
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # Structured thresholding

    # Projected 2d prior ("drop down" a twod mask)
    
    # Projected 3d prior ("inflate" a velocity field)

    # Define line-free channels

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # RECIPES
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # Convolve-then-threshold (2+1d)
    
    # High-reject-grow-low

    # Autotune thresholding

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# STRUCTURING ELEMENTS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# VISUALIZATION AND DIAGNOSTICS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
