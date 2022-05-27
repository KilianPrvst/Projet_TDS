"""
Algorithm implementation
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt
from essai import constellation
import scipy

from scipy.io.wavfile import read
from scipy.signal import spectrogram
from skimage.feature import peak_local_max

# ----------------------------------------------------------------------------
# Create a fingerprint for an audio file based on a set of hashes
# ----------------------------------------------------------------------------


class Encoding:

    """
    Class implementing the procedure for creating a fingerprint 
    for the audio files

    The fingerprint is created through the following steps
    - compute the spectrogram of the audio signal
    - extract local maxima of the spectrogram
    - create hashes using these maxima

    """
    def __init__(self):

        """
        Class constructor

        To Do
        -----

        Initialize in the constructor all the parameters required for
        creating the signature of the audio files. These parameters include for
        instance:
        - the window selected for computing the spectrogram
        - the size of the temporal window 
        - the size of the overlap between subsequent windows
        - etc.

        All these parameters should be kept as attributes of the class.
        """

        # Insert code here
        self.fs, self.sample = read(path)
        #POUR TESTER PLUS VITE
        self.sample = self.sample[:10000]
        self.window = 128
        self.noverlap = 32
        self.n_coeff = len(self.sample)
      #   self.window = scipy.signal.get_window('triang', 128)
      #   self.window_size = len(self.window)

    def process(self, fs, s):

        """

        To Do
        -----

        This function takes as input a sampled signal s and the sampling
        frequency fs and returns the fingerprint (the hashcodes) of the signal.
        The fingerprint is created through the following steps
        - spectrogram computation
        - local maxima extraction
        - hashes creation

        Implement all these operations in this function. Keep as attributes of
        the class the spectrogram, the range of frequencies, the anchors, the 
        list of hashes, etc.

        Each hash can conveniently be represented by a Python dictionary 
        containing the time associated to its anchor (key: "t") and a numpy 
        array with the difference in time between the anchor and the target, 
        the frequency of the anchor and the frequency of the target 
        (key: "hash")


        Parameters
        ----------

        fs: int
           sampling frequency [Hz]
        s: numpy array
           sampled signal
        """

        # Insert code here
        self.spectr = spectrogram(self.sample,self.fs,nperseg = self.window,noverlap = self.noverlap)
        self.f, self.t, self.Sxx = self.spectr
        
        
        def display_spectrogram(self):
           plt.pcolormesh(self.t,self.f,self.Sxx)
        #self.spec = scipy.signal.spectrogram(s, fs, self.window, noverlap = 32)
        #self.f, self.t, self.Sxx = scipy.signal.spectrogram(s, fs, return_onesided=False)
        self.maxi = peak_local_max(self.Sxx, min_distance=1, indices=True, exclude_border = False)
        #Construisons la constellation du morceau:
        delta_t = 0.01
        def constellation(delta_t,coord_maxima):
           hash = {}
           x = coord_maxima[:,0]
           y = coord_maxima[:,1]
           for i in range(len(x)):
              for j in range(i,len(x)):
                 if abs(x[i] - x[j]) < delta_t and abs(y[i] - y[j]):
                    hash[f"{i}"] = {abs(i - j), y[i],y[j]}
                    return hash
        self.constellation = constellation(self.t, self.maxi)
        return self.constellation

    def display_spectrogram(self):
      f, t, Sxx = scipy.signal.spectrogram(s, fs, return_onesided=False)
      plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
      plt.ylabel('Frequency [Hz]')
      plt.xlabel('Time [sec]')
      plt.show()


        


# ----------------------------------------------------------------------------
# Compares two set of hashes in order to determine if two audio files match
# ----------------------------------------------------------------------------

class Matching:

    """
    Compare the hashes from two audio files to determine if these
    files match

    Attributes
    ----------

    hashes1: list of dictionaries
       hashes extracted as fingerprints for the first audiofile. Each hash 
       is represented by a dictionary containing the time associated to
       its anchor (key: "t") and a numpy array with the difference in time
       between the anchor and the target, the frequency of the anchor and
       the frequency of the target (key: "hash")

    hashes2: list of dictionaries
       hashes extracted as fingerprint for the second audiofile. Each hash 
       is represented by a dictionary containing the time associated to
       its anchor (key: "t") and a numpy array with the difference in time
       between the anchor and the target, the frequency of the anchor and
       the frequency of the target (key: "hash")

    matching: numpy array
       absolute times of the hashes that match together

    offset: numpy array
       time offsets between the matches
    """

    def __init__(self, hashes1, hashes2):

        """
        Class constructor

        Compare the hashes from two audio files to determine if these
        files match

        To Do
        -----

        Implement a code establishing correspondences between the hashes of
        both files. Once the correspondences computed, construct the 
        histogram of the offsets between hashes. Finally, search for a criterion
        based on the histogram that allows to determine if both audio files 
        match

        Parameters
        ----------

        hashes1: list of dictionaries
           hashes extracted as fingerprint for the first audiofile. Each hash 
           is represented by a dictionary containing the time associated to
           its anchor (key: "t") and a numpy array with the difference in time
           between the anchor and the target, the frequency of the anchor and
           the frequency of the target

        hashes2: list of dictionaries
           hashes extracted as fingerprint for the second audiofile. Each hash 
           is represented by a dictionary containing the time associated to
           its anchor (key: "t") and a numpy array with the difference in time
           between the anchor and the target, the frequency of the anchor and
           the frequency of the target
        """


        self.hashes1 = hashes1
        self.hashes2 = hashes2

        # Insert code here
        



             
    def display_scatterplot(self):
       """
        Display through a scatterplot the times associated to the hashes
        that match
        """
    
       
       keys1 = hashes1.key()
       keys2 = hashes2.key()
       time_cloud = [[],[]]
       for k1 in keys1:
           for k2 in keys2:
              if k1 == k2:
                 time_cloud[0].append(k1 - hashes1[f"k1"][0])
                 time_cloud[1].append(k2 - hashes2[f"k2"][0])
       plt.scatter(time_cloud[0],time_cloud[1])
       plt.show()


      

    def display_histogram(self):

        """
        Display the offset histogram
        """

        # Insert code here



# ----------------------------------------------
# Run the script
# ----------------------------------------------
if __name__ == '__main__':

    encoder = Encoding()
    fs, s = read('./samples/Late Truth - Audio Hertz.wav')
    encoder.process(fs, s[:900000])
    encoder.display_spectrogram(display_anchors=True)





