# RPiSandB
Python programs for Raspberry Shake and Boom seismometers and infrasound detectors.

# QReport10any.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ channel (vertical geophone) which is common to all models (except the Raspberry Boom). Some models may use SHZ instead of EHZ.

Output includes:
Filtered Displacement trace,
Filtered Velocity trace,
Filtered acceleration trace,
Specific Energy trace,
Unfiltered velocity spectrogram,
Power Spectral Density plot (of filtered displacement, velocity, acceleration and jerk and optionally unfiltered velocity),
Spherical Ray Path Plot,
Nearside Perspective Map Plot,
Background Noise in/at the station at the time of the event,
trace maxima for filtered displacement, velocity, acceleration, specific energy and jerk,
Signal to noise ratios for filtered displacement, velocity, acceleration and specific energy plots,
Phase arrival times,
Percentage vertical component of the phase arrival,
Event details,
Quake Energy,
Phase key,
Notes.

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the files "RS logo.png" and "twitter logo.png" to the same location as QReport10any.

Most plot information is entered in lines 95 to 138.
Bandpass Filter corners are specified in lines 149 to 162.

The program demonstrates:
Reading station traces,
Removing instrument response,
Trace manipulation/calculations,
Differentiation of a Trace,
Secondary axes,
Plotting arrivals,
Figure and Axes Text.

Files "M5.8 West of Macquarie Island*.png" are examples of the output.

# BoomEventReport4.py
This code can be run on any Raspberry Boom or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the HDF channel (infrasound sensor) which is common to all Raspberry Booms and Raspberry Shake and Booms.

Output includes:
Raw count trace,
Peak Raw Counts,
Power Spectral Density of both Raw Counts and Filtered Infrasound Prssure (Pa),
Spectrogram of the Unfilterd Raw Counts,
Filtered Infrasound Pressure trace in Pascals (Pa),
Peak Filtered Infrasound Pressure (Pa),
Unweighted Infrasound Pressure Level trace in decibels (dB),
Peak Unweighted Infrasound Level (dB),
Filtered Infrasound Intensity trace (W/m2),
Peak Filtered Infrasound Intensity (W/m2),
Peak Source Filtered Infrasound Power (W) if the distance to the source is known,
Filtered Infrasound Energy Cumulative trace (J/m2),
Total Cumulative Filtered Infrasound Energy (J) if the dtsance to the source is known,
Notes.

Most plot information is added in lines 40 to 61.

The program demonstrates:
Reading station traces,
Removing instrument response,
Conversion of counts to Infrasound Pressure,
Conversion of Infrasound Pressure to Infrasound Pressure Level,
Conversion of Infrasound Pressure to Infrasound Intensity,
Integration of the Infrasound Pressure trace to create the Cumulative Infrasound Energy trace,
Calculation of Peak Source Infrasound Power,
Calculation of Total Infrasound Power.

Example output files:
R21C0 Background InfrasoundR21C0 HDF 20230605 021500 UTC.png
Spacex Dragon Crew 1 Trunk Re-EntryR21C0 HDF 20220708 212230 UTC 3.png

# RSandBCorr.py
This code can be run on any Raspberry Shake and Boom on the Raspberry Shake Network.
It could be adapted to compare any two channels on any two stations on the Raspberry Shake Network.
It reads both the EHZ and HDF channels of the Raspberry Shake and Boom and tests for correlation between the two channels.
i.e. is a seismic signal driving the infrasound channel or producing infrasound or is an infrasound signal driving the vibration channel or producing a seismic signal.

Both the raw counts traces and the filtered (velocity and pressure) traces are tested for correlations.

This was developed as a first step to developing a program to search for meteor infrasound detections.
i.e. if there is a reasonable correlation with the seismic signal it is not likely to be a meteor.

Output includes:
EHZ raw counts trace,
HDF raw counts trace,
Raw shift between traces in 1/100ths of a second,
Raw trace correlation coefficient,
EHZ velocity trace,
HDF pressure trace,
Filtered shift between velocity and pressure in 1/100ths of a second,
Filtered trace correlation coefficient.

# LocalStns2.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ (vertical geophone) channel of each station.

Output Includes:
A Section Plot of Station Traces,
A customised map of the area of the stations and the event/earthquake,

This program can be used to plot a section across multiple local stations for a known earthquake,
or it can also be used to locate an unregistered event such as a small local earthquake, or mine blast
by trial and error on the event location and timing.

Example output file:
Ulan Mine Blast 230610 060918UTC 1.png

# Q3DSEReport.py
This code can be run on any RS3D Raspberry Shake on the Raspberry Shake Network.
It reads all three channels (EHZ, EHE and EHN).

Output includes:
Filtered velocity traces for EHZ, EHE and EHN channels,
Specific Energy Traces showing total Specific Energy and components from each of the 3 channels,
Unfiltered spectrogram of the EHZ channel,
a choice of:
Power Spectral Density plots for all three channels; or
Fast Fourier Transform plot of all three channels,
Background Noise levels on all three channels,
a table of Phase arrival times,
Spherical Ray Path plot,
Nearside Perspective map of the event and station,
Event details,
Quake Energy,
Phase key,
Notes.

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the files "RS logo.png" and "twitter logo.png" to the same location as Q3DSEReport.

Most plot information is entered in lines 80 to 115.
Bandpass Filter corners are specified in lines 126 to 137.

The program demonstrates:
Reading station traces,
Removing instrument response,
Trace manipulation/calculations,
Secondary axes,
Plotting arrivals,
Figure and Axes Text.

Example output files:
M6.9Quake Tonga Islandsrs2023mwwzcd20230702 102743 UTCRB59E All.png
M6.9Quake Tonga Islandsrs2023mwwzcd20230702 102743 UTCRB59E P P P pP pP pP pP sP sP sP sP sP.png

# QR11any.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ channel (vertical geophone) which is common to all models (except the Raspberry Boom). Some models may use SHZ instead of EHZ. This is an upgrade of Qreport10any.py.

Output includes:
Filtered Displacement trace,
Filtered Velocity trace,
Filtered acceleration trace,
Specific Energy trace,
Unfiltered velocity spectrogram,
a choice of:
Power Spectral Density plot (of filtered displacement, velocity, acceleration and jerk and optionally unfiltered velocity); or
FFT Spectrum plot of (of filtered displacement, velocity, acceleration and/or jerk and optionally unfiltered velocity,
Spherical Ray Path Plot,
Nearside Perspective Map Plot,
Background Noise in/at the station at the time of the event,
trace maxima for filtered displacement, velocity, acceleration, specific energy and jerk,
Signal to noise ratios for filtered displacement, velocity, acceleration and specific energy plots,
Phase arrival times,
Percentage vertical component of the phase arrival,
Event details,
Quake Energy,
Phase key,
Notes.

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the files "RS logo.png" and "twitter logo.png" to the same location as QR11any.

Most plot information is entered in lines 102 to 141.
Bandpass Filter corners are specified in lines 152 to 166.

The program demonstrates:
Reading station traces,
Selecting the active epoch from inventory data,
Removing instrument response,
Trace manipulation/calculations,
Differentiation of a Trace,
Secondary axes,
Plotting arrivals,
colour coding arrival plots consistent with TAUp,
calculation and plotting of FFT spectrum,
automated zooming of nearside perspective map to suit quake/station separation,
calculation of Rayleigh Surface Wave arrival time,
Calculation of Infrasound arrival time for correlation of Infrasound for explosive events such as some volcanic eruptions;
Figure and Axes Text.

Files "M6.3Quake Near Cost of Chiapas, Mexico*.png" are examples of the output.
