# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:19:54 2024

@author: al72
"""
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from matplotlib.ticker import AutoMinorLocator
#import numpy as np
import matplotlib.pyplot as plt
import RBoomGWeighting as gw

# define fdsn client to get data from
client = Client('https://data.raspberryshake.org/')

# define start and end times
eventTime = UTCDateTime(2024, 6, 19, 1, 13, 51) # (YYYY, m, d, H, M, S) **** Enter data****
delay = 0               #delay from event time to start of plot
start = eventTime + delay   #calculate the plot start time
duration = 30               #duration of plot in seconds
end = start + duration                # start plus plot duration in seconds (recommend a minimum of 10s)
daylightSavings = False
save_plot = True
oct13 = True    # True for 1/3 Octave analysis, False for Octave analysis
inside = False  # True to keep bands inside the filtered range, False to span the filtered range

# Name the Event
eventName = 'Quarry Blast at Oberon Quarries'       # Name for the Report
notes = ''      #add notes

# get data from the FSDN server and detrend it
STATION = "R21C0"               # station name
st = client.get_waveforms("AM", STATION, "00", "HDF", starttime=start, endtime=end, attach_response=True)
st.merge(method=0, fill_value='latest')
st.detrend(type="demean")
cmax = abs(st[0].max())     # maximum amplitude of raw counts

# get Instrument Response
inv = client.get_stations(network="AM", station=STATION, level="RESP")

# set up bandpass filter
flc = 0.5      #enter bandpass filter lower corner frequency
fuc = 20        #enter bandpass filter upper corner frequency
filt = [flc-0.01, flc, fuc, fuc+0.1]   

# remove instrument response now that raw trace has been processed
y = st.remove_response(inventory=inv,pre_filt=filt,output="DEF", water_level=60)

# calculate linear SPL

yspl = gw.pa2db(y[0].data)

#calculate linear Leq
yleq = gw.leq(yspl)

# calculate infrasound exposure level SEL
ysel = gw.sel(yspl)

# initialise arrays for FFTs
f_plot = []
y_mag_plot = []
ydB = []
ydBG = []
fftG = []

# calculate linear FFT
f_plot, y_mag_plot = gw.fftL(y, flc, fuc)

# Convert linear FFT to dBL
ydB = gw.fft2dBL(y_mag_plot)

# calculate G weighted ffT in dB(G)
ydBG = gw.dBL2dBG(f_plot, ydB)

# Convert G weighted FFT from db(G) back to Pa
#fftG, l2G = gw.dBG2PaG(f_plot, ydB, ydBG, flc, fuc)
fftG = gw.dBG2PaG(f_plot, ydB, ydBG, flc, fuc)

# find the linear waveform parameters
pmax = gw.peak(y[0])
splmax = gw.peakSPL(y[0])
pav = gw.average(y[0])
prms = gw.rms(y[0])

# Calculate octave or 1/3 octave bands
bands = []
if oct13:
    bands = gw.oct13Bands(flc, fuc, inside)
else:
    bands = gw.octBands(flc, fuc, inside)
#print(bands)

# Build a stream of waveforms filtered to each band
bwaves = gw.band_waveforms(y, bands)

# test sum the band filtered waveforms to compare to original
testwave = gw.sum_stream(bwaves)

# calculate G weighted SPL

tspl = gw.pa2db(testwave.data)

#calculate G weighted Leq
tleq = gw.leq(tspl)

# calculate infrasound exposure level SEL
tsel = gw.sel(tspl)

# calculate band G factors
bGf = gw.band_G_factors(f_plot, y_mag_plot, fftG, bands)

#calculate G weighted waveforms for each band
bGwaves = gw.band_G_waveforms(bwaves, bGf)

#estimate G weighted waveform
g_weighted_wave = gw.sum_stream(bGwaves)
#print(g_weighted_wave)

# calculate G weighted SPL

gspl = gw.pa2db(g_weighted_wave.data)

#calculate G weighted Leq
gleq = gw.leq(gspl)

# calculate infrasound exposure level SEL
gsel = gw.sel(gspl)

# calculate G weighted waveform parameters
pGmax = gw.peak(g_weighted_wave)
pGav = gw.average(g_weighted_wave)
pGrms = gw.rms(g_weighted_wave)
splGmax = gw.peakSPL(g_weighted_wave)

# plot charts
# set-up figure and subplots
fig = plt.figure(figsize=(18,12), dpi=150)    #18 x 12 inches
ax1 = fig.add_subplot(4,1,1)    #left top 2 high
ax2 = fig.add_subplot(4,1,2)    #left middle 2 high
ax3 = fig.add_subplot(4,1,3)    #right top 2 high
ax4 = fig.add_subplot(4,1,4)    #right middle 2 high

# plot the waveform
ax1.plot(y[0].times(reftime=start), y[0].data, lw=1, color='b', label='linear Pa')
ax1.plot(y[0].times(reftime=start), testwave.data, lw=1, color='g', alpha = 0.5, label='recon lin Pa')
ax1.plot(y[0].times(reftime=start), g_weighted_wave.data, lw=1, color='r', alpha=0.7, label='G weighted Pa')
ax1.set_ylabel('Infrasound, Pa')
ax1.legend(frameon=False, fontsize='x-small')
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
ax1.margins(x=0)

# plot the FFTs in Pascals
ax2.plot(f_plot, y_mag_plot, lw=1, color = 'b', label='linear')
ax2.plot(f_plot, fftG, lw=1, color = 'r', label='G weighted')
ax2.set_ylabel('FFT, Pa')
ax2.legend(frameon=False, fontsize='x-small')
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
ax2.set_xscale('log')
ax2.margins(x=0)

# plot bands on ax2
gw.plotBands(bands, ax2)

# plot the FFTsin dBL and dB(G)
ax3.plot(f_plot, ydB, lw=1, color = 'b', label='dBL', alpha=1)
ax3.set_ylabel('FFT, dB')
ax3.plot(f_plot, ydBG, lw=1, color='r', label='dB(G)', alpha=0.7)
ax3.legend(frameon=False, fontsize='x-small')
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.yaxis.set_minor_locator(AutoMinorLocator(5))
ax3.set_xscale('log')
ax3.margins(x=0)

# plot bands on ax3
gw.plotBands(bands, ax3)

# plot the time domain dBL and estimated dB(G)
ax4.plot(y[0].times(reftime=start), yspl, lw=1, color='b', label='dbL')
ax4.plot(y[0].times(reftime=start), tspl, lw=1, color='g', label='dbL')
ax4.plot(y[0].times(reftime=start), gspl, lw=1, color='r', alpha=0.7, label='dbG')
ax4.axhline(tleq, lw=1, color='g', linestyle='--', label = 'linear Leq')
ax4.axhline(tsel, lw=1, color='g', linestyle='-.', label = 'linear SEL')
ax4.axhline(gleq, lw=1, color='k', linestyle='--', label = 'G weighted Leq')
ax4.axhline(gsel, lw=1, color='k', linestyle='-.', label = 'G weighted SEL')
ax4.set_ylabel('Infrasound, dBL')
ax4.legend(frameon=False, fontsize='x-small')
ax4.xaxis.set_minor_locator(AutoMinorLocator(10))
ax4.yaxis.set_minor_locator(AutoMinorLocator(5))
ax4.margins(x=0)

# add grids to the plots
ax1.grid(color='dimgray', ls = '-.', lw = 0.33)
ax2.grid(color='dimgray', ls = '-.', lw = 0.33)
ax3.grid(color='dimgray', ls = '-.', lw = 0.33)
ax4.grid(color='dimgray', ls = '-.', lw = 0.33)
ax1.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax2.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax3.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax4.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)

# add text to report
if daylightSavings:
    dsc = 11
    dst = 'AEDT'
else:
    dsc=10 
    dst = 'AEST'
    
fig.suptitle('Infrasound Report: '+eventName+' - '+eventTime.strftime('%d/%m/%Y %H:%M:%S.%f UTC'), size='xx-large',color='b')
fig.text(0.12, 0.945, 'Start: '+start.strftime('%d/%m/%Y %H:%M:%S UTC')+'   '+(start+dsc*3600).strftime('%d/%m/%Y %H:%M:%S '+dst))
fig.text(0.12, 0.93, 'End: '+end.strftime('%d/%m/%Y %H:%M:%S UTC')+'   '+(end+dsc*3600).strftime('%d/%m/%Y %H:%M:%S '+dst))
fig.text(0.12, .915, 'Station: AM.'+STATION+'.00.HDF')
fig.text(0.12, 0.9, 'Bandpass Filter: '+str(flc)+' to '+str(fuc)+' Hz.')
fig.text(0.12, 0.885, 'Notes: '+notes, size='small')
fig.text(0.88, 0.72, 'Peak Pressure = '+str(round(pmax,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right', alpha=0.7)    #report the peak Pressure
fig.text(0.88, 0.735, 'Est. Peak G weighted Pressure = '+str(round(pGmax,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right', color='r', alpha=0.7)    #report the peak G weighted pressure
fig.text(0.5, 0.72, 'Average Pressure = '+str(round(pav,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='center', alpha=0.7)    #report the average Pressure
fig.text(0.5, 0.735, 'Average G weighted Pressure = '+str(round(pGav,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='center', color='r', alpha=0.7)    #report the average G weighted Pressure
fig.text(0.14, 0.72, 'RMS Pressure = '+str(round(prms,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='left', alpha=0.7)    #report the RMS Pressure
fig.text(0.14, 0.735, 'G weighted RMS Pressure = '+str(round(pGrms,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='left', color='r', alpha=0.7)    #report the G weighted RMS Pressure
fig.text(0.88, 0.14, 'Peak Infrasound Pressure Level ='+str(round(splmax,1))+' dBL. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right', alpha=0.7)   #report peak sound pressure level
fig.text(0.88, 0.155, 'Estimated Peak Infrasound Pressure Level ='+str(round(splGmax,1))+' dB(G). ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right', alpha=0.7)   #report peak sound pressure level
fig.text(0.14, 0.14, 'Leq = '+str(round(tleq,1))+' dB.', alpha=0.7, color='g')
fig.text(0.14, 0.155, 'Leq = '+str(round(gleq,1))+' dB(G).', alpha=0.7, color='r')
fig.text(0.22, 0.14, 'SEL = '+str(round(tsel,1))+' dB.', alpha=0.7, color='g')
fig.text(0.22, 0.155, 'SEL = '+str(round(gsel,1))+' dB(G).', alpha=0.7, color='r')
fig.text(0.9, 0.945, 'Raspberry Shake and Boom', size='small', ha='right', color='r')
fig.text(0.9, 0.935, '@AlanSheehan18', size='small', ha='right')
fig.text(0.9, 0.925, '@raspishake', size='small', ha='right')
fig.text(0.9, 0.915, 'Oberon Citizen Science Network (OCSN)', size='small', ha='right')
fig.text(0.9, 0.905, '#CitizenScience', size='small', ha='right')
fig.text(0.9, 0.895,'https://github.com/sheeny72/RPiSandB', size='x-small', ha='right')

#print filename on bottom left corner of diagram
path = "D:/Pictures/Raspberry Shake and Boom/2024/"      # Edit to suit **** Enter data****
filename = path+'IR-'+STATION+eventName+start.strftime('%Y%m%d %H%M%S UTC')+str(flc)+'-'+str(fuc)+'-'+str(duration)
fig.text(0.1, 0.1,filename+'.png', size='x-small')

# save the final figure if the plot is ready
if save_plot:
    plt.savefig(filename+'.png')

# show the final figure
plt.show()

gw.band_stream_plot(bwaves, eventName+' - '+eventTime.strftime('%d/%m/%Y %H:%M:%S.%f UTC'), 'Linear Waveforms', save_plot, filename)
gw.band_stream_plot(bGwaves, eventName+' - '+eventTime.strftime('%d/%m/%Y %H:%M:%S.%f UTC'), 'G Weighted Waveforms', save_plot, filename)