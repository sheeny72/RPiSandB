# 3D Report featuring Specific Energy Plot
from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime, Stream
from obspy.signal import filter
# from obspy import read_inventory      # remove comment if using local inventory files
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.gridspec as gs
import numpy as np
from obspy.taup import TauPyModel
import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
rs = Client('https://data.raspberryshake.org/')

# Pretty paired colors. Reorder to have saturated colors first and remove
# some colors at the end. This cmap is compatible with obspy taup
cmap = plt.get_cmap('Paired', lut=12)
COLORS = ['#%02x%02x%02x' % tuple(int(col * 255) for col in cmap(i)[:3]) for i in range(12)]
COLORS = COLORS[1:][::2][:-1] + COLORS[::2][:-1]
def plot_arrivals(ax, d1):
    y1 = -1
    axb, axt = ax.get_ylim()               # calculate the y limits of the graph
    for q in range(0, no_arrs):            #plot each arrival in turn
        x1 = arrs[q].time                  # extract the time to plot
        if (x1 >= delay):
            if x1 < delay+duration:
                ax.axvline(x=x1-d1, linewidth=0.7, linestyle='--', color=COLORS[q % len(COLORS)])      # draw a vertical line
                if y1 < 0 or y1 < axt/2:                      # alternate top and bottom for phase tags
                    y1 = axt*0.8
                else:
                    y1 = axb*0.95
                ax.text(x1-d1,y1,arrs[q].name, alpha=0.7, color=COLORS[q % len(COLORS)])     # print the phase name
    x1 = rayt       #plot the Rayleight Surface Wave arrival
    if (x1>=delay):
        if x1 < delay+duration:
            ax.axvline(x=x1-d1, linewidth=0.5, linestyle='--', color='black')      # draw a vertical line
            if y1 < 0 or y1 < axt/2:                      # alternate top and bottom for phase tags
                y1 = axt*0.8
            else:
                y1 = axb*0.95
            ax.text(x1-d1,y1,'Ray', alpha=0.5)            # print the phase name

def time2UTC(a):        # convert time (seconds) since event back to UTCDateTime
    return eventTime + a

def uTC2time(a):        # convert UTCDateTime to seconds since the event
    return a - eventTime

def one_over(a):            # 1/x to convert frequency to period
    # Vectorized 1/a, treating a==0 manually
    a = np.array(a).astype(float)
    near_zero = np.isclose(a, 0)
    a[near_zero] = np.inf
    a[~near_zero] = 1 / a[~near_zero]
    return a

inverse = one_over          # function 1/x is its own inverse

def plot_noiselims(ax, uplim, downlim):
    axl, axr = ax.get_xlim()
    ax.axhline(y=uplim, lw=0.33, color='r', linestyle='dotted')       # plot +1 SD
    ax.axhline(y=uplim*2, lw=0.33, color='r', linestyle='dotted')     # plot +2 SD
    ax.axhline(y=uplim*3, lw=0.33, color='r', linestyle='dotted')     # plot upper background noise limit +3SD
    ax.axhline(y=downlim, lw=0.33, color='r', linestyle='dotted')     # plot -1 SD
    ax.axhline(y=downlim*2, lw=0.33, color='r', linestyle='dotted')   # plot -2SD
    ax.axhline(y=downlim*3, lw=0.33, color='r', linestyle='dotted')   # plot lower background noise limit -3SD
    ax.text(axl, uplim*3,'3SD background', size='xx-small', color='r',alpha=0.5, ha='left', va='bottom')
    ax.text(axl, downlim*3, '-3SD background', size='xx-small', color='r', alpha=0.5, ha='left', va='top')

def plot_se_noiselims(ax, uplim):
    axl, axr = ax.get_xlim()
    ax.axhline(y=uplim, lw=0.33, color='r', linestyle='dotted')         # plot +1 SD
    ax.axhline(y=uplim*2*2, lw=0.33, color='r', linestyle='dotted')     # plot +2 SD
    ax.axhline(y=uplim*3*3, lw=0.33, color='r', linestyle='dotted')     # plot upper background noise limit +3SD
    ax.axhline(y=0, lw=0.33, color='r', linestyle='dotted')             # plot 0 limit in case data has no zero
    ax.text(axl, uplim*3*3,'3SD background', size='xx-small', color='r',alpha=0.5, ha='left', va='bottom')

def divTrace(tr, n):            # divide trace into n equal parts for background noise determination
    return tr.__div__(n)

#enter event data
eventTime = UTCDateTime(2024, 5, 25, 22, 23, 16) # (YYYY, m, d, H, M, S) **** Enter data****
latE = -17.1                                    # quake latitude + N -S **** Enter data****
lonE = 167.9                                    # quake longitude + E - W **** Enter data****
depth = 29                             # quake depth, km **** Enter data****
mag = 6.3                             # quake magnitude **** Enter data****
eventID = 'rs2024khwvdp'               # ID for the event **** Enter data****
locE = "Vanuatu Islands"      # location name **** Enter data****

# set the station name and download the response information
stn = 'R4FA0'      # your station name

""" use the following routine if using local inventory files
if stn == 'R4FA0':      #add stations with local response files here
    f = open('R4FA0.xml')
    inv = read_inventory("R4FA0.xml")
    f.close()
else:
    inv = rs.get_stations(network='AM', station=stn, level='RESP')  # get the instrument response
""" 
# comment out the following line if using local inventory files
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

notes1 = ""                       # add notes to the diagram.
notes2 = ""

# set up the traces and ray paths
plot_envelopes = False          # plot envelopes on traces
allphases = True   # true if all phases to be plotted, otherwise only those in the plotted time window are plotted **** Enter data****
save_plot = False   # Set to True when plot is readyto be saved

start = eventTime + delay       # calculate the plot start time from the event and delay
end = start + duration               # calculate the end time from the start and duration

# set background noise sample times (choose a section of minimum velocity amplitude to represent background noise)
bnS = 900             # enter time of start of background noise sample (default = 0) **** Enter data****
bnE = 600               # enter time of end of background noise sample (default = 600) **** Enter data****
bnstart = eventTime - bnS            
bnend = eventTime + bnE               

# bandpass filter - select to suit system noise and range of quake
#filt = [0.09, 0.1, 0.8, 0.9]
#filt = [0.29, 0.3, 0.8, 0.9]
#filt = [0.49, 0.5, 2, 2.1]
filt = [0.69, 0.7, 2, 2.1]       # distant quake
#filt = [0.69, 0.7, 3, 3.1]
#filt = [0.69, 0.7, 4, 4.1]
#filt = [0.69, 0.7, 6, 6.1]
#filt = [0.69, 0.7, 8, 8.1]
#filt = [.69, 0.7, 10, 10.1]
#filt = [.69, 0.7, 20, 20.1]
#filt = [2.9, 3, 20, 20.1]        # use for local quakes
#filt = [.69, 0.7, 49, 50]

# set the FDSN server location and channel names
channels = ['EHZ', 'EHE', 'EHN'] # ENx = accelerometer channels; EHx or SHZ = geophone channels

# get waveforms and copy it for independent removal of instrument response
st = Stream()
for ch in channels:
    trace = rs.get_waveforms('AM', stn, '00', ch, start, end)
    st += trace
st.merge(method=0, fill_value='latest')         # fill in any gaps in the data to prevent a crash
st.detrend(type='demean')                       # demean the data
rawstream = st.copy()            # save a raw copy of the traces for the spectrogram

# get waveforms for background noise and copy it for independent removal of instrument response
bnst = Stream()
for ch in channels:
    trace = rs.get_waveforms('AM', stn, '00', ch, start, end)
    bnst += trace
bnst.merge(method=0, fill_value='latest')         # fill in any gaps in the data to prevent a crash
bnst.detrend(type='demean')                       # demean the data

# calculate great circle angle of separation
# convert angles to radians
latSrad = math.radians(latS)
lonSrad = math.radians(lonS)
latErad = math.radians(latE)
lonErad = math.radians(lonE)

if lonSrad > lonErad:
    lon_diff = lonSrad - lonErad
else:
    lon_diff = lonErad - lonSrad

great_angle_rad = math.acos(math.sin(latErad)*math.sin(latSrad)+math.cos(latErad)*math.cos(latSrad)*math.cos(lon_diff))
great_angle_deg = math.degrees(great_angle_rad)     #great circle angle between quake and station
distance = great_angle_rad*12742/2      #calculate distance between quake and station in km

# Calculate the Phase Arrivals
model = TauPyModel(model='iasp91')
arrs = model.get_travel_times(depth, great_angle_deg)
print(arrs)             # print the arrivals for reference when setting delay and duration
no_arrs = len(arrs)     # the number of arrivals

# calculate Rayleigh Wave arrival Time
rayt = distance/2.96
print("Rayleigh Arrival Time: ", rayt)

# Calculate Earthquake Total Energy
qenergy = 10**(1.5*mag+4.8)

# Remove instrument response
st.remove_response(inventory=inv,pre_filt=filt,output='VEL',water_level=60, plot=False)

# Calculate maximums
e_max = st[0].max()
n_max = st[1].max()
z_max = st[2].max()
se_max = (z_max*z_max+e_max*e_max+n_max*n_max)/2

# Create background noise traces
bn = bnst.remove_response(inventory=inv,pre_filt=filt,output='VEL',water_level=60, plot=False)

# Calculate background noise limits using standard deviation
bnsamp = 15                             # sample size in seconds
bns = int((bnend - bnstart)/bnsamp)     # calculate the number of samples in the background noise traces
bnz = divTrace(bn[2],bns)               # divide the displacement background noise trace into equal traces
bne = divTrace(bn[0],bns)               # divide the velocity background noise trace into equal traces
bnn = divTrace(bn[1],bns)               # divide the acceleration background noise trace into equal traces
for j in range (0, bns):                # find the sample interval with the minimum background noise amplitude
    if j == 0:
        bnZstd = abs(bnz[j].std())
        bnEstd = abs(bne[j].std())
        bnNstd = abs(bnn[j].std())
    elif abs(bnz[j].std()) < bnZstd:
        bnZstd = abs(bnz[0].std())
    elif abs(bne[j].std()) < bnEstd:
        bnEstd = abs(bne[j].std())
    elif abs(bnn[j].std()) < bnNstd:
        bnNstd = abs(bnn[j].std())
bnsestd = (bnZstd*bnZstd+bnEstd*bnEstd+bnNstd*bnNstd)/2           # calculate the max background noise level for the specific energy

# Create Signal Envelopes
z_env = filter.envelope(st[2].data)     # create displacement envelope
e_env = filter.envelope(st[0].data)     # create velocity envelope
n_env = filter.envelope(st[1].data)     # create acceleration envelope
se_env=(z_env*z_env+e_env*e_env+n_env*n_env)/2    # create specific energy envelope from velocity envelope! - comment out undesired method.

# set up map plot
if great_angle_deg <5:      #set satellite height based on separation
    sat_height = 1000000
elif great_angle_deg <25:
    sat_height = 10000000
elif great_angle_deg >120:
    sat_height = 100000000000
elif great_angle_deg >90:
    sat_height = 1000000000
else:
    sat_height = 100000000
    
latC = (latE+latS)/2        # latitude 1/2 way between station and event/earthquake
lonC = (lonE+lonS)/2        # longitude 1/2 way between station and event/earthquake
if abs(lonE-lonS) > 180:
    lonC = lonC + 180
projection=ccrs.NearsidePerspective(
      central_latitude=latC,
      central_longitude=lonC,
      satellite_height=sat_height)      # adjust satellite height to best display station and event/earthquake
projection._threshold = projection._threshold/20    #reduce threshold so great circle lines are smooth

# set up plot
fig = plt.figure(figsize=(20,14), dpi=150)       # set to page size in inches
gsouter = gs.GridSpec(1, 3, width_ratios = [8, 3, 4], wspace = 0.15)
gsleft = gs.GridSpecFromSubplotSpec(8, 1, subplot_spec = gsouter[0], hspace = 0.5, wspace = 0.2)
gsmid = gs.GridSpecFromSubplotSpec(5, 1, height_ratios = [3,1,1,1,1], subplot_spec = gsouter[1], hspace = 0.5)
gsmt = gs.GridSpecFromSubplotSpec(3,2, subplot_spec = gsmid[0], hspace= 0.3, wspace = 0.2)
gsright = gs.GridSpecFromSubplotSpec(3, 1, subplot_spec = gsouter[2], height_ratios = [3, 2, 3], hspace = 0.1)
ax1 = fig.add_subplot(gsleft[0])            # EHZ
ax2 = fig.add_subplot(gsleft[1])            # EHZ Spectrogram
ax3 = fig.add_subplot(gsleft[2])            # EHN
ax4 = fig.add_subplot(gsleft[3])            # EHN Spectrogram
ax5 = fig.add_subplot(gsleft[4])            # EHE
ax6 = fig.add_subplot(gsleft[5])            # EHE Spectrogram
ax7 = fig.add_subplot(gsleft[6])            # Specific Energy
ax8 = fig.add_subplot(gsmt[0])              # Z/N polar
ax9 = fig.add_subplot(gsmt[2])              # Z/E polar
ax10 = fig.add_subplot(gsmt[4])             # N/E Polar
ax11 = fig.add_subplot(gsmid[2])            # PSD
ax12 = fig.add_subplot(gsmid[3])            # FFT
ax13 = fig.add_subplot(gsright[0], polar=True)              # TAUp plot
ax14 = fig.add_subplot(gsright[2], projection=projection)   # Map


fig.suptitle("M"+str(mag)+" Earthquake - "+locE+" - "+eventTime.strftime(' %d/%m/%Y %H:%M:%S UTC'), weight='black', color='b', size='x-large')      #Title of the figure
fig.text(0.05, 0.95, "Filter: "+str(filt[1])+" to "+str(filt[2])+"Hz")          # Filter details
fig.text(0.84, 0.48, 'Separation = '+str(round(great_angle_deg,3))+u"\N{DEGREE SIGN}"+' or '+str(int(distance))+'km.', ha = 'center', size='large')   #distance between quake and station
fig.text(0.84, 0.46, 'Latitude: '+str(latE)+u"\N{DEGREE SIGN}"+' Longitude: '+str(lonE)+u"\N{DEGREE SIGN}"+' Depth: '+str(depth)+'km.', ha = 'center', size='large')  #quake lat, lon and depth
fig.text(0.84, 0.44, 'Quake Energy: '+f"{qenergy:0.1E}"+'J. Equiv. to '+f"{qenergy/4.18e9:0.1E}"+' t TNT.', ha = 'center', size='large')        #Earthquake energy
fig.text(0.7, 0.95, 'Event ID: '+eventID)
fig.text(0.95, 0.95, 'Station: AM.'+stn, ha='right',size='large')
fig.text(0.95, 0.935, 'Raspberry Shake 3D', color='r', ha='right')
fig.text(0.95, 0.92, '#ShakeNet', ha='right',size='small')
fig.text(0.98, 0.905, '@raspishake', ha='right',size='small')
fig.text(0.98, 0.89, '@AlanSheehan18', ha='right',size='small')
fig.text(0.98, 0.875, '@matplotlib', ha='right',size='small')
fig.text(0.98, 0.86, '#Python', ha='right',size='small')
fig.text(0.98, 0.845, '#CitizenScience', ha='right',size='small')
fig.text(0.98, 0.83, '#Obspy', ha='right',size='small')
fig.text(0.98, 0.815, '#Cartopy', ha='right',size='small')
fig.text(0.53, 0.58, 'Particle Motion Plots\nstart blue and end red.')
fig.text(0.61, 0.72, 'Particle Motion Plots', size='large', rotation=90)

# plot logos
pics = "D:/Pictures/Raspberry Shake and Boom/2024/"
rsl = plt.imread("RS logo.png")
newaxr = fig.add_axes([0.935, 0.915, 0.05, 0.05], anchor='NE', zorder=-1)
newaxr.imshow(rsl)
newaxr.axis('off')

# perspective map viewing height
fig.text(0.84, 0.38, 'Satellite Viewing Height = '+str(int(sat_height/1000))+' km.', ha='center')

# print notes
fig.text(0.04, 0.05, 'NOTES:  '+notes1)                 # add any notes about the report **** Enter data****
fig.text(0.04, 0.03, notes2)                 # add any notes about the report **** Enter data****

# trace notes and maxima
#fig.text(0.48, 0.715, 'East / West', size='x-small',rotation=90, va='center')
#fig.text(0.485, 0.715, 'Velocity', size='x-small',rotation=90, va='center')
#fig.text(0.48, 0.87, 'Vertical', size='x-small',rotation=90, va='center')
#fig.text(0.485, 0.87, 'Velocity', size='x-small',rotation=90, va='center')
#fig.text(0.48, 0.56, 'North South', size='x-small',rotation=90, va='center')
#fig.text(0.485, 0.56, 'Velocity', size='x-small',rotation=90, va='center')
#fig.text(0.48, 0.41, 'E/m = v²/2', size='x-small',rotation=90, va='center')
#fig.text(0.485, 0.41, 'For weak arrivals', size='x-small',rotation=90, va='center')
fig.text(0.3, 0.12, 'Max Z = '+f"{z_max:.3E}"+' m/s', size='small',color='b')
fig.text(0.3, 0.11, 'Max E = '+f"{e_max:.3E}"+' m/s', size='small',color='g')
fig.text(0.3, 0.10, 'Max N = '+f"{n_max:.3E}"+' m/s', size='small',color='r')
fig.text(0.3, 0.09, 'Max SE = '+f"{se_max:.3E}"+' J/kg', size='small',color='purple')
#fig.text(0.48, 0.253, 'Unfiltered Spectrogram', size='x-small', rotation=90, va='center')

# print signal to noise ratios
fig.text(0.4, 0.12, 'S/N = '+f"{abs(z_max/(3*bnZstd)):.3}", size='x-small', color='b')
fig.text(0.4, 0.11, 'S/N = '+f"{abs(e_max/(3*bnEstd)):.3}", size='x-small', color='g')
fig.text(0.4, 0.10, 'S/N = '+f"{abs(n_max/(3*bnNstd)):.3}", size='x-small', color='r')
fig.text(0.4, 0.09, 'S/N = '+f"{abs(se_max/(3*bnsestd)):.3}", size='x-small', color='purple')

# print backgrround noise data
fig.text(0.04, 0.13, 'Background Noise:', size='small')
fig.text(0.04, 0.12, 'Z (vertical):', color='b', size='small')
fig.text(0.04, 0.11, 'SD = '+f"{bnZstd:.3E}"+' m/s', color='b', size='small')
fig.text(0.04, 0.10, '3SD = '+f"{(3*bnZstd):.3E}"+' m/s', color='b', size='small')
fig.text(0.04, 0.09, 'E (East/West):', color='g', size='small')
fig.text(0.04, 0.08, 'SD = '+f"{bnEstd:.3E}"+' m/s', color='g', size='small')
fig.text(0.04, 0.07, '3SD = '+f"{(3*bnEstd):.3E}"+' m/s', color='g', size='small')
fig.text(0.11, 0.12, 'N (North/South):', color='r', size='small')
fig.text(0.11, 0.11, 'SD = '+f"{bnNstd:.3E}"+' m/s', color='r', size='small')
fig.text(0.11, 0.10, '3SD = '+f"{(3*bnNstd):.3E}"+' m/s', color='r', size='small')
fig.text(0.11, 0.09, 'Specific Energy:', color='g', size='small')
fig.text(0.11, 0.08, 'SD = '+f"{bnsestd:.3E}"+' J/kg', color='g', size='small')
fig.text(0.11, 0.07, '3SD = '+f"{(3*bnsestd):.3E}"+' J/kg', color='g', size='small')
fig.text(0.18, 0.12, 'BN parameters:', size='small')
fig.text(0.18, 0.11, 'Minimum SD over:', size='small')
fig.text(0.18, 0.10, 'Start: Event time - '+str(bnS)+' s.',size='small')
fig.text(0.18, 0.09, 'End: Event time + '+str(bnE)+' s.',size='small')
fig.text(0.18, 0.08, 'BN Sample size = '+str(bnsamp)+' s.',size='small')

# plot traces
ax1.plot(st[0].times(reftime=eventTime), st[2].data, lw=1, color='b')      # displacement waveform
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax1.set_ylim(-2e-8,2e-8)         # set manual y limits for displacement- comment this out for autoscaling
ax1.margins(x=0)
ax3.plot(st[0].times(reftime=eventTime), st[0].data, lw=1, color='g')       # velocity Waveform
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax2.set_ylim(-1e-7,1e-7)         # set manual y limits for velocity - comment this out for autoscaling
ax3.margins(x=0)
ax5.plot(st[0].times(reftime=eventTime), st[1].data, lw=1, color='r')       # acceleration waveform
ax5.xaxis.set_minor_locator(AutoMinorLocator(10))
ax5.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax3.set_ylim(-5e-7,5e-7)         # set manual y limits for acceleration - comment this out for auto scaling
ax5.margins(x=0)
ax2.specgram(x=rawstream[2], NFFT=128, noverlap=64, Fs=100, cmap='viridis')         # velocity spectrogram
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.set_yscale('log')               # set logarithmic y scale - comment this out for linear scale
ax2.set_ylim(0.5,50)              # limits for log scale
# plot filter limits on spectrogram
ax2.axhline(y=filt[1], lw=1, color='r', linestyle='dotted')
ax2.axhline(y=filt[2], lw=1, color='r', linestyle='dotted')
ax4.specgram(x=rawstream[0], NFFT=128, noverlap=64, Fs=100, cmap='viridis')         # velocity spectrogram
ax4.xaxis.set_minor_locator(AutoMinorLocator(10))
ax4.set_yscale('log')               # set logarithmic y scale - comment this out for linear scale
ax4.set_ylim(0.5,50)              # limits for log scale
# plot filter limits on spectrogram
ax4.axhline(y=filt[1], lw=1, color='r', linestyle='dotted')
ax4.axhline(y=filt[2], lw=1, color='r', linestyle='dotted')
ax6.specgram(x=rawstream[1], NFFT=128, noverlap=64, Fs=100, cmap='viridis')         # velocity spectrogram
ax6.xaxis.set_minor_locator(AutoMinorLocator(10))
ax6.set_yscale('log')               # set logarithmic y scale - comment this out for linear scale
ax6.set_ylim(0.5,50)              # limits for log scale
# plot filter limits on spectrogram
ax6.axhline(y=filt[1], lw=1, color='r', linestyle='dotted')
ax6.axhline(y=filt[2], lw=1, color='r', linestyle='dotted')

ax7.plot(st[0].times(reftime=eventTime), (st[0].data*st[0].data+st[1].data*st[1].data+st[2].data*st[2].data)/2, lw=0.5, color='white', alpha = 0.5, linestyle=':')  #specific kinetic energy Waveform
ax7.xaxis.set_minor_locator(AutoMinorLocator(10))
ax7.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax7.set_ylim(0,5e-15)         # set manual y limits for energy - comment this out for autoscaling
ax7.margins(x=0)

# plot particle motion plots
n_lines = len(st[0].data)
cmap = plt.get_cmap('coolwarm')     #plots start blue and end red
for i in range(0, n_lines-1):
    mcolor = cmap(float(i)/float(n_lines))
    ax8.plot([st[1].data[i], st[1].data[i+1]], [st[2].data[i], st[2].data[i+1]], lw=0.5, color = mcolor)
    ax9.plot([st[0].data[i], st[0].data[i+1]], [st[2].data[i], st[2].data[i+1]], lw=0.5, color = mcolor)
    ax10.plot([st[0].data[i], st[0].data[i+1]], [st[1].data[i], st[1].data[i+1]], lw=0.5, color = mcolor)
# find maxima for each plot to scale x and y axes equally
max8 = max(abs(z_max), abs(n_max))
max9 = max(abs(e_max), abs(z_max))
max10 = max(abs(n_max), abs(e_max))
#adjust scale to correct for plot window size and shape
ax8.set_xlim(-max8*1.469, max8*1.469)
ax9.set_xlim(-max9*1.469, max9*1.469)
ax10.set_xlim(-max10*1.469, max10*1.469)
ax8.set_ylim(-max8, max8)
ax9.set_ylim(-max9, max9)
ax10.set_ylim(-max10, max10)
ax8b, ax8t = ax8.get_ylim()
ax8l, ax8r = ax8.get_xlim()
ax9b, ax9t = ax9.get_ylim()
ax9l, ax9r = ax9.get_xlim()
ax10b, ax10t = ax10.get_ylim()
ax10l, ax10r = ax10.get_xlim()
ax8.text(0.8*ax8l, 0.8*ax8t,'Z', va='center', ha='center')
ax8.text(0.8*ax8r, 0.8*ax8b,'N', va='center', ha='center')
ax9.text(0.8*ax9l, 0.8*ax9t,'Z', va='center', ha='center')
ax9.text(0.8*ax9r, 0.8*ax9b,'E', va='center', ha='center')
ax10.text(0.8*ax10l, 0.8*ax10t,'N', va='center', ha='center')
ax10.text(0.8*ax10r, 0.8*ax10b,'E', va='center', ha='center')


#plot either PSD or FFT plot
#calculate NFFT for PSD
if duration >= 82:
    nfft = 8192
else:
    nfft = duration*100
# ax5.psd(x=rawtrace[0], NFFT=512, noverlap=0, Fs=100, color='k', lw=1)      # velocity PSD raw data
ax11.psd(x=st[2], NFFT=nfft, noverlap=0, Fs=100, color='b', label='EHZ', alpha = 0.7, lw=0.5)             # displacement PSD filtered
ax11.psd(x=st[1], NFFT=nfft, noverlap=0, Fs=100, color='r', label='EHN', alpha = 0.7, lw=0.5)             # velocity PSD filtered
ax11.psd(x=st[0], NFFT=nfft, noverlap=0, Fs=100, color='g', label='EHE', alpha = 0.7, lw=0.5)             # acceleration PSD filtered
ax11.legend(fontsize='x-small')
ax11.set_xscale('log')               #use logarithmic scale on PSD
# plot filter limits on PSD
ax11.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
ax11.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
ax11.set_xlim(filt[1]*.8, int(filt[2]+1))
ax11.set_ylabel("PSD, dB",size='small')
ax11.set_xlabel("Frequency, Hz",size='small')
#ax11.xaxis.set_minor_locator(AutoMinorLocator(10))
ax11.yaxis.set_minor_locator(AutoMinorLocator(5))
secax_x11 = ax11.secondary_xaxis('top', functions=(one_over, inverse))        #PSD secondary axis
secax_x11.set_xlabel('P e r i o d ,   s', size='small', alpha=0.5, labelpad=0)

# fourier analysis plot
#rfft = np.fft.rfft(rawtrace[0].data)
ehzfft = np.fft.rfft(st[2].data)
ehnfft = np.fft.rfft(st[1].data)
ehefft = np.fft.rfft(st[0].data)
xfft = np.fft.rfftfreq(st[0].data.size, d = 1/100)
#ax12.plot(xfft, abs(rfft), color='k', lw=1, label='Unfiltered EHZ')
ax12.plot(xfft, abs(ehzfft), color='b', lw=0.5, alpha = 0.7, label='EHZ')
ax12.plot(xfft, abs(ehnfft), color='r', lw=0.5, alpha = 0.7, label='EHN')
ax12.plot(xfft, abs(ehefft), color='g', lw=0.5, alpha = 0.7, label='EHE')
ax12.legend(frameon=False, fontsize='x-small')
#ax12.set_xscale('log')               #use logarithmic scale on PSD
#ax12.set_yscale('linear')
#ax12.set_yscale('log')
#plot filter limits on PSD
ax12.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
ax12.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
if filt[2] >=4:
    fxt = filt[2]+0.5
else:
    fxt = filt[2]*1.1
ax12.set_xlim(filt[1]*.8, fxt)
ax12.set_ylabel("FFT",size='small')
ax12.set_xlabel("Frequency, Hz",size='small')
ax12.xaxis.set_minor_locator(AutoMinorLocator(10))
ax12.yaxis.set_minor_locator(AutoMinorLocator(10))
secax_x12 = ax12.secondary_xaxis('top', functions=(one_over, inverse))        #PSD secondary axis
secax_x12.set_xlabel('P e r i o d ,   s', size='small', alpha=0.5, labelpad=0)

#plot background noise limits
plot_noiselims(ax1, bnZstd, -bnZstd)      # EHZ noise limits - comment out if not desired
plot_noiselims(ax3, bnEstd, -bnEstd)      # EHN noise limits - comment out if not desired
plot_noiselims(ax5, bnNstd, -bnNstd)      # EHE noise limits - comment out if not desired
plot_se_noiselims(ax7, bnsestd)           # specific kinetic energy noise limits - comment out if not desired

# plot Signal envelopes
if plot_envelopes:
    ax1.plot(st[0].times(reftime=eventTime), z_env, 'b', lw = 0.5)    # EHZ envelope
    ax3.plot(st[0].times(reftime=eventTime), e_env, 'g', lw = 0.5)     # EHE envelope
    ax5.plot(st[0].times(reftime=eventTime), n_env, 'r', lw = 0.5)     # EHN envelope
# envelope for specific kinetic plot IS the specific energy graph.
# Energy is a scalar, so in vibrations alternates between kinetic and potential energy states.
ax7.plot(st[0].times(reftime=eventTime), se_env, 'purple', lw = 1, alpha = 0.5, label='Total')    # specific energy envelope
ax7.plot(st[0].times(reftime=eventTime), z_env*z_env/2, 'b', lw = 0.7, alpha = 0.5, label='EHZ')    # specific energy in vertical direction
ax7.plot(st[0].times(reftime=eventTime), n_env*n_env/2, 'r', lw = 0.7, alpha = 0.5, label='EHN')    # specific energy in North/South direction
ax7.plot(st[0].times(reftime=eventTime), e_env*e_env/2, 'g', lw = 0.7, alpha = 0.5, label='EHE')    # specific energy in East/West direction
ax7.legend(fontsize='x-small')

# plot secondary axes - set time interval (dt) based on the duration to avoid crowding
if duration <= 90:
    dt=10           #10 seconds
elif duration <= 180:
    dt=20           #20 seconds
elif duration <= 270:
    dt=30           #30 seconds
elif duration <= 540:
    dt=60           #1 minute
elif duration <= 1080:
    dt=120          #2 minutes
elif duration <= 2160:
    dt=240          #4 minutes
else:
    dt=300          #5 minutes
tbase = start - start.second +(int(start.second/dt)+1)*dt       # find the first time tick

# clear the first tick if it will overprint the Y axis scale factor
if tbase-start < duration/10:
    clear1tick = True
else:
    clear1tick = False
    
tlabels = []            #initialise a blank array of time labels
tticks = []             #initialise a blank array of time ticks
sticks = []           #initialise a blank array for spectrogram ticks
nticks = int(duration/dt)       #calculate the number of ticks
for k in range (0, nticks):
    if k==0 and clear1tick:
        tlabels.append('')
    elif dt >= 60:                #build the array of time labels - include UTC to eliminate the axis label
        tlabels.append((tbase+k*dt).strftime('%H:%M UTC'))      #drop the seconds if not required for readability
    else:
        tlabels.append((tbase+k*dt).strftime('%H:%M:%SUTC'))    #include seconds where required
    tticks.append(uTC2time(tbase+k*dt))                         #build the array of time ticks
    sticks.append(uTC2time(tbase+k*dt)-delay)                   #build the array of time ticks for the spectrogram
secax_x1 = ax1.secondary_xaxis('top')       #EHZ secondary axis
secax_x1.set_xticks(ticks=tticks)
secax_x1.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x1.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x3 = ax3.secondary_xaxis('top')       #EHN secondary axis
secax_x3.set_xticks(ticks=tticks)
secax_x3.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x3.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x5 = ax5.secondary_xaxis('top')       #EHE secondary axis
secax_x5.set_xticks(ticks=tticks)
secax_x5.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x5.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x2 = ax2.secondary_xaxis('top')      #spectrogram secondary axis
secax_x2.set_xticks(ticks=sticks)
secax_x2.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x2.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x4 = ax4.secondary_xaxis('top')      #spectrogram secondary axis
secax_x4.set_xticks(ticks=sticks)
secax_x4.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x4.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x6 = ax6.secondary_xaxis('top')      #spectrogram secondary axis
secax_x6.set_xticks(ticks=sticks)
secax_x6.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x6.xaxis.set_minor_locator(AutoMinorLocator(10))
secax_x7 = ax7.secondary_xaxis('top')       #Specific Energy secondary axis
secax_x7.set_xticks(ticks=tticks)
secax_x7.set_xticklabels(tlabels, size='small', va='center_baseline')
secax_x7.xaxis.set_minor_locator(AutoMinorLocator(10))

# add grid to graphs
ax1.grid(color='dimgray', ls = '-.', lw = 0.33)
ax2.grid(color='dimgray', ls = '-.', lw = 0.33)
ax3.grid(color='dimgray', ls = '-.', lw = 0.33)
ax4.grid(color='dimgray', ls = '-.', lw = 0.33)
ax5.grid(color='dimgray', ls = '-.', lw = 0.33)
ax6.grid(color='dimgray', ls = '-.', lw = 0.33)
ax7.grid(color='dimgray', ls = '-.', lw = 0.33)
ax11.grid(color='dimgray', ls = '-.', lw = 0.33)
ax12.grid(color='dimgray', ls = '-.', lw = 0.33)
ax1.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax2.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax3.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax4.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax5.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax6.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax7.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax11.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
ax12.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)

# plot map
ax14.coastlines(resolution='110m')
ax14.stock_img()
# Create a feature for States/Admin 1 regions at 1:50m from Natural Earth to display state borders
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax14.add_feature(states_provinces, edgecolor='gray')
ax14.gridlines()
# plot station position on map
ax14.plot(lonS, latS,
     color='red', marker='v', markersize=12, markeredgecolor='black',
     transform=ccrs.Geodetic(),
     )
# plot event/earthquake position on map
ax14.plot(lonE, latE,
     color='yellow', marker='*', markersize=20, markeredgecolor='black',
     transform=ccrs.Geodetic(),
     )
#plot dashed great circle line from event/earthquake to station
ax14.plot([lonS, lonE], [latS, latE],
     color='blue', linewidth=2, linestyle='--', 
     transform=ccrs.Geodetic(),
     )

# build array of arrival data
y2 = 0.93        # start near middle of page but maximise list space
dy = 0.01        # linespacing
fig.text(0.625, y2, 'Phase',size='xx-small')         # print headings
fig.text(0.65, y2, 'Time',size='xx-small')
fig.text(0.675, y2, 'UTC',size='xx-small')
pphases=[]          # create an array of phases to plot
pfile=''            # create phase names for filename
alf=1.0             # set default transparency
for i in range (0, no_arrs):                    #print data array
    y2 -= dy
    if arrs[i].time >= delay and arrs[i].time < (delay+duration):       # list entries in the plots are black
        alf=1.0
    else:                                                               # list entries not in plots are greyed out
        alf=0.5
    fig.text(0.625, y2, arrs[i].name, size='xx-small', alpha=alf)       # print phase name
    fig.text(0.65, y2, str(round(arrs[i].time,3))+'s', size='xx-small', alpha=alf)     # print arrival time
    arrtime = eventTime + arrs[i].time
    fig.text(0.675, y2, arrtime.strftime('%H:%M:%S'), size='xx-small', alpha=alf)
    if allphases or (arrs[i].time >= delay and arrs[i].time < (delay+duration)):      # build the array of phases
        pphases.append(arrs[i].name)
        pfile += ' '+arrs[i].name
y2 -= 2*dy        
fig.text(0.625, y2, str(no_arrs)+' arrivals total.', size='xx-small')     # print number of arrivals

print(pphases)      # print the phases to be plotted on ray path diagram

if allphases or (rayt >= delay and rayt <= (delay+duration)):
    y2 -= 2*dy
    fig.text(0.625, y2, 'Rayleigh', size='xx-small')
    y2 -= dy
    fig.text(0.625, y2, 'Surface Wave: '+str(round(rayt,1))+'s:', size='xx-small')
    arrtime = eventTime + rayt
    fig.text(0.675, y2, arrtime.strftime('%H:%M:%S UTC'), size='xx-small')
    
# print phase key
y2 = 0.62          # line spacing
fig.text(0.98, y2, 'Phase Key', size='small', ha='right')      # print heading
pkey = ['P:   compression wave', 'p:   strictly upward compression wave', 'S:   shear wave', 's:   strictly upward shear wave', 'K:   compression wave in outer core', 'I:   compression wave in inner core', 'c:   reflection off outer core', 'diff:   diffracted wave along core mantle boundary', 'i:   reflection off inner core', 'n:   wave follows the Moho (crust/mantle boundary)']
for i in range (0, 10):
    y2 -=dy
    fig.text(0.98, y2, pkey[i], size='x-small', ha='right')      # print the phase key

#plot phase arrivals
plot_arrivals(ax1,0)          # plot arrivals on EHZ plot
plot_arrivals(ax3,0)          # plot arrivals on EHN plot
plot_arrivals(ax5,0)          # plot arrivals on EHE plot
plot_arrivals(ax2,delay)      # plot arrivals on spectrogram plot
plot_arrivals(ax4,delay)      # plot arrivals on spectrogram plot
plot_arrivals(ax6,delay)      # plot arrivals on spectrogram plot
plot_arrivals(ax7,0)          # plot arrivals on energy plot

# set up some plot details
ax1.set_ylabel("EHZ Velocity, m/s", size='small')
ax1.set_xlabel('Seconds after Event, s', size='small', labelpad=0)
ax3.set_ylabel("EHE Velocity, m/s", size ='small')
ax3.set_xlabel('Seconds after Event, s', size='small', labelpad=0)
ax5.set_ylabel("EHN Velocity, m/s", size='small')         
ax5.set_xlabel('Seconds after Event, s', size='small', labelpad=0)
ax2.set_ylabel("EHZ Vel. Frequency, Hz", size='small')
ax2.set_xlabel('Seconds after Start of Trace, s', size='small', labelpad=0)
ax4.set_ylabel("EHE Vel. Frequency, Hz", size='small')
ax4.set_xlabel('Seconds after Start of Trace, s', size='small', labelpad=0)
ax6.set_ylabel("EHN Vel. Frequency, Hz", size='small')
ax6.set_xlabel('Seconds after Start of Trace, s', size='small', labelpad=0)
ax7.set_ylabel('Specific Energy, J/kg', size='small')
ax7.set_xlabel('Seconds after Event, s', size='small', labelpad=0)

# get the limits of the y axis so text can be consistently placed
ax2b, ax2t = ax2.get_ylim()
ax2.text(2, ax2t*0.6, 'Plot Start Time: '+start.strftime(' %d/%m/%Y %H:%M:%S.%f UTC (')+str(delay)+' seconds after event).', size='small')      # explain difference in x time scale
ax4b, ax4t = ax4.get_ylim()
ax4.text(2, ax4t*0.6, 'Plot Start Time: '+start.strftime(' %d/%m/%Y %H:%M:%S.%f UTC (')+str(delay)+' seconds after event).', size='small')      # explain difference in x time scale
ax6b, ax6t = ax6.get_ylim()
ax6.text(2, ax6t*0.6, 'Plot Start Time: '+start.strftime(' %d/%m/%Y %H:%M:%S.%f UTC (')+str(delay)+' seconds after event).', size='small')      # explain difference in x time scale

# adjust subplots for readability
plt.subplots_adjust(hspace=0.5, wspace=0.1, left=0.05, right=0.95, bottom=0.05, top=0.92)

#plot the ray paths
arrivals = model.get_ray_paths(depth, great_angle_deg, phase_list=pphases)      # calculate the ray paths
ax13 = arrivals.plot_rays(plot_type='spherical', ax=ax13, fig=fig, phase_list=pphases, show=False, legend=True)   #plot the ray paths
if allphases:
    fig.text(0.91, 0.71, 'Show All Phases', size='small')
else:
    fig.text(0.91, 0.71, 'Show Phases\nVisible in Traces', size='small')
if great_angle_deg > 103 and great_angle_deg < 143:
    ax13.text(great_angle_rad,6000, 'Station in P and\nS wave shadow', size='x-small', rotation=180-great_angle_deg, ha='center', va='center')
elif great_angle_deg >143:
    ax13.text(great_angle_rad,6000, 'Station in S\nwave shadow', size='x-small', rotation=180-great_angle_deg, ha='center', va='center')
    
# label Station
ax13.text(great_angle_rad,7000, stn, ha='center', va='center', alpha=.7, size='small', rotation= -great_angle_deg)
    
# add boundary depths
ax13.text(math.radians(315),5550, '660km', ha='center', va='center', alpha=.7, size='small', rotation=45)
ax13.text(math.radians(315),3300, '2890km', ha='center', va='center', alpha=.7, size='small', rotation=45)
ax13.text(math.radians(315),1010, '5150km', ha='center', va='center', alpha=.7, size='small', rotation=45)

# Annotate regions
ax13.text(0, 0, 'Solid\ninner\ncore',
        horizontalalignment='center', verticalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
ocr = (model.model.radius_of_planet -
       (model.model.s_mod.v_mod.iocb_depth +
        model.model.s_mod.v_mod.cmb_depth) / 2)
ax13.text(math.radians(180), ocr, 'Fluid outer core',
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
mr = model.model.radius_of_planet - model.model.s_mod.v_mod.cmb_depth / 2
ax13.text(math.radians(180), mr, 'Solid mantle',
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# create phase identifier for filename
if allphases:
    pfile = ' All'

# print filename on bottom left corner of diagram
filename = pics+'M'+str(mag)+'Quake '+locE+eventID+eventTime.strftime('%Y%m%d %H%M%S UTC'+stn+pfile+'.png')
fig.text(0.02, 0.01,filename, size='x-small')

#print standard text to copy for posting on Social Media (Twitter)
print('M'+str(mag)+' #earthquake '+locE+' detected on Raspberry Shake 3D (AM.'+stn+'.00.EH(ZNE)) @raspishake #python #CitizenScience #ShakeNet #Obspy @matplotlib #Cartopy #OCSN')

# save the final figure
if save_plot:
    plt.savefig(filename)

# show the final figure
plt.show()
