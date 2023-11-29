# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:52:26 2023

@author: al72
"""

# Spectrum comparison for the Raspberry Shake and Boom

from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np

rs = Client('https://data.raspberryshake.org/')

# Channel 1 data
startTime1 = UTCDateTime(2023, 11, 27, 1, 0, 0) # (YYYY, m, d, H, M, S) **** Enter data****

# set the station name and download the response information
stn1 = 'R21C0'      # station name
nw1 = 'AM'          # network name
#ch1 = ['*HZ', 'DISP', 'm.', 'Displacement']
#ch1 = ['*HZ', 'VEL', 'm/s.', 'Velocity']
#ch1 = ['*HZ', 'ACC', 'm/s².', 'Acceleration']
ch1 = ['HDF', 'DEF', 'Pa.', 'Pressure']
inv1 = rs.get_stations(network=nw1, station=stn1, level='RESP')  # get the instrument response
notes1 = 'R21C0 Oberon'

# Channel 2 data
startTime2 = UTCDateTime(2023, 11, 27, 1, 0, 0) # (YYYY, m, d, H, M, S) **** Enter data****

# set the station name and download the response information
stn2 = 'R571C'      # station name
nw2 = 'AM'          # network name
#ch2 = ['*HZ', 'DISP', 'm.', 'Displacement']
#ch2 = ['*HZ', 'VEL', 'm/s.', 'Velocity']
#ch2 = ['*HZ', 'ACC', 'm/s².', 'Acceleration']
ch2 = ['HDF', 'DEF', 'Pa.', 'Pressure']
inv2 = rs.get_stations(network=nw2, station=stn2, level='RESP')  # get the instrument response
notes2 = 'R571C Coonabarabran'
      
#Setup the data plot
duration = 3600               # duration of plots in seconds **** Enter data****
end1 = startTime1 + duration
end2 = startTime2 + duration
filtered = True        # True to apply a frequency bandpass filter
logspect = False        # True to display logarithmic spectrogram Y axes

#Infrasund Filter bands
filt = [0.04, 0.05, 49, 50]   # For Booms with 20s mechanical filter fitted
#filt = [0.04, 0.05, 1, 1.1]
#filt = [0.09, 1, 49, 50]      # For all Booms...
#filt = [0.9, 1, 10, 10.1]
#filt = [9.9, 10, 20, 20.1]
#filt = [19.9, 20, 30, 30.1]
#filt = [29.9, 30, 40, 40.1]
#filt = [39.9, 40, 49, 50]

#seismic filter bands
#filt = [0.04, 0.05, 49, 50]
#filt = [0.69, 0.7, 2, 2.1]
#filt = [0.69, 0.7, 10, 10.1]
#filt = [0.69, 0.7, 20, 20.1]
#filt = [0.69, 0.7, 49, 50]


# calculate spectrum plot limits if filtered
if filtered:
    if filt[2] >=4:
        fxt = filt[2]+1
    else:
        fxt = filt[2]*1.25
    if filt[1] >= 2:
        fxb = filt[1]-1
    else:
        fxb = filt[1]*0.75
else:
    fxt = 50
    fxb = 0.05

# get and process the waveforms
trace1 = rs.get_waveforms(nw1, stn1, '00', ch1[0], startTime1, end1)
trace1.merge(method=0, fill_value='latest')         #fill in any gaps in the data to prevent a crash
trace1.detrend(type='demean')                       #demean the data
raw1 = trace1.copy()
trace1.remove_response(inventory=inv1,pre_filt=filt,output=ch1[1],water_level=60, plot=False)

trace2 = rs.get_waveforms(nw2, stn2, '00', ch2[0], startTime2, end2)
trace2.merge(method=0, fill_value='latest')         #fill in any gaps in the data to prevent a crash
trace2.detrend(type='demean')                       #demean the data
raw2 = trace2.copy()
trace2.remove_response(inventory=inv2,pre_filt=filt,output=ch2[1],water_level=60, plot=False)

# set up plot
fig = plt.figure(figsize=(20,14), dpi=150)       # set to page size in inches
ax1 = fig.add_subplot(5, 2, 1)      # waveform 1 plot
ax2 = fig.add_subplot(5, 2, 2)      # waveform 2 plot
ax3 = fig.add_subplot(5, 2, 3)      # waveform 1 spectrogram
ax4 = fig.add_subplot(5, 2, 4)      # waveform 2 spectrogram
ax5 = fig.add_subplot(5, 2, (5,6))      # PSD plots
ax6 = fig.add_subplot(5, 2, (7,8))      # FFT plots
ax7 = fig.add_subplot(5, 2, (9,10))     # FFT difference plot

#plot traces
if filtered:
    ax1.plot(trace1[0].times(reftime=startTime1), trace1[0].data, lw=1, color='b')      # displacement waveform
    ax2.plot(trace2[0].times(reftime=startTime2), trace2[0].data, lw=1, color='g')
    ax1.set_ylabel(ch1[3]+', '+ch1[2],size='small')
    ax2.set_ylabel(ch2[3]+', '+ch2[2],size='small')
else:
    ax1.plot(raw1[0].times(reftime=startTime1), raw1[0].data, lw=1, color='b')      # displacement waveform
    ax2.plot(raw2[0].times(reftime=startTime2), raw2[0].data, lw=1, color='g')
    ax1.set_ylabel(ch1[3]+', counts.',size='small')
    ax2.set_ylabel(ch2[3]+', counts.',size='small')
ax1.margins(x=0)
ax2.margins(x=0)

# document max amplitudes
if filtered:
    max1 = trace1.max()
    max2 = trace2.max()
    units1 = ch1[2]
    units2 = ch2[2]
else:
    max1 = raw1.max()
    max2 = raw2.max()
    units1 = 'Counts'
    units2 = 'Counts'
ax1l, ax1r = ax1.get_xlim()
ax2l, ax2r = ax2.get_xlim()
ax1b, ax1t = ax1.get_ylim()
ax2b, ax2t = ax2.get_ylim()
ax1.text(ax1r*0.02, ax1t*0.8, 'Max amplitude = '+f"{abs(max1[0]):0.3E}"+units1)
ax2.text(ax2r*0.02, ax2t*0.8, 'Max amplitude = '+f"{abs(max2[0]):0.3E}"+units2)

#plot spectrograms
ax3.specgram(x=raw1[0], NFFT=256, noverlap=128, Fs=100, cmap='plasma')         # velocity spectrogram
ax3.set_ylabel(ch1[3]+' Spectrogram',size='small')
ax4.specgram(x=raw2[0], NFFT=256, noverlap=128, Fs=100, cmap='plasma')         # velocity spectrogram
ax4.set_ylabel(ch2[3]+' Spectrogram',size='small')
if filtered:    # plot filter limits
    ax3.axhline(y=filt[1], lw=1, color='w', linestyle='dotted')
    ax3.axhline(y=filt[2], lw=1, color='w', linestyle='dotted')
    ax4.axhline(y=filt[1], lw=1, color='w', linestyle='dotted')
    ax4.axhline(y=filt[2], lw=1, color='w', linestyle='dotted')
if logspect:
    ax3.set_yscale('log')
    ax4.set_yscale('log')
ax4.set_ylim(0.05, 50)

#plot PSD
#calculate NFFT for PSD
if duration >= 82:
    nfft = 8192
else:
    nfft = duration*100
if filtered:
    ax5.psd(x=trace1[0], NFFT=nfft, noverlap=0, Fs=100, color='b', lw=1, label=nw1+'.'+stn1+'.00.'+ch1[0]+' '+ch1[1])      
    ax5.psd(x=trace2[0], NFFT=nfft, noverlap=0, Fs=100, color='g', lw=1, label=nw2+'.'+stn2+'.00.'+ch2[0]+' '+ch2[1])
    #plot filter limits on PSD
    ax5.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
    ax5.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
else:
    ax5.psd(x=raw1[0], NFFT=nfft, noverlap=0, Fs=100, color='b', lw=1, label=nw1+'.'+stn1+'.00.'+ch1[0]+' '+ch1[1])      
    ax5.psd(x=raw2[0], NFFT=nfft, noverlap=0, Fs=100, color='g', lw=1, label=nw2+'.'+stn2+'.00.'+ch2[0]+' '+ch2[1])
ax5.set_xlim(fxb, fxt)
#ax5.set_ylim(-290, -130)
ax5.legend(frameon=False, fontsize='x-small')
#ax5.set_xscale('log')               #use logarithmic scale on PSD
#ax5.set_yscale('linear')
#ax5.set_yscale('log')
ax5.set_ylabel("PSD, dB",size='small')
ax5.set_xlabel('F r e q u e n c y ,   H z', size='small', alpha=0.5, labelpad=-9)
ax5.xaxis.set_minor_locator(AutoMinorLocator(10))


# fourier analysis plot
if filtered:
    fft1 = np.fft.rfft(trace1[0].data)
    fft2 = np.fft.rfft(trace2[0].data)
    xfft = np.fft.rfftfreq(trace1[0].data.size, d = 1/100)
    # plot filter limits on FFT
    ax6.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
    ax6.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
else:
    fft1 = np.fft.rfft(raw1[0].data)
    fft2 = np.fft.rfft(raw2[0].data)
    xfft = np.fft.rfftfreq(raw1[0].data.size, d = 1/100)  
ax6.set_xlim(fxb, fxt)
ax6.plot(xfft, abs(fft1), color='b', lw=1, label=nw1+'.'+stn1+'.00.'+ch1[0]+' '+ch1[1])
ax6.plot(xfft, abs(fft2), color='g', lw=1, label=nw2+'.'+stn2+'.00.'+ch2[0]+' '+ch2[1])
#ax6.legend(frameon=False, fontsize='x-small')
#ax6.set_xscale('log')               #use logarithmic scale on FFT
#ax6.set_yscale('linear')
#ax6.set_yscale('log')
ax6.set_ylabel("FFT Spectrum",size='small')
ax6.set_xlabel('F r e q u e n c y ,   H z', size='small', alpha=0.5, labelpad=0)
ax6.xaxis.set_minor_locator(AutoMinorLocator(10))

# fourier difference plot
dfft = abs(fft1) - abs(fft2)
ax7.plot(xfft, abs(dfft), color='r', lw=1, label='FFT Difference')
#ax7.legend(frameon=False, fontsize='x-small')
ax7.margins(x=0)
if filtered:
    ax7.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='b')
    ax7.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='b')
ax7.set_xlim(fxb, fxt)
#ax7.set_xscale('log')               #use logarithmic scale on FFT Difference
ax7.set_ylabel("FFT Spectrum Difference",size='small')
ax7.set_xlabel('F r e q u e n c y ,   H z', size='small', alpha=0.5, labelpad=0)
ax7.xaxis.set_minor_locator(AutoMinorLocator(10))

# Calculate Trend Lines
# Note high order polynomial fits may generate Rank Warnings for poor fit conditioning.
# Visually check the fit in these cases. If not acceptable reduce/adjust torder until
# fit is aceptable or Rank Warning disappears.
n = len(xfft)
trx = []
#tr1 = []
#tr2 = []
trd = []
torder = 15     #enter polynomial order for trend line

for i in range(0,n):
    if xfft[i] >= filt[1] and xfft[i] <= filt[2]:   # only use data in the filter range!
        trx.append(xfft[i])
        #tr1.append(fft1[i])
        #tr2.append(fft2[i])
        trd.append(dfft[i])

#z1 = np.polyfit(trx, tr1, torder)
#z2 = np.polyfit(trx, tr2, torder)
zd = np.polyfit(trx, trd, torder)   # max polynomial trend line ... visually check fit especially if a rank warning is issued!
zav = np.polyfit(trx, trd, 0)       # order 0 = constant = average
zlin = np.polyfit(trx, trd, 1)      # order 1 = linear ... general trend.

#tl1 = np.poly1d(z1)
#tl2 = np.poly1d(z2)
tld = np.poly1d(zd)
tlav = np.poly1d(zav)
tllin = np.poly1d(zlin)

#ax6.plot(trx, abs(tl1(trx)), color = 'r', lw = 2, linestyle = 'dotted', label = 'FFT Blue Trend')
#ax6.plot(trx, abs(tl2(trx)), color = 'purple', lw = 2, linestyle = 'dotted', label = 'FFT Green Trend')
ax7.plot(trx, abs(tld(trx)), color = 'k', lw = 2, linestyle = 'dotted', label = 'FFT Difference Trend (order = '+str(torder)+')')
ax7.plot(trx, abs(tlav(trx)), color = 'b', lw = 2, linestyle = 'dotted', label = 'FFT Mean = '+f"{tlav.c[0]:0.3E}")
if tllin.c[1] < 0:
    tlt = 'x - '
else:
    tlt = 'x + '
ax7.plot(trx, abs(tllin(trx)), color = 'g', lw = 2, linestyle = 'dotted', label = 'FFT y = '+f"{tllin.c[0]:0.3E}"+tlt+f"{abs(tllin.c[1]):0.3E}")
ax6.legend(frameon=False, fontsize='x-small')
ax7.legend(frameon=False, fontsize='x-small')


fig.suptitle("FFT Signal Comparison", weight='black', color='b', size='x-large')      #Title of the figure
fig.text(0.13, 0.94, nw1+'.'+stn1+'.00.'+ch1[0]+'.')
fig.text(0.13, 0.93, 'Start time = '+startTime1.strftime(' %d/%m/%Y %H:%M:%S UTC'))
fig.text(0.13, 0.92, 'Duration = '+str(duration)+' seconds.')
if filtered:
    fig.text(0.13, 0.91, 'Filter = '+str(filt[1])+' to '+str(filt[2])+' Hz.')
else:
    fig.text(0.13, 0.91, 'Raw Counts, Unfiltered.')
fig.text(0.13, 0.9, notes1)
    
fig.text(0.55, 0.94, nw2+'.'+stn2+'.00.'+ch2[0]+'.')
fig.text(0.55, 0.93, 'Start time = '+startTime2.strftime(' %d/%m/%Y %H:%M:%S UTC'))
fig.text(0.55, 0.92, 'Duration = '+str(duration)+' seconds.')
if filtered:
    fig.text(0.55, 0.91, 'Filter = '+str(filt[1])+' to '+str(filt[2])+' Hz.')
else:
    fig.text(0.55, 0.91, 'Raw Counts, Unfiltered.')
fig.text(0.55, 0.9, notes2)