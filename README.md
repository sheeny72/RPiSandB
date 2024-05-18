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
A Section Plot of Station Velocity Traces,
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
automatic selection of EHZ or SHZ channel as appropriate (not need to manually change code on error),
calculation of Rayleigh Surface Wave arrival time,
Calculation of Infrasound arrival time for correlation of Infrasound for explosive events such as some volcanic eruptions;
Figure and Axes Text.

Example output files are M6.3Quake Near Coast of Chiapas, Mexico*.png.

# StreamColours.py
This is some experimental code to simulate a stream.plot() but with individual colours for each trace.
The standard stream.plot() function plots all traces the same colour. This allows the user to specify different colours for each trace.

It will run on any Raspberry Shake 3D station. With minimal modification it to could also run on any 4D station.

Coloured Stream Plot.png is an example of the output.

# QR12any.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ channel (vertical geophone) which is common to all models (except the Raspberry Boom). Some models may use SHZ instead of EHZ. This is an upgrade of QReport10any.py and QR11any.py.

Output includes:
Filtered Displacement trace,
Filtered Velocity trace,
Filtered Acceleration trace,
Filtered Jerk trace,
Specific Energy trace,
Unfiltered velocity spectrogram,
Power Spectral Density plot (of filtered displacement, velocity, acceleration and jerk and optionally unfiltered velocity),
FFT Spectrum plot of (of filtered displacement, velocity, acceleration and/or jerk and optionally unfiltered velocity),
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
Estimations of the earthquake magnitude calculated from the maximum displacement (MLDv), veloity (MLVv) and Acceleration (MLAv) amplitudes. These can be turned off when not required.
Text for Social Media (Twitter) post (to copy),
Notes.

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the file "RS logo.png" to the same location as QR12any.

Most plot information is entered in lines 104 to 143.
Bandpass Filter corners are specified in lines 154 to 168.

The program demonstrates:
Reading station traces,
Selecting the active epoch from inventory data,
Distiguishing a Raspberry Shake and Boom from a Raspberry Shake,
Removing instrument response,
Trace manipulation/calculations,
Differentiation of a Trace,
Secondary axes,
Plotting arrivals,
colour coding arrival plots consistent with TAUp,
calculation and plotting of FFT spectrum,
use of gridspec to similate a stream plot with different colours for each trace,
automated zooming of nearside perspective map to suit quake/station separation,
automatic selection of EHZ or SHZ channel as appropriate (no need to manually change code on error),
calculation of Rayleigh Surface Wave arrival time,
Calculation of Infrasound arrival time for correlation of Infrasound for explosive events such as some volcanic eruptions;
Figure and Axes Text.

Example output files are M6.5Quake Vanuatu Islands*.png
Latest example file showing estimated earthquake magnitudes is M6.1Quake Timor Region*.png

# LocalStns4.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ or SHZ (vertical geophone) channel of each station.

Output Includes:
A Section Plot of Station Displacement Traces,
A customised map of the area of the stations and the event/earthquake,
Estimates of the ML for each trace by the Tsuboi Estimation Formula,
Calculation of the total "quake" energy

This program can be used to plot a section across multiple local stations for a known earthquake,
or it can also be used to locate an unregistered event such as a small local earthquake, or mine blast
by trial and error on the event location and timing.

Example output file:
Moolarben Mine Blast 231003 040950UTC.png

# LocalStns5.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ or SHZ (vertical geophone) channel of each station.

This is an upgrade of LocalStns4 in that the map extents have been modified to automatically adjust depending on the quake location and the stations selected for the section plot. The formula for estimating the magnitudes has also been updated.

Output Includes:
A Section Plot of Station Displacement Traces,
A customised map of the area of the stations and the event/earthquake,
Estimates of the MLDv for each trace by the modified Tsuboi Estimation Formula,
Calculation of the total "quake" energy

This program can be used to plot a section across multiple local stations for a known earthquake,
or it can also be used to locate an unregistered event such as a small local earthquake, or mine blast
by trial and error on the event location and timing.

Example output files:
M2.9 Boggabri Mine Blast 231103 012322UTC.png
M2.4 Mt Arthur Mine Blast 231103 000138UTC.png

# Event Data *.py
Selected earthquake event data saved by simple copy and paste direct from my programs.

# MLAv, MLDv, MLVv
Results of empirical formulae for estimating earthquake magnitude from maximum acceleration (MLAv), velocity (MLVv) and displacement (MLDv) amplitude on the vertical geophone (EHZ or SHZ) in any Raspberry Shake.
Assumes a lower bandpass filter of 0.7Hz (though 1Hz works OK) and the upper bandpass filter frequency must be high enough not to clip too much signal.

# Estimating Earthquake Magnitudes
Discussion of estimation of earthquake magnitudes for small, local earthquakes using the vertical geophone signal (EHZ or SHZ) in any Raspberry Shake.

# ComSpect.py
This code can run on any Raspberry Shake or raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ or HDF channels of a Raspberry Shake and Boom, but other channels compatible with 3D or 4D shakes can easily be added.

The aim is to compare two waveforms by plotting the PSD and FFT plots for each waveform sample on the same plot.

The code also calculates the difference between the two FFT plots as well. Trending has been added to the FFT difference plot to assist in quantitative and qualitative comparison.

Example output files are: Log Truck Passing *.png.

As all my programs use the same data format and variable names, this is a simple way to save the data in a readable (if verbose) form, to be able to retrieve the data simply to rerun a report of apply a new report to and old event.

# MagLimit.py
This code can be run on any Raspberry Shake on the Raspberry Shake Network.
It reads the EHZ or SHZ vertical geophone channel.
While it could be run on other channels (horizontal geophones or accelerometer channels) for comparison purposes, the estimated magnitude limits would not necessarily be numerically meaningful.

It's purpose is to read the background noise level on the channel and calculate the earthquake magnitude limits of what is detectible on the Shake.
It calculates the background noise level as 3x the standard deviation of the signal. This is done for both the whole test period and a smaller sample representing the minimum SD for that test period.
Hence the whole test period includes any local noise, of short duration, where the smaller sample is intended to pick up the minimum base level noise without transients.

The formulae used to estimate the earthquake magnitudes are the the empirical formulae for mLDv, mLVv and mLAv based on modified Tsuboi method (adjusted for 0.7Hx lower bandpass frequency).

Output includes:
Unfiltered Waveform,
Unfiltered PSD,
Unfilterd Spectrigram,
Filtered Waveform,
Filtered PSD,
Filtered Spectrogram,
Plot of the Earthquake Magnitude Limit v Distance.

This tool can be used to:
Compare outputs (DISP, VEL, or ACC) to determine which is most suitable to give the best signal to noise ratio given the frequencies found in the background noise;
Compare diurnal effects;
Compare old versus new shake location or installation (such as moving the shake or new or modified vault);
Compare different stations (e.g. compare city v country installations).

The Earthquake Magnitude Limit plot has fixed graph limits so plots can readily be compared by flicking between images.

Example output files are:
R21C0VEL*.png
RE900VEL*.png

# LocalStns7.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ or SHZ (vertical geophone) channel of each station.

This is an upgrade of previous versions in that provision has been made to determine the station to quake distance from the difference in P and S arrival times, and radius circles are plotted.
The quake location is at the intersection of the circles. The tightness of the intersections gives an indication of the accuracy of the estimation of the position of the quake.

Output Includes:
A Section Plot of Station Displacement, Velocity or Acceleration Traces,
A customised map of the area of the stations and the event/earthquake,
Estimates of the MLDv, MLVv and/or MLAv for each trace,
Calculation of the total "quake" energy,
Individual high resolution plots of each trace for estimation of P and S arrival times.

This program can be used to plot a section across multiple local stations for a known earthquake,
or it can also be used to locate an unregistered event such as a small local earthquake, or mine blast
by trial and error on the event location and timing.

The program does not automatically save plots. This is for simplicity and to allow the plots to be saved when complete manually using a common filename convention consistent with other files (such as QReport*.py).

Intended workflow:

1. Enter EventTime in line 195 at the whole minute 30 to 60s ahead of the observed event on the helicorder.
2. Set rplots to True, and plotrs to False in lines 204 and 205 respectively.
3. Select stations to include in the station list in lines 26 to 62.
4. Run LocalStns7. A high resolution plot of the trace of each station will be produced, along with the final section plot and map. Comment out any stations (in lines 26 to 62) that do not produce a useful trace.
5. Refer to each high resolution trace plot and estimate the P and S phase arrival times. Record these in pstimes in lines 64 to 74. Ensure you have a pair of times for each station - no more no less. Comment out unwanted lines, or add additional lines as required. Where one or both arrivals is NOT clear, consider changing output (e.g. Displacement, velocity, or acceleration) to get clear arrivals. Where one arrival is not clear, correct the timing for this arrival on successive iterations so it is not misleading. DO NOT ADJUST CLEAR ARRIVALS (other than to correct errors) - these are critical to accurate location and timing.
6. Change plotrs to True on line 205.
7. Re-run LocalStns7. This time the high resolution trace plots will have the estimated P and S arrival times plotted on them for checking. The Final map will also have circles plotted on it showin
8. g how far the quake is from each station. The epicentre will be at the intersection of all the circles.
9. Adjust the quake latitude (latE) and longitude (longE) to match the intersection of circles in lines 196 and 197.
10. Adjust the EventTime again to better match the arrivals on the section plot. (Remember to correct the pstimes whenever the EventTime is adjusted. i.e. if EventTime is increased by 18s, decrease the pstimes by 18s!)
11. Red dots are plotted on the section plot for each station which are the estimated arrival times from the high resolution plots. This is to aid precision in both location and timing adjustments.
12. Re-run LocalStns7 as many times as required to refine the position and timing of the quake.
13. Once position and timing of the quake is determined, set rplots to False for subsequent runs so the high resolution trace plots don't have to be produced every time the final plot is produced.

N.B. Each high resolution trace plot shows the stream index number in the legend to avoid confusion.

# LocalStns8.py
This code can be run on any Raspberry Shake or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the EHZ or SHZ (vertical geophone) channel of each station.

This is an upgrade of LOcalStns7.py. OpenStreetMap imagery has been added for the background of the map.
As in LocalStns7.py, provision has been made to determine the station to quake distance from the difference in P and S arrival times, and radius circles are plotted.
The quake location is at the intersection of the circles. The tightness of the intersections gives an indication of the accuracy of the estimation of the position of the quake.

Output Includes:
A Section Plot of Station Displacement, Velocity or Acceleration Traces,
A customised map of the area of the stations and the event/earthquake,
Estimates of the MLDv, MLVv and/or MLAv for each trace,
Calculation of the total "quake" energy,
Individual high resolution plots of each trace for estimation of P and S arrival times.

This program can be used to plot a section across multiple local stations for a known earthquake,
or it can also be used to locate an unregistered event such as a small local earthquake, or mine blast
by trial and error on the event location and timing.

The program does not automatically save plots. This is for simplicity and to allow the plots to be saved when complete manually using a common filename convention consistent with other files (such as QReport*.py).

Intended workflow:

1. Enter EventTime in line 195 at the whole minute 30 to 60s ahead of the observed event on the helicorder.
2. Set rplots to True, and plotrs to False in lines 204 and 205 respectively.
3. Select stations to include in the station list in lines 26 to 62.
4. Run LocalStns7. A high resolution plot of the trace of each station will be produced, along with the final section plot and map. Comment out any stations (in lines 26 to 62) that do not produce a useful trace.
5. Refer to each high resolution trace plot and estimate the P and S phase arrival times. Record these in pstimes in lines 64 to 74. Ensure you have a pair of times for each station - no more no less. Comment out unwanted lines, or add additional lines as required. Where one or both arrivals is NOT clear, consider changing output (e.g. Displacement, velocity, or acceleration) to get clear arrivals. Where one arrival is not clear, correct the timing for this arrival on successive iterations so it is not misleading. DO NOT ADJUST CLEAR ARRIVALS (other than to correct errors) - these are critical to accurate location and timing.
6. Change plotrs to True on line 205.
7. Re-run LocalStns7. This time the high resolution trace plots will have the estimated P and S arrival times plotted on them for checking. The Final map will also have circles plotted on it showin
8. g how far the quake is from each station. The epicentre will be at the intersection of all the circles.
9. Adjust the quake latitude (latE) and longitude (longE) to match the intersection of circles in lines 196 and 197.
10. Adjust the EventTime again to better match the arrivals on the section plot. (Remember to correct the pstimes whenever the EventTime is adjusted. i.e. if EventTime is increased by 18s, decrease the pstimes by 18s!)
11. Red dots are plotted on the section plot for each station which are the estimated arrival times from the high resolution plots. This is to aid precision in both location and timing adjustments.
12. Re-run LocalStns7 as many times as required to refine the position and timing of the quake.
13. Once position and timing of the quake is determined, set rplots to False for subsequent runs so the high resolution trace plots don't have to be produced every time the final plot is produced.
14. Adjust the OpenStreetMap imagery zoom level for best appearance in line 353.

N.B. Each high resolution trace plot shows the stream index number in the legend to avoid confusion.
Example output files for high resolution trace plots:
M2.5Quake BHP Mt Arthur Coal Mine, Muswellbrook, NSW, Australiaunknown20240502*.*
Example output for section plot and map:
M2.5Quake Moolarben *.*
