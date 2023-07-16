# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 10:41:35 2023

@author: al72
"""

from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime, Stream
import matplotlib.pyplot as plt

rs = Client('https://data.raspberryshake.org/')

def maxbt(mb, mt, ab, at):
    if mb > ab:
        mb = ab
    if mt < at:
        mt = at
    return (mb, mt)
         
#enter event data
eventTime = UTCDateTime(2023, 7, 2, 10, 27, 43) # (YYYY, m, d, H, M, S) **** Enter data****
latE = -17.9                           # quake latitude + N -S **** Enter data****
lonE = -174.9                        # quake longitude + E - W **** Enter data****
depth = 229                             # quake depth, km **** Enter data****
mag = 6.9                              # quake magnitude **** Enter data****
eventID = 'rs2023mwwzcd'               # ID for the event **** Enter data****
locE = "Tonga Islands"                # location name **** Enter data****

# set the station name and download the response information
stn = 'RB59E'      # your station name
inv = rs.get_stations(network='AM', station=stn, level='RESP')  # get the instrument response
k=0
while True:     #loop until the active epoch is found
    sta = inv[0][k]         #station metadata
    staOK = sta.is_active(time=eventTime)
    if staOK:
        break
    k += 1
latS = sta.latitude      # station latitude
lonS = sta.longitude     # station longitude
eleS = sta.elevation     # station elevation
      
# Setup the data plot
delay = 200                  # delay the start of the plot from the event **** Enter data****
duration = 900                  # duration of plots **** Enter data****

start = eventTime + delay       # calculate the plot start time from the event and delay
end = start + duration               # calculate the end time from the start and duration

# bandpass filter - select to suit system noise and range of quake
#filt = [0.09, 0.1, 0.8, 0.9]
#filt = [0.29, 0.3, 0.8, 0.9]
#filt = [0.49, 0.5, 2, 2.1]
filt = [0.69, 0.7, 2, 2.1]       # distant quake
#filt = [0.69, 0.7, 3, 3.1]
#filt = [0.69, 0.7, 4, 4.1]
#filt = [0.69, 0.7, 6, 6.1]
#filt = [0.69, 0.7, 8, 8.1]
#filt = [.99, 1, 10, 10.1]
#filt = [.99, 1, 20, 20.1]
#filt = [2.9, 3, 20, 20.1]        # use for local quakes

# set the FDSN server location and channel names
channels = ['EHZ', 'EHE', 'EHN'] # ENx = accelerometer channels; EHx or SHZ = geophone channels

colours = ['b', 'r', 'g']   # Define colours for the traces in the stream

# get waveforms and copy it for independent removal of instrument response
st = Stream()
k = 0
for ch in channels:
    trace = rs.get_waveforms('AM', stn, '00', ch, start, end)
    trace[0].stats.color = colours[k]   #save a new colour for each trace
    k += 1
    st += trace
st.merge(method=0, fill_value='latest')         # fill in any gaps in the data to prevent a crash
st.detrend(type='demean')                       # demean the data

# Remove instrument response
st.remove_response(inventory=inv,pre_filt=filt,output='VEL',water_level=60, plot=False)

# set up plot
fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)
ax1.plot(st[0].times(reftime=eventTime), st[2], color=st[2].stats.color, label = 'AM.'+stn+'.00.'+st[2].stats.channel)
ax2.plot(st[0].times(reftime=eventTime), st[1], color=st[1].stats.color, label = 'AM.'+stn+'.00.'+st[1].stats.channel)
ax3.plot(st[0].times(reftime=eventTime), st[0], color=st[0].stats.color, label = 'AM.'+stn+'.00.'+st[0].stats.channel)
# Identify each trace
ax1.legend()
ax2.legend()
ax3.legend()
# Maximiise plotwidth in each subplot
ax1.margins(x=0)
ax2.margins(x=0)
ax3.margins(x=0)
# Hide the xtick labels on the top 2 subplots
ax1.set_xticks([])
ax2.set_xticks([])

#set equal Y scales for all traces
maxb, maxt = ax1.get_ylim()
axb, axt = ax2.get_ylim()
maxb, maxt = maxbt(maxb, maxt, axb, axt)
axb, axt = ax3.get_ylim()
mab, maxt = maxbt(maxb, maxt, axb, axt)
ax1.set_ylim(maxb,maxt)
ax2.set_ylim(maxb,maxt)
ax2.set_ylim(maxb,maxt)   

# adjust subplots for readability
fig.subplots_adjust(hspace=0)   #, wspace=0.1, left=0.05, right=0.95, bottom=0.05, top=0.92)

plt.show()