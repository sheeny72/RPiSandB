from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime, Stream
from obspy.signal import cross_correlation
import matplotlib.pyplot as plt
rs = Client('RASPISHAKE')
xc = cross_correlation

# set the station name and download the response information
stn = 'R21C0'                            # your station name
inv = rs.get_stations(network='AM', station=stn, level='RESP')

print (inv)

# set data start/end times
start = UTCDateTime(2023, 3, 27, 0, 13, 0) # (YYYY, m, d, H, M, S.ffffff)
end = start + 60     # end = start + duration in seconds (S.ffffff)

# set the FDSN server location and channel names
channels = ['EHZ' , 'HDF'] # ENx = accelerometer channels; EHx or SHZ = geophone channels

# get waveforms and put them all into one Stream
stream = Stream()
for ch in channels:
        trace = rs.get_waveforms('AM', stn, '00', ch, start, end)
        stream += trace
stream.merge(method=0, fill_value='latest')
stream.detrend(type='demean')

print(stream)

#get instrument response
inv = rs.get_stations(network="AM", station=stn, level="RESP")

# setup figure and subplots
fig = plt.figure(figsize=(12,12))
ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2)
ax3 = fig.add_subplot(4,1,3)
ax4 = fig.add_subplot(4,1,4)
fig.suptitle("AM."+stn+" RS&B Cross Channel Correlation Report: "+start.strftime('%d/%m/%Y %H:%M:%S.%f UTC'))

# plot raw traces
ax1.plot(stream[0].times(reftime=start), stream[0].data, lw=1, color='g')
ax2.plot(stream[0].times(reftime=start), stream[1].data, lw=1)

# calculate cross correlation
s = 10     # shift in data points each side to test
cc = xc.correlate(stream[0], stream[1], s)    
print(cc)         # print correlations for each shift value
shift, value = xc.xcorr_max(cc)     #find the max correlation and shift
print(shift, round(value,3))

# get the limits of the y axis so text can be consistently placed
ax2b, ax2t = ax2.get_ylim()

#add the correlation to the plot
ax2.text(0, ax2t*0.8, 'Raw Shift = '+str(shift)+'/100 s. Correlation Coefficient ='+str(round(value,3)))

# set up filter
filt = [0.3, 0.5, 10, 12]   #edit filter values to suit

# remove instrument response and add new traces to the stream
stream += stream[0].remove_response(inventory=inv,pre_filt=filt,output="VEL", water_level=60)
stream += stream[1].remove_response(inventory=inv,pre_filt=filt,output="DEF", water_level=60)

# plot filtered traces
ax3.plot(stream[0].times(reftime=start), stream[2].data, lw=1, color='r')
ax4.plot(stream[0].times(reftime=start), stream[3].data, lw=1, color='b')

#calculate cross correlation of filtered traces
cc1 = xc.correlate(stream[2], stream[3], s)    
print(cc1)         # print correlations for each shift value
shift1, value1 = xc.xcorr_max(cc1)     #find the max correlation and shift
print(shift1, round(value1,3))

# get ax4 y axis limits so text can be consistently placed
ax4b, ax4t = ax4.get_ylim()

#add the correlation to the plot
ax4.text(0, ax4t*0.8, 'Filtered Shift = '+str(shift1)+'/100 s. Correlation Coefficient ='+str(round(value1,3)))

# setup some plot details
ax1.set_ylabel("EHZ Raw Counts")
ax2.set_ylabel("HDF Raw Counts")         
ax3.set_ylabel("EHZ Velocity (m/s) ("+str(filt[1])+" to "+str(filt[2])+"Hz)")
ax4.set_ylabel("HDF Pascals (Pa) ("+str(filt[1])+" to "+str(filt[2])+"Hz)")

# save the final figure
#plt.savefig(stn+' RSandB Corr'+start.strftime('%Y%m%d %H%M%S UTC'))  #comment this line out till figure is final

# show the final figure
plt.show()


