Implementation of the Long Term Spectral Average as described by the Scripps Institute of Oceanography here: http://cetus.ucsd.edu/technologies_LTSA.html

An LTSA is a spectrogram for visualizing acoustic activity in relatively long recordings. Depending on the settings used to create and view the LTSA, the level of detail can vary widely, but the LTSA is most useful for viewing recordings that have relatively sparse acoustic activity. 

The Scripps Institute implementation of the LTSA is open source as part of the "Triton" package of Matlab programs they have released. My implementation is written without having studied theirs, and as such it is almost certainly not an identical algorithm, but rather one with similar goals. Octave compatibility is a goal of my implementation, as Triton is operated via a GUI, which is not supported by Octave. 

## Algorithm Description and Terminology

* _Signal_ 
    * The entire audio recording, raw data only
* _Division_ 
    * The signal is broken up into non-overlapping divisions, which are processed independently
    * Usually called "div" in codebase
* _Subdivision_
    * Each division contains at least one subdivision. The subdivisions may or may not overlap. The subdivisions are windowed with a Hanning window and their spectra averaged together to represent the division
    * Usually called "subdiv" in codebase

## Usage

### Matlab/Octave version

The `ltsa_run` script is the easiest way to compute an LTSA. Alternatively, you can call `ltsa_process()` directly. The `ltsa_run` script currently reads the entire audio file into memory before processing -- support is forthcoming for piecewise processing of long files. 

In `ltsa_run` there are a number of variables that control the LTSA computation:

* *file*: path to the file to be processed
* *div_len*: length of a division, in samples
* *subdiv_len*: length of a subdivision, in samples
* *nfft*: can be used to pad the FFT if desired
* *noverlap*: subdivision overlap, in samples

`ltsa_view()` displays the resulting LTSA. The fourth and fifth arguments specify time and frequency ranges to display.

The recommended way to save an LTSA is to either save the raw `ltsa_process()` output or save the figure (`File -> Save As` in Matlab, `print` in Octave or Matlab) as imwrite will not attach axis ticks, labels, etc.

### Python version

`ltsa.py` contains the `WavLTSA` class, which is instantiated with the name of the file to be processed and an optional channel argument for multichannel files. `ltsa.py` also contains the `RawLTSA` class, whose constructor accepts a one dimensional numpy array of raw audio data as well as a sampling frequncy argument. `WavLTSA` and `RawLTSA` objects have attributes that control the computation and can be changed directly or by use of the `set_params()` method. 

The `compute()` method runs the algorithm using the current parameters of the object and stores the resulting image in the `ltsa` attribute. 

The `crop()` method crops the image to a specified time/frequency range. Data outside this range is thrown away by cropping. 

The `show()` method displays the image in the current figure using `pyplot.imshow()`. `show()` accepts optional arguments for resizing the image. Calling `show()` with an integer argument `n` will downsample the image vertically to `n` pixels of height. Calling show() with a tuple like `(h, w)` will use SciPy's `imresize()` to resize the image. 
