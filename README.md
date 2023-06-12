# RPiSandB
Python programs for Raspberry Shake and Boom seismometers and infrasound detectors.

# QReport10any.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ channel (vertical geophone) which is common to all models (except the Raspberry Boom). Some models may use SHZ instead of EHZ.

Output includes:
Filtered Displacement trace
Filtered Velocity trace
Filtered acceleration trace
Specific Energy trace
Unfiltered velocity spectrogram
Power Spectral Density plot (of filtered displacement, velocity, acceleration and jerk and optionally unfiltered velocity)
Spherical Ray Path Plot
Nearside Perspective Map Plot
Background Noise in/at the station at the time of the event
trace maxima for filtered displacement, velocity, acceleration, specific energy and jerk
Signal to noise ratios for filtered dispalcement, velocity, acceleration and specific energy plots
Phase arrival times
Percentage vertical component of the phase arrival
Event details
Quake Energy
Phase key
Notes

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the files "RS logo.png" and "twitter logo.png" to the same location as QReport10any.

Most plot information is entered in lines 95 to 138.
Bandpass Filter corners are specified in lines 149 to 162.

The program demonstrates:
Reading station traces
Removing instrument response
Trace manipulation/calculations
Differentiation of a Trace
Secondary axes
Plotting arrivals
Figure and Axes Text
