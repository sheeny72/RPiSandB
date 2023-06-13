from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import AutoMinorLocator

def time2UTC(a):        #convert time (seconds) since event back to UTCDateTime
    return eventTime + a

def uTC2time(a):        #convert UTCDateTime to seconds since the event
    return a - eventTime

def one_over(a):            # 1/x to convert frequency to period
    #Vectorized 1/a, treating a==0 manually
    a = np.array(a).astype(float)
    near_zero = np.isclose(a, 0)
    a[near_zero] = np.inf
    a[~near_zero] = 1 / a[~near_zero]
    return a

inverse = one_over          #function 1/x is its own inverse

def power_units(a):
    if a >= 1000000:
        return str(round(a/1000000,3))+'MW. ('
    elif a>=1000:
        return str(round(a/1000,3))+'kW. ('
    else:
        return str(round(a,3))+'W. ('

def energy_units(a):
    if a >= 1000000:
        return str(round(a/1000000,3))+'MJ. ('
    elif a>=1000:
        return str(round(a/1000,3))+'kJ. ('
    else:
        return str(round(a,3))+'J. ('

# define start and end times
eventTime = UTCDateTime(2022, 7, 8, 21, 5, 0) # (YYYY, m, d, H, M, S)
delay = 1050               #delay from event time to start of plot
start = eventTime + delay   #calculate the plot start time
duration = 200               #duration of plot in seconds
end = start + duration                # start plus plot duration in seconds (recommend a minimum of 10s)

# Name the Event
eventName = 'SpaceX Dragon Crew 1 Trunk Re-Entry'       # Name for the Report
distancem = 370000                    #enter distance in metres! Enter 0 to omit.
if distancem <=0:
    distance = 'unknown'
else:
    distance = str(distancem/1000)+' kms.'    #distance to the source in kms
notes1 = ''  #add notes about event if desired
notes2 = ''  #add more notes if req'd

# set up bandpass filter
filt = [0.49, 0.5, 10, 10.1]   #edit filter values to suit

#Ready to Save the Plot?
saveFig = False

# define fdsn client to get data from
client = Client('https://data.raspberryshake.org/')

# get data from the FSDN server and detrend it
STATION = "R21C0"               # station name
st = client.get_waveforms("AM", STATION, "00", "HDF", starttime=start, endtime=end, attach_response=True)
st.merge(method=0, fill_value='latest')
st.detrend(type="demean")
cmax = abs(st[0].max())     # maximum amplitude of raw counts

# get Instrument Response
inv = client.get_stations(network="AM", station=STATION, level="RESP")

# set-up figure and subplots
fig = plt.figure(figsize=(18,12), dpi=150)    #18 x 12 inches
ax1 = fig.add_subplot(6,2,(1,3))    #left top 2 high
ax2 = fig.add_subplot(6,2,(5,7))    #left middle 2 high
ax3 = fig.add_subplot(6,2,(2,4))    #right top 2 high
ax4 = fig.add_subplot(6,2,(6,8))    #right middle 2 high
ax5 = fig.add_subplot(6,2,(9,11))   #left bottom 2 high
ax6 = fig.add_subplot(6,2,10)    #right bottom +1
ax7 = fig.add_subplot(6,2,12)    #right bottom
fig.suptitle(eventName+' - '+eventTime.strftime('%d/%m/%Y %H:%M:%S.%f UTC'), size='xx-large',color='b')
fig.text(0.1, 0.94, 'Distance: '+distance)
fig.text(0.05, 0.04, 'NOTES: '+notes1, size='small')
fig.text(0.05, 0.025, notes2, size='small')
fig.text(0.93, 0.94, 'Station: AM.'+STATION+'.00.HDF Channel', size='small', rotation=90, va='top')
fig.text(0.94, 0.94, 'Raspberry Shake and Boom', size='small', rotation=90, va='top', color='r')
fig.text(0.95, 0.94, '@AlanSheehan18', size='small', rotation=90, va='top')
fig.text(0.93, 0.025, '#Python', size='small', rotation=90, va='bottom')
fig.text(0.94, 0.025, '#MatPlotLib', size='small', rotation=90, va='bottom')
fig.text(0.95, 0.025, '#Obspy', size='small', rotation=90, va='bottom')
fig.text(0.93, 0.5, '#CitizenScience', size='small', rotation=90, va='center')
fig.text(0.94, 0.5, '@raspishake', size='small', rotation=90, va='center')
fig.text(0.95, 0.5, '#ShakeNet', size='small', rotation=90, va='center')

# plot the raw curve
ax1.plot(st[0].times(reftime=eventTime), st[0].data, lw=1)
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
ax1.margins(x=0)

#plot the PSD
#calculate NFFT for PSD
if duration >= 82:
    nfft = 8192
else:
    nfft = duration*100

ax2.psd(x=st[0], NFFT=nfft, noverlap=0, Fs=100, color='r', lw=1, label='Raw Counts')
ax2.set_xscale('log')
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))

#plot spectrogram
ax5.specgram(x=st[0], NFFT=256, noverlap=128, Fs=100, cmap='plasma')
ax5.xaxis.set_minor_locator(AutoMinorLocator(10))
ax5.yaxis.set_minor_locator(AutoMinorLocator(5))
ax5.set_yscale('log')
ax5.set_ylim(0.5,50)

# record filter settings
fig.text(0.55, 0.94,'Bandpass Filter: '+str(filt[1])+' to '+str(filt[2])+' Hz.')
         
# remove instrument response now that raw trace has been processed
resp_removed = st.remove_response(inventory=inv,pre_filt=filt,output="DEF", water_level=60)

#copy resp_removed to integrate to calculate the energy of the event
et = resp_removed.copy()
et[0].data = et[0].data*et[0].data/397.2
et[0].integrate(method='cumtrapz')
aemax = abs(et[0].max())
if distancem >0:            #calculate the energy of the event if the distance is known
    emax = aemax*4*math.pi*distancem*distancem

# plot the filtered and corrected, and dB curves
ax2.psd(x=resp_removed[0], NFFT=nfft, noverlap=0, Fs=100, color='g', lw=1, label='Filtered Pa')
ax2.legend(frameon=False, fontsize='x-small')
ax3.plot(st[0].times(reftime=eventTime), resp_removed[0].data, lw=1, color='g')
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.yaxis.set_minor_locator(AutoMinorLocator(5))
ax3.margins(x=0)
ax4.plot(st[0].times(reftime=eventTime), 20*np.log10(abs(resp_removed[0].data)/0.00002))
ax4.xaxis.set_minor_locator(AutoMinorLocator(10))
ax4.yaxis.set_minor_locator(AutoMinorLocator(5))
ax4.margins(x=0)
ax6.plot(st[0].times(reftime=eventTime), resp_removed[0].data*resp_removed[0].data/397.2, lw=1, color = 'r')
ax6.xaxis.set_minor_locator(AutoMinorLocator(10))
ax6.yaxis.set_minor_locator(AutoMinorLocator(5))
ax6.margins(x=0)
ax7.plot(st[0].times(reftime=eventTime), et[0].data, lw=1, color = 'g')
ax7.xaxis.set_minor_locator(AutoMinorLocator(10))
ax7.yaxis.set_minor_locator(AutoMinorLocator(5))
ax7.margins(x=0)

#calculate maximum sound pressure level sound intensity and source power
pmax = abs(resp_removed[0].max())   #find the max pressure amplitude
splmax = 10*np.log10(pmax*pmax) + 93.979400087        #convert to sound pressure level
sintensity = pmax*pmax/397.2    #calculate the sound intensity, W/m/m
if distancem >0:        #calculate the power of the event if the distance is known
    spower = sintensity*4*math.pi*distancem*distancem      #calculate the sound power at the source in W for a point source

#plot secondary axes - set time interval (dt) based on the duration to avoid crowding
if duration <= 9:
    dt=1           #1 seconds
elif duration <= 18:
    dt=2           #2 seconds
elif duration <= 45:
    dt=5           #5 seconds
elif duration <= 90:
    dt=10           #10 seconds
elif duration <= 180:
    dt=20          #20 seconds
elif duration <= 270:
    dt=30          #30 seconds
elif duration <= 540:
    dt=60           #1 minute
elif duration <= 1080:
    dt=120          #2 minutes
else:
    dt=300          #5 minutes
tbase = start - start.second +(int(start.second/dt)+1)*dt       #find the first time tick

#clear the first tick if it will overprint the Y axis scale factor
if tbase-start < duration/10:
    clear1tick = True
else:
    clear1tick = False
    
tlabels = []            #initialise a blank array of time labels
tticks = []             #initialise a blank array of time ticks
sticks = []           #initialise a blank array for spectrogram ticks
nticks = int(duration/dt)+1       #calculate the number of ticks
for k in range (0, nticks):
    if k==0 and clear1tick:
        tlabels.append('')
    elif dt >= 60:                #build the array of time labels - include UTC to eliminate the axis label
        tlabels.append((tbase+k*dt).strftime('%H:%M UTC'))      #drop the seconds if not required for readability
    else:
        tlabels.append((tbase+k*dt).strftime('%H:%M:%SUTC'))    #include seconds where required
    tticks.append(uTC2time(tbase+k*dt))                         #build the array of time ticks
    sticks.append(uTC2time(tbase+k*dt)-delay)                   #build the array of time ticks for the spectrogram
secax_x1 = ax1.secondary_xaxis('top')       #Raw counts secondary axis
secax_x1.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x1.set_xticks(ticks=tticks)
secax_x1.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x1.set_xlabel('UTC', size='small', labelpad=1)
secax_x2 = ax2.secondary_xaxis('top', functions=(one_over, inverse))        #PSD secondary axis
secax_x2.set_xlabel('Period, s', size='small', labelpad=-6)
secax_x3 = ax3.secondary_xaxis('top')       #Pascals secondary axis
secax_x3.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x3.set_xticks(ticks=tticks)
secax_x3.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x3.set_xlabel('UTC', size='small', labelpad=1)
secax_x4 = ax4.secondary_xaxis('top')       #dB secondary axis
secax_x4.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x4.set_xticks(ticks=tticks)
secax_x4.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x4.set_xlabel('UTC', size='small', labelpad=1)
secax_x5 = ax5.secondary_xaxis('top')       #Spectrogram secondary axis
secax_x5.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x5.set_xticks(ticks=sticks)
secax_x5.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x5.set_xlabel('UTC', size='small', labelpad=1)
secax_x6 = ax6.secondary_xaxis('top')       #Intensity secondary axis
secax_x6.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x6.set_xticks(ticks=tticks)
secax_x6.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x6.set_xlabel('UTC', size='small', labelpad=1)
secax_x7 = ax7.secondary_xaxis('top')       #Energy secondary axis
secax_x7.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x7.set_xticks(ticks=tticks)
secax_x7.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x7.set_xlabel('UTC', size='small', labelpad=1)

# set-up some plot details
ax1.set_ylabel("Raw Counts")
ax2.set_ylabel("Power Spectral Density")
ax2.set_xlabel('Frequency,Hz',labelpad=-4)
ax3.set_ylabel("Pressure (Pa) ("+str(filt[1])+" to "+str(filt[2])+"Hz)")
ax4.set_ylabel("Infrasound Pressure Level (dB) ("+str(filt[1])+" to "+str(filt[2])+"Hz)", size='small')
ax5.set_ylabel("Frequency, Hz", size='small')
ax6.set_ylabel("Infrasound Intensity (W/m²)\n("+str(filt[1])+" to "+str(filt[2])+"Hz)", size='small')
ax7.set_ylabel("Energy (J/m²)\n("+str(filt[1])+" to "+str(filt[2])+"Hz)", size='small')
ax1.set_xlabel("Seconds after event", size='small', labelpad=0)
ax3.set_xlabel("Seconds after event", size='small', labelpad=0)
ax4.set_xlabel("Seconds after event", size='small', labelpad=0)
ax5.set_xlabel("Seconds after start", size='small', labelpad=0)
ax6.set_xlabel("Seconds after event", size='small', labelpad=0)
ax7.set_xlabel("Seconds after event", size='small', labelpad=0)

ax1.grid(color='dimgray', ls = '-.', lw = 0.33)
ax2.grid(color='dimgray', ls = '-.', lw = 0.33)
ax3.grid(color='dimgray', ls = '-.', lw = 0.33)
ax4.grid(color='dimgray', ls = '-.', lw = 0.33)
#ax5.grid(color='dimgray', ls = '-.', lw = 0.33)
ax6.grid(color='dimgray', ls = '-.', lw = 0.33)
ax7.grid(color='dimgray', ls = '-.', lw = 0.33)
ax1.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax2.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax3.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax4.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
#ax5.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax6.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax7.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)

# Report Peak Calculated Values
fig.text(0.11, 0.69, 'Peak Count = '+str(int(cmax)))
fig.text(0.55, 0.69, 'Peak Pressure = '+str(round(pmax,3))+'Pa. ('+str(filt[1])+" to "+str(filt[2])+"Hz)")    #report the peak Pressure
fig.text(0.55, 0.39, 'Peak Infrasound Pressure Level ='+str(round(splmax,1))+'dB. ('+str(filt[1])+" to "+str(filt[2])+"Hz)")   #report peak sound pressure level
fig.text(0.55, 0.3, 'Peak Infrasound Intensity = '+f"{sintensity:.3}"+' W/m². ('+str(filt[1])+" to "+str(filt[2])+"Hz)")
fig.text(0.55, 0.15, 'Total Energy = '+f"{aemax:.3}"+' J/m².')
if distancem >0:        #display the power and energy if the distance is known
    fig.text(0.55, 0.285, 'Peak Source Infrasound Power = '+power_units(spower)+str(filt[1])+" to "+str(filt[2])+"Hz)")
    fig.text(0.55, 0.135, 'Total Energy = '+energy_units(emax)+str(filt[1])+" to "+str(filt[2])+"Hz)")

# get the limits of the y axis so text can be consistently placed
ax5b, ax5t = ax5.get_ylim()
ax5.text(2, ax5t*0.7, 'Plot Start Time: '+start.strftime(' %d/%m/%Y %H:%M:%S.%f UTC '))      # explain difference in x time scale

#adjust subplots for readability
plt.subplots_adjust(hspace=0.7, wspace=0.13, right=0.92, left=0.1, top=0.92, bottom=0.08)

# save the final figure
if saveFig:
    plt.savefig('D:\Pictures\Raspberry Shake and Boom\\'+eventName+STATION+' HDF '+start.strftime('%Y%m%d %H%M%S UTC'))  #comment this line out till figure is final

# show the final figure
plt.show()
