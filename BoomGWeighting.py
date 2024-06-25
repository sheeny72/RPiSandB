# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:19:54 2024

@author: al72
"""
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import matplotlib.pyplot as plt

# define fdsn client to get data from
client = Client('https://data.raspberryshake.org/')

# define start and end times
eventTime = UTCDateTime(2024, 6, 19, 1, 13, 51) # (YYYY, m, d, H, M, S) **** Enter data****
delay = 0               #delay from event time to start of plot
start = eventTime + delay   #calculate the plot start time
duration = 40               #duration of plot in seconds
end = start + duration                # start plus plot duration in seconds (recommend a minimum of 10s)
daylightSavings = False
save_plot = False

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
fuc = 49        #enter bandpass filter upper corner frequency
filt = [flc-0.01, flc, fuc, fuc+0.1]   

# remove instrument response now that raw trace has been processed
y = st.remove_response(inventory=inv,pre_filt=filt,output="DEF", water_level=60)

fs = 100    # sampling frequency
tstep = 1/fs    # sample time interval
f0 = 10     #signal frequency
ns = len(y[0].data)   #number of samples

t = np.linspace(0, (ns-1)*tstep, ns)    # time steps
fstep = fs / ns     # frequency interval
f = np.linspace(0, (ns-1)*fstep, ns)     #frequency steps

# FFT
yfft = np.fft.fft(y[0].data)
y_mag = np.abs(yfft)/ns     #normalise the FFT

f_plot = f[0:int(ns/2+1)]
y_mag_plot = 2*y_mag[0:int(ns/2+1)]
y_mag_plot[0] = y_mag_plot[0]/2     # do not multiply DC value

#calculate maximum sound pressure level
pmax = abs(y[0].max())   #find the max pressure amplitude
splmax = 10*np.log10(pmax*pmax) + 93.979400087        #convert to sound pressure level

# Convert FFT to dB(L)
ydB = []
FFTsum = 0
for i in range (0, len(y_mag_plot.data)):
    ydB.append(20*np.log10(abs(y_mag_plot[i])/0.00002))

# Convert DB(L) to dB(G)
ydBG = []
for i in range (0, len(ydB)):
    if f_plot[i] == 0:
        ydBG.append(ydB[i+1]+34.142*np.log(f_plot[i+1])-41.332)
    elif f_plot[i] < 1:
        ydBG.append(ydB[i]+34.142*np.log(f_plot[i])-41.332)
    elif f_plot[i] <= 3.15:
        ydBG.append(ydB[i]-1.7406*f_plot[i]**4+15.961*f_plot[i]**3-55.565*f_plot[i]**2+95.938*f_plot[i]-97.475)
    elif f_plot[i] < 12.5:
        ydBG.append(ydB[i]+17.396*np.log(f_plot[i])-40.037)
    elif f_plot[i] <= 20:
        ydBG.append(ydB[i]-.0976*f_plot[i]**2+3.8393*f_plot[i]-28.738)
    elif f_plot[i] < 31.5:
        ydBG.append(ydB[i]-.0108*f_plot[i]**2-.5724*f_plot[i]+24.782)
    else:
        ydBG.append(ydB[i]+.0076*f_plot[i]**2-1.4868*f_plot[i]+35.262)

# convert db(G) back to G weighted FFT in Pa
fftG = []
l2G = 0
j = 0
for i in range (0, len(ydB)):
    fftG.append(0.00002*10**(ydBG[i]/20))
    if f_plot[i] >= flc and f_plot[i] < fuc:
        l2G += ydB[i] - ydBG[i]
        j += 1

# estimated Linear to G weighted overall correction
l2G = l2G/j     #average difference between ydB and ydBG over the bandpass filter range

# plot charts
# set-up figure and subplots
fig = plt.figure(figsize=(18,12), dpi=150)    #18 x 12 inches
ax1 = fig.add_subplot(4,1,1)    #left top 2 high
ax2 = fig.add_subplot(4,1,2)    #left middle 2 high
ax3 = fig.add_subplot(4,1,3)    #right top 2 high
ax4 = fig.add_subplot(4,1,4)    #right middle 2 high

# plot the waveform
ax1.plot(y[0].times(reftime=start), y[0].data, lw=1, color='k')
ax1.set_ylabel('Infrasound, Pa')
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
ax1.margins(x=0)

# plot the FFTs in Pascals
ax2.plot(f_plot, y_mag_plot, lw=1, color = 'b', label='linear')
ax2.plot(f_plot, fftG, lw=1, color = 'r', label='G weighted')
ax2.set_ylabel('FFT, Pa')
ax2.legend()
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
#ax2.set_yscale('log')
ax2.margins(x=0)

# plot the FFTsin dBL and dB(G)
ax3.plot(f_plot, ydB, lw=1, color = 'g', label='dBL')
ax3.set_ylabel('FFT, dB')
ax3.plot(f_plot, ydBG, lw=1, color='r', label='dB(G)')
ax3.legend()
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.yaxis.set_minor_locator(AutoMinorLocator(5))
#ax3.set_yscale('log')
ax3.margins(x=0)

# plot the time domain dBL and estimated dB(G)
ax4.plot(y[0].times(reftime=start), 20*np.log10(abs(y[0].data)/0.00002), lw=1, color='purple', label='dbL')
ax4.plot(y[0].times(reftime=start), 20*np.log10(abs(y[0].data)/0.00002)-l2G, lw=1, color='r', label='dB(G)')
ax4.set_ylabel('Infrasound, dBL')
ax4.legend()
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
fig.text(0.88, 0.73, 'Peak Pressure = '+str(round(pmax,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right')    #report the peak Pressure
fig.text(0.88, 0.14, 'Peak Infrasound Pressure Level ='+str(round(splmax,1))+' dBL. ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right')   #report peak sound pressure level
fig.text(0.88, 0.155, 'Estimated Peak Infrasound Pressure Level ='+str(round(splmax-l2G,1))+' dB(G). ('+str(filt[1])+" to "+str(filt[2])+"Hz)", ha='right')   #report peak sound pressure level
fig.text(0.9, 0.945, 'Raspberry Shake and Boom', size='small', ha='right', color='r')
fig.text(0.9, 0.935, '@AlanSheehan18', size='small', ha='right')
fig.text(0.9, 0.925, '@raspishake', size='small', ha='right')
fig.text(0.9, 0.915, 'Oberon Citizen Science Network (OCSN)', size='small', ha='right')
fig.text(0.9, 0.905, '#CitizenScience', size='small', ha='right')
fig.text(0.9, 0.895,'https://github.com/sheeny72/RPiSandB', size='x-small', ha='right')

#print filename on bottom left corner of diagram
path = "D:/Pictures/Raspberry Shake and Boom/2024/"      # Edit to suit **** Enter data****
filename = path+'IR-'+STATION+eventName+start.strftime('%Y%m%d %H%M%S UTC')+str(flc)+'-'+str(fuc)+'-'+str(duration)+'.png'
fig.text(0.1, 0.1,filename, size='x-small')

# save the final figure if the plot is ready
if save_plot:
    plt.savefig(filename)

# show the final figure
plt.show()