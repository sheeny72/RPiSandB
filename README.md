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

As all my programs use the same data format and variable names, this is a simple way to save the data in a readable (if verbose) form, to be able to retrieve the data simply to rerun a report of apply a new report to and old event.

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

This version has now been updated to allow use of local instrument response files if instrument response is unavailable on the FDSN server.

Example output files are: Log Truck Passing *.png.

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

This version has now been updated to allow use of local instrument response files if instrument response is unavailable on the FDSN server.

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

This is an upgrade of LOcalStns7.py. OpenStreetMap imagery has been added for the background of the map and also allows instrument response from local file rather than FDSN server.
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

# RSnB Plinth.pdf
This is a drawing for a proposed plinth for my Raspberry Shake and Boom (RSnB), but it will probably also house my Raspberry Shake 3D. Installation is waiting on establishing reliable network to the shed.

It uses the tapered ends of a 200L HDPE drum to form the plinth and make the cover for the Shakes.

A 4 port infrasound manifold is cast into the plinth using 20mm PVC pipe, a 20mm PVC pipe 5 way joint, and a 20mm PVC to 1/2" BSP elbow. Building the manifold into the plinth keeps it low to the ground to minimise the effects of wind noise, and it also allows the minimum length of 4mm plastic tubing for connection to the RSnB to minimise attenuation.

The plinth will be located close to but not touching the shed so that ethernet and the power cables for the Shakes can pass through the 25mm PVC conduit. The conduit will be flexibly sealed to the shed wall cladding to minimise transmission of any noise/vibration from the shed.

The cover will be attached by 4 M8 bolts and nutserts rivetted into the plinth form. The nutserts will be taped off from the inside to stop concrete entering the threads.

Builders plastic will be used to line the excavation (which is only shown roughly) to prevent rising ground moisture.

If in future, a surrounding concrete slab is to be poured, 10 or 12mm expansion form is to be used to ensure isolation from the slab. (This has worked excellently in previous observatory pier plinth/floor designs).

The cover will be trimmed to suit the infrasound manifold and conduit.

The planned location is of the souther side (southern hemisphere!) of the shed so it should be shaded most of the time.

In the event that high temperatures, or high humidity becomes an issue, 2mm ventialtion holes will ve drilled in the cover around the perispher just above the top of the plinth for ventilation. These holes will be angled up for outside to inside to prevent water ingress.

Open cell foam plugs can be cut to fit the ends of the infrasound manifold pipes to prevent wasps and other insects nesting inside, but the design is conducing to rodding of the manifold if necessary to remove and such blockages.

Being a plinth design, ground water and flooding issues associated with pit type vaults should be eliminated. The size and depth of the plinth excavation should allow good seismic transmission.

# Q3DSEReport3.py
This code can be run on any RS3D Raspberry Shake on the Raspberry Shake Network.
It reads all three channels (EHZ, EHE and EHN).
It is an update of Q3DSEReport.py

There is latent code included for use of local inventory files (just need to uncomment these lines if required).

Output includes:
Filtered velocity traces for EHZ, EHE and EHN channels,
Specific Energy Traces showing total Specific Energy and components from each of the 3 channels,
Unfiltered spectrogram of all channels,
Power Spectral Density plots for all three channels;
Fast Fourier Transform plot of all three channels,
Background Noise levels on all three channels,
a table of Phase arrival times,
Spherical Ray Path plot,
Nearside Perspective map of the event and station,
Particle Motion Plots,
Event details,
Quake Energy including TNT equivalent,
Phase key,
Notes.

The background noise limits and Specific Energy plot were developed to assist identification of weak arrivals.

Copy and save the files "RS logo.png" to the same location as Q3DSEReport3.

Most plot information is entered in lines 83 to 126.
Bandpass Filter corners are specified in lines 136 to 148.

The program demonstrates:
Reading station traces,
Removing instrument response,
Trace manipulation/calculations,
Secondary axes,
Plotting arrivals,
Figure and Axes Text.

Example output files:
M6.3Quake Vanuatu Islands*.png

# BoomGWeighting
This code can be run on any Raspberry Boom or Raspberry Shake and Boom on the Raspberry Shake Network.
It reads the HDF channel.
It's intended use is for direct comparison with noise pollution compliance requirements which may be expressed in units of dB(G).

Output includes:
Filtered waveform (in Pa);
Normalised linear FFT spectrum in Pa;
G weighted FFT spectrum in Pa;
Normailised linear FFT spectrum in dBL;
G weighted FFT spectrum (db(G));
Time domain plots of Infrasound Pressure Level in dBL and estimated dB(G);
Peak Infrasound Pressure in Pa;
Peak Infrasound Pressure Level in dbL;
Estimated Peak Infrasound Pressure Level in dB(G);
Notes.

Note: the Infrasound pressure level in dB(G) is "estimated" as the calculation method assumes the frequency distribution
across the sample does not change, so it is not as accurate as hardware weighting filters between the microphone and a SPL meter.

Empirical formulae were used to approximate the G weighting curve with R>=0.9999.

Example output files:
IR-R21C0Quarry*.png

# BoomGWeighting3.py
This code can be run on any Raspberry Boom or Raspberry Shake and Boom on the Raspberry Shake Network.
It uses module RBoomGWeighting.py and demonstrates a typical workflow for using the RBoomGWeighting.py module.
It reads the HDF channel.
It's intended use is for direct comparison with noise pollution compliance requirements which may be expressed in units of dB(G).

Output includes:
Filtered waveform (in Pa);
Normalised linear FFT spectrum in Pa;
G weighted FFT spectrum in Pa;
Normailised linear FFT spectrum in dBL;
G weighted FFT spectrum (db(G));
Time domain plots of Infrasound Pressure Level in dBL and estimated dB(G);
Peak Linear Infrasound Pressure in Pa;
Peak G weighted Infrasound Pressure in Pa;
Peak Linear Infrasound Pressure Level in dbL;
Estimated Peak Infrasound Pressure Level in dB(G);
Octave or 1/3 Octave analysis including peak, peak to peak, average and RMS amplitude, as well as waveforms;
Notes.

Note: 1/3 Octave or Octave analysis is used to apply G weighting and reconstruct and estimated G weighted waveform.

Empirical formulae were used to approximate the G weighting curve with R>=0.9999.

Example output files:
IR-R21C0Quarry*.png

#########################################################################################
# RBoomGWeighting.py

This is a module used by BoomGWeighting3.py.

Functions include:

def fftL(y, fl, fu):
    """
    fftL produces a linear FFT from a filtered signal waveform.
    Wave form units are Pascals (Pa) and output fft units are also Pascals(Pa)
    i.e. FFT units same as waveform
    
    Parameters
    ----------
    y : stream 
        Obspy waveform stream with response removed. Pa
    fl : float
        Bandpass lower frequency used to filter y. Hz
    fu : float
        Bandpass upper frequency used to filter y. Hz

    Returns
    -------
    f_plot : array of float64
        np.array of frequencies for the fft plot. Hz
    lfft : array of float64
        FFT values for f_plot. Pa

    """

def peak(y):
    """
    Calculate maximum pressure amplitude
    
    Parameters
    ----------
    y : trace 
        Obspy waveform stream with response removed. Pa

    Returns
    -------
    maxp : float64
        maximum waveform amplitude. Pa
    
    """

def peak_peak(y):
    """
    Calculate maximum peak to peak pressure amplitude
    
    Parameters
    ----------
    y : trace 
        Obspy waveform stream with response removed. Pa

    Returns
    -------
    maxpp : float64
        maximum waveform peak to peak amplitude. Pa
    
    """

def average(y):
    """
    Calculate average pressure amplitude
    
    Parameters
    ----------
    y : trace 
        Obspy waveform trace with response removed. Pa

    Returns
    -------
    yav : float64
        waveform average amplitude for the sample. Pa
    
    """

def rms(y):
    """
    Calculate RMS pressure amplitude
    
    Parameters
    ----------
    y : trace 
        Obspy waveform trace with response removed. Pa

    Returns
    -------
    yrms : float64
        waveform root mean square (RMS) amplitude for the sample. Pa
    
    """

def pa2db(y):    
    """
    Convert Pascals (Pa) to linear (unweighted) decibels (dBL)
    
    Parameters
    ----------
    y : stream 
        Obspy waveform stream with response removed. Pa

    Returns
    -------
    db : stream
        Obspy wave form stream. dBL
    
    """

def db2pa(db):    
    """
    Convert decibels (dB) to Pascals (Pa)
    
    Parameters
    ----------
    db : array of float 
        array of decibel (dB) values

    Returns
    -------
    x : stream
        Obspy wave form stream. dBL
    
    """

def peakSPL(y):
    """
    Calculate the peak sound pressure level (SPL). dBL
    
    Parameters
    ----------
    y : stream 
        Obspy waveform stream with response removed. Pa

    Returns
    -------
    pspl : float64
        Peak sound pressure level (SPL). dBL
    
    """

def fft2dBL(lfft):
    """
    Convert FFT in Pa to dBL
    
    Parameters
    ----------
    lfft : array of float64
        Linear FFT values. Pa

    Returns
    -------
    fftdB : list
        FFT values in sound pressure level (SPL). dBL
    
    """

def dBL2dBG(f_plot, fftdB):
    """
    Convert dBL to dB(G)
    Empirical formulae curve fitted to G weighting curve with R>=0.9999
    
    Parameters
    ----------
    f_plot : array of float64
        np.array of frequencies for the fft plot. Hz
    fftdB : list
        FFT values in sound pressure level (SPL). dBL

    Returns
    -------
    fftdBG : list
        G weighted FFT values in sound pressure level (SPL). dB(G)
    
    """

def dBG2PaG(f_plot, fftdB, fftdBG, fl, fu):
    """
    Convert G weighted SPL FFT in dB(G) back to G weighted FFT in Pa
    
    Parameters
    ----------
    f_plot : array of float64
        np.array of frequencies for the fft plot. Hz
    fftdB : list
        Linear FFT values in sound pressure level (SPL). dBL
    fftdBG : list
        G weighted FFT values in sound pressure level (SPL). dB(G)

    Returns
    -------
    fftG : list
        G weighted FFT values in Pascals. Pa
    l2G : float64
        Average difference between G weighted and linear sound pressure levels.
        i.e. to be ADDED to dbL to get db(G)
    
    """

def octave():
    """
    Generate an array of standard octave band centre frequencies
    
    Parameters
    ----------
    nil.
    
    Returns
    -------
    oct : 2D array of float
        oct[n][0] : octave band number
        oct[n][1] : octave band nominal frequency, Hz
        oct[n][2] : octave band centre frequency, Hz
 
    Use the band number to correlate with reports using this notation
    Use the nominal frequency for labelling octaves
    use the centre frequency for calculating octave upper and lower frequencies
    
    'Octave' : text bendwidth identifier
    
    """

def octFL(fc):
    """
    Calculate lower octave band frequency
    
    Parameters
    ----------
    fc : float
        Calculated octave band centre frequency. Hz

    Returns
    -------
    fl : float
        Octave band lower frequency. Hz
    
    """

def octFU(fc):
    """
    Calculate upper octave band frequency
    
    Parameters
    ----------
    fc : float
        Calculated octave band centre frequency. Hz

    Returns
    -------
    fu : float
        Octave band upper frequency. Hz
    
    """

def octBandLow(fl, fu):
    """
    Find the lowest octave band fully within the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    octBL[i] : array of float
        octBL[i][0] : Octave Band Number.
        octBL[i][1] : Octave band nominal frequency. Hz
        octBL[i][2] : Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def octBandHigh(fl, fu):
    """
    Find the highest octave band fully within the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    octBH[i] : array of float
        octBH[i][0] : Octave Band Number.
        octBH[i][1] : Octave band nominal frequency. Hz
        octBH[i][2] : Octave Band centre frequency. Hz
     i : index in octave array
   
    """

def octBandLow1(fl, fu):
    """
    Find the lowest octave band which spans the lower frequency of the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    octBL[i] : array of float
        octBL[i][0] : Octave Band Number.
        octBL[i][1] : Octave band nominal frequency. Hz
        octBL[i][2] : Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def octBandHigh1(fl, fu):
    """
    Find the highest octave band which spans the upper frequency of the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    octBH[i] : array of float
        octBH[i][0] : Octave Band Number.
        octBH[i][1] : Octave band nominal frequency. Hz
        octBH[i][2] : Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def octBands(fl, fu, within):
    """
    Calculate an array of octave band frequencies
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz
    within : boolean
        True of bands wholly contained inside bandpass filter frequencies
        False if bands span the bandpass filter frequencies

    Returns
    -------
    octB[i][j] : array of float
        octB[i][0] : Octave Band Number.
        octB[i][1] : Octave band nominal frequency. Hz
        octB[i][2] : Octave Band centre frequency. Hz
        octB[i][3] : Octave Band lower frequency. Hz
        octB[i][4] : Octave Band upper frequency. Hz

    """

def octave13():
    """
    Generate an array of standard 1/3 octave band frequencies
    
    Parameters
    ----------
    nil.
    
    Returns
    -------
    oct13 : 2D array of float
        oct13[n][0] : 1/3 octave band number
        oct13[n][1] : 1/3 octave band nominal frequency, Hz
        oct13[n][2] : 1/3 octave band centre frequency, Hz
    
    oct13t : text band width identifier
    
    """

def oct13FL(fc):
    """
    Calculate lower 1/3 octave band frequency
    
    Parameters
    ----------
    fc : float
        Calculated 1/3 octave band centre frequency. Hz

    Returns
    -------
    fl : float
        1/3 Octave band lower frequency. Hz
    
    """

def oct13FU(fc):
    """
    Calculate upper 1/3 octave band frequency
    
    Parameters
    ----------
    fc : float
        Calculated 1/3 octave band centre frequency. Hz

    Returns
    -------
    fu : float
        1/3 Octave band upper frequency. Hz
    
    """

def oct13BandLow(fl, fu):
    """
    Find the lowest 1/3 octave band fully within the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    oct13BL[i] : array of float
        oct13BL[i][0] : 1/3 Octave Band Number.
        oct13BL[i][1] : 1/3 Octave band nominal frequency. Hz
        oct13BL[i][2] : 1/3 Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def oct13BandHigh(fl, fu):
    """
    Find the highest octave band fully within the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    oct13BH[i] : array of float
        oct13BH[i][0] : Octave Band Number.
        oct13BH[i][1] : Octave band nominal frequency. Hz
        oct13BH[i][2] : Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def oct13BandLow1(fl, fu):
    """
    Find the lowest 1/3 octave band which spans the lower frequency of the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    oct13BL[i] : array of float
        oct13BL[i][0] : 1/3 Octave Band Number.
        oct13BL[i][1] : 1/3 Octave band nominal frequency. Hz
        oct13BL[i][2] : 1/3 Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def oct13BandHigh1(fl, fu):
    """
    Find the highest octave band which spans the upper frequency of the filter frequency range
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz

    Returns
    -------
    oct13BH[i] : array of float
        oct13BH[i][0] : 1/3 Octave Band Number.
        oct13BH[i][1] : 1/3 Octave band nominal frequency. Hz
        oct13BH[i][2] : 1/3 Octave Band centre frequency. Hz
    i : index in octave array
    
    """

def oct13Bands(fl, fu, within):
    """
    Calculate an array of 1/3 octave band frequencies
    
    Parameters
    ----------
    fl : float
        Bandpass lower frequency. Hz
    fu : float
        Bandpass upper frequency. Hz
    within : boolean
        True of bands wholly contained inside bandpass filter frequencies
        False if bands span the bandpass filter frequencies

    Returns
    -------
    oct13B[i][j] : array of float
        oct13B[i][0] : Octave Band Number.
        oct13B[i][1] : Octave band nominal frequency. Hz
        oct13B[i][2] : Octave Band centre frequency. Hz
        oct13B[i][3] : Octave Band lower frequency. Hz
        oct13B[i][4] : Octave Band upper frequency. Hz

    """

def sum_waveforms(a, b):
    
    """
    Add waveform data points from 2 waveforms of the same length

    Parameters
    ----------
    a : stream 
        Obspy waveform stream with response removed. Pa
        
    b : stream 
        Obspy waveform stream with response removed. Pa

    Returns
    -------
    c : stream 
        Obspy waveform stream with response removed. Pa
    """

def sum_stream(st):
    """
    Sum the band analysed / processed waveforms back to a single stream/trace

    Parameters
    ----------
    st : stream 
        Obspy waveform stream with response removed. Pa
        
    Returns
    -------
    c : trace 
        Obspy waveform trace with response removed. Pa
    """

def plotBands (a, ax):
    """
    Plot bands on selected axes
    
    Parameters
    ----------
    a[i][j] : array of float
        a[i][0] : Octave Band Number.
        a[i][1] : Octave band nominal frequency. Hz
        a[i][2] : Octave Band centre frequency. Hz
        a[i][3] : Octave Band lower frequency. Hz
        a[i][4] : Octave Band upper frequency. Hz
        
    ax : Matlotlib pyplot axes
        Target axes for band plots

    Returns
    -------
    nil

    """

def update_trace_stats(z):
    """
    Add or update stats to a trace
    
    Parameters
    ----------
    z : trace 
        Obspy waveform trace in Infrasound Pressure. Pa
        

    Returns
    -------
    z : trace 
        Obspy waveform trace in Infrasound Pressure. Pa
        
        Stats added or updated to trace:
            z.stats.max = maximum amplitude as float
            z.stats.mean = mean (or average) amplitude as float
            z.stats.rms = root mean squared (RMS) amplitude as float

    """

def band_waveforms(a, bands):
    """
    Build a stream of waveforms filtered by bands
    
    Parameters
    ----------
    a : stream 
        Obspy waveform stream in Infrasound Pressure. Pa
        
    bands[i][j] : array of float
        bands[i][0] : Octave Band Number.
        bands[i][1] : Octave band nominal frequency. Hz
        bands[i][2] : Octave Band centre frequency. Hz
        bands[i][3] : Octave Band lower frequency. Hz
        bands[i][4] : Octave Band upper frequency. Hz

    Returns
    -------
    st : stream 
        Obspy waveform stream in Infrasound Pressure. Pa
        One trace per filter band.
        
        Stats added to each trace:
            st[i].stats.filter = bandpass filter range as string
            st[i].stats.max = maximum amplitude as float
            st[i].stats.mean = mean (or average) amplitude as float
            st[i].stats.rms = root mean squared (RMS) amplitude as float

    """

def band_stream_plot(a, title1, title2, save, file):
    """
    Plot a stream of waveforms filtered by bands
    
    Parameters
    ----------
    a : stream 
        Obspy waveform stream in Infrasound Pressure. Pa
        
    title : Title text for the plot
    
    save : boolean
        save = True to automatically name and save the plot
        save = False to display only without saving
        
    file : text
        file = filename including path for saving. title and .png will be added!
    
    Returns
    -------
    nil
    
    """

def band_G_factors(f, fftL, fftG, bands):
    """
    Build an an array of G weighting factors for each band
    
    Parameters
    ----------
    f : array of float64
        np.array of frequencies for the fft plot. Hz
    fftL : list
        Linear FFT values in infrasound pressure (Pa)
    fftG : list
        G weighted FFT values in infrasound pressure (Pa)
        
    bands[i][j] : array of float
        bands[i][0] : Octave Band Number.
        bands[i][1] : Octave band nominal frequency. Hz
        bands[i][2] : Octave Band centre frequency. Hz
        bands[i][3] : Octave Band lower frequency. Hz
        bands[i][4] : Octave Band upper frequency. Hz

    Returns
    -------
    bandGs : array of float64
        np.array of max G weight and linear amplitude per band
        
        bandGs[i][0] : max Linear FFT amplitude
        bandGs[i][1] : corresponding max G weighted FFT amplitude
    """

def band_G_waveforms(lwaves, bandGs):
    """
    Build a stream of G weighted waveforms filtered by bands
    
    Parameters
    ----------
    lwaves : stream 
        Obspy linear waveform stream in Infrasound Pressure. Pa
        One trace per filter band.
        
        Stats added to each trace:
            st[i].stats.filter = bandpass filter range as string
            st[i].stats.max = maximum amplitude as float
            st[i].stats.mean = mean (or average) amplitude as float
            st[i].stats.rms = root mean squared (RMS) amplitude as float
        
    bands[i][j] : array of float
        bands[i][0] : Octave Band Number.
        bands[i][1] : Octave band nominal frequency. Hz
        bands[i][2] : Octave Band centre frequency. Hz
        bands[i][3] : Octave Band lower frequency. Hz
        bands[i][4] : Octave Band upper frequency. Hz

    Returns
    -------
    gwaves : stream 
        Obspy G weighted waveform stream in Infrasound Pressure. Pa
        One trace per filter band.
        
        Stats updated in each trace:
            st[i].stats.max = maximum amplitude as float
            st[i].stats.mean = mean (or average) amplitude as float
            st[i].stats.rms = root mean squared (RMS) amplitude as float

    """


