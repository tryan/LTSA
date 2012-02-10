Implementation of the Long Term Spectral Average as described by the Scripps Institute of Oceanography here: http://cetus.ucsd.edu/technologies_LTSA.html

An LTSA is a spectrogram for visualizing acoustic activity in relatively long recordings. Depending on the settings used to create and view the LTSA, the level of detail can vary widely, but the LTSA is most useful for viewing recordings that have relatively sparse acoustic activity. 

The Scripps Institute implementation of the LTSA is open source as part of the "Triton" package of Matlab programs they have released. My implementation is written without having studied theirs, and as such it is almost certainly not an identical algorithm, but rather one with similar goals. Octave compatibility is a goal of my implementation, as Triton is operated via a GUI, which is not supported by Octave.

# Algorithm Description and Terminology

* _Signal_ 
    * The entire audio recording, raw data only
* _Division_ 
    * The signal is broken up into non-overlapping divisions, which are processed independently
    * Usually called "div" in codebase
* _Subdivision_
    * Each division contains at least one subdivision. The subdivisions may or may not overlap. The subdivisions are windowed with a Hanning window and their spectra averaged together to represent the division
    * Usually called "subdiv" in codebase

#Usage

The ltsa_run script is the easiest way to compute an LTSA. Alternatively, you can call ltsa_process() directly. The ltsa_run script currently reads the entire audio file into memory before processing -- support is in forthcoming for piecewise processing of long files. 

The recommended way to save an LTSA is to either save the raw ltsa_process() output or save the figure (File -> Save As in Matlab, `print` in Octave) as imwrite will not attach axis ticks, labels, etc.
