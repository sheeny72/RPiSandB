from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy.signal import filter
#from obspy import read_inventory
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

def plot_arrivals(ax, d1, pt, pb, bottoff):
    y1 = -1
    axb, axt = ax.get_ylim()           # calculate the y limits of the graph
    for q in range(0, no_arrs):        #plot each arrival in turn
        x1 = arrs[q].time              # extract the time to plot
        if (x1 >= delay):
            if x1 < delay+duration:
                ax.axvline(x=x1-d1, linewidth=1, linestyle='--', color=COLORS[q % len(COLORS)])      # draw a vertical line
                if y1 < 0 or y1 < axt/2:                      # alternate top and bottom for phase tags
                    y1 = axt*pt
                else:
                    if bottoff:
                        y1 = axt*0.1
                    else:
                        y1 = axb*pb
                ax.text(x1-d1,y1,arrs[q].name, alpha=1, color=COLORS[q % len(COLORS)])                              # print the phase name
    x1 = rayt       #plot the Rayleigh Surface Wave arrival
    if (x1>=delay):
        if x1 < delay+duration:
            ax.axvline(x=x1-d1, linewidth=0.5, linestyle='--', color='k')      # draw a vertical line
            if y1 < 0 or y1 < axt/2:                      # alternate top and bottom for phase tags
                y1 = axt*pt
            else:
                if bottoff:
                    y1 = axt*0.1
                else:
                    y1 = axb*pb
            ax.text(x1-d1,y1,'Ray', alpha=0.5)   # print the phase name
    x1 = lovet       #plot the Love Surface Wave arrival
    if (x1>=delay):
        if x1 < delay+duration:
            ax.axvline(x=x1-d1, linewidth=0.5, linestyle='--', color='k')      # draw a vertical line
            if y1 < 0 or y1 < axt/2:                      # alternate top and bottom for phase tags
                y1 = axt*pt
            else:
                if bottoff:
                    y1 = axt*0.1
                else:
                    y1 = axb*pb
            ax.text(x1-d1,y1,'Love', alpha=0.5)   # print the phase name

def time2UTC(a):        #convert time (seconds) since event back to UTCDateTime
    return eventTime + a

def uTC2time(a):        #convert UTCDateTime to seconds since the event
    return a - eventTime

def one_over(a):        # 1/x to convert frequency to period
    #Vectorized 1/a, treating a==0 manually
    a = np.array(a).astype(float)
    near_zero = np.isclose(a, 0)
    a[near_zero] = np.inf
    a[~near_zero] = 1 / a[~near_zero]
    return a

inverse = one_over      #function 1/x is its own inverse

def plot_noiselims(ax, uplim, downlim):
    axl, axr = ax.get_xlim()
    ax.axhline(y=uplim, lw=0.33, color='r', linestyle='dotted')     #plot +1 SD
    ax.axhline(y=uplim*2, lw=0.33, color='r', linestyle='dotted')     #plot +2 SD
    ax.axhline(y=uplim*3, lw=0.33, color='r', linestyle='dotted')     #plot upper background noise limit +3SD
    ax.axhline(y=downlim, lw=0.33, color='r', linestyle='dotted')   #plot -1 SD
    ax.axhline(y=downlim*2, lw=0.33, color='r', linestyle='dotted')   #plot -2SD
    ax.axhline(y=downlim*3, lw=0.33, color='r', linestyle='dotted')   #plot lower background noise limit -3SD
    ax.text(axl, uplim*3,'3SD background', size='xx-small', color='r',alpha=0.5, ha='left', va='bottom')
    ax.text(axl, downlim*3, '-3SD background', size='xx-small', color='r', alpha=0.5, ha='left', va='top')

def plot_se_noiselims(ax, uplim):
    axl, axr = ax.get_xlim()
    ax.axhline(y=uplim, lw=0.33, color='r', linestyle='dotted')     #plot +1 SD
    ax.axhline(y=uplim*2*2, lw=0.33, color='r', linestyle='dotted')     #plot +2 SD
    ax.axhline(y=uplim*3*3, lw=0.33, color='r', linestyle='dotted')     #plot upper background noise limit +3SD
    ax.axhline(y=0, lw=0.33, color='r', linestyle='dotted')         #plot 0 limit in case data has no zero
    ax.text(axl, uplim*3*3,'3SD background', size='xx-small', color='r',alpha=0.5, ha='left', va='bottom')

def divTrace(tr, n):            #divide trace into n equal parts for background noise determination
    return tr.__truediv__(n)

def fmtax(ax, lim, noneg):  #pass axis, 0 for auto y scaling or manual limit, True if no negatives in plot i.e. Specific energy
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.margins(x=0)
    grid(ax)
    if lim!=0:
        if noneg:
            ax.set_ylim(0, lim)
        else:
            ax.set_ylim(-lim, lim)         # set manual y limits for displacement- comment this out for autoscaling

def grid(ax):   #pass axis
    ax.grid(color='dimgray', ls = '-.', lw = 0.33)
    ax.grid(color='dimgray', which='minor', ls = ':', lw = 0.33)
 
def sax(secax, tix):    #pass secondary axis, and ticks
    secax.set_xticks(ticks=tix)
    secax.set_xticklabels(tlabels, size='small', va='center_baseline')
    secax.xaxis.set_minor_locator(AutoMinorLocator(10))

#enter event data
eventTime = UTCDateTime(2025, 4, 22, 10, 17, 13) # (YYYY, m, d, H, M, S) **** Enter data****
latE = 4.5                                   # quake latitude + N -S **** Enter data****
lonE = 127.8                                     # quake longitude + E - W **** Enter data****
depth = 118                             # quake depth, km **** Enter data****
mag = 6.2                             # quake magnitude **** Enter data****
eventID = 'rs2025hwoboz'               # ID for the event **** Enter data****
locE = "Talaud Islands, Indonesia"      # location name **** Enter data****

# set the station name and download the response information
stn = 'R21C0'      # station name
#stn = 'R5968'      # station name
#stn = 'R4FA0'      # station name
nw = 'AM'          # network name

"""  Use this routine for local inventory files
if stn == 'R5968' or stn == 'R4FA0':    # read inventory files if online inventory not available
    f = open(stn+'.xml')
    inv = read_inventory(stn+'.xml')
    f.close()
else:
    inv = rs.get_stations(network=nw, station=stn, level='RESP')  # get the instrument response
""" 
# comment the next line out if using local inventory files
inv = rs.get_stations(network=nw, station=stn, level='RESP')  # get the instrument response
k=0
while True:     #loop until the active epoch is found for the time of the event
    sta = inv[0][k]         #station metadata
    if sta.is_active(time=eventTime):
        break
    k += 1
latS = sta.latitude      #station latitude
lonS = sta.longitude     #station longitude
eleS = sta.elevation     #station elevation
      
#Setup the data plot
delay = 200                  # delay the start of the plot from the event (seconds) **** Enter data****
duration = 900              # duration of plots in seconds **** Enter data****

# max note length ------------------------------\n
notes1 = ""   # add notes to the diagram. max one \n per note.
#notes1 = "Likely local noise at +1095s.\nRefer to Spectrogram."     #edit as required - This overwrites the previous line!
notes2 = ""
notes3 = ""
if sta.channels[0].code =='HDF':    #if the first channels is 'HDF'
    sab = 'Raspberry Shake and Boom'
else:
    sab = 'Raspberry Shake'

#set up the traces and ray paths
calcmL = True
plot_envelopes = False         # plot envelopes on traces **** Enter data****
allphases = True   # True if all phases to be plotted, otherwise only those in the plotted time window are plotted **** Enter data****
save_plot = False   # Set to True when plot is readyto be saved **** Enter data****

start = eventTime + delay       # calculate the plot start time from the event and delay
end = start + duration               # calculate the end time from the start and duration

#set background noise sample times (choose a section of minimum velocity amplitude to represent background noise)
bnst = 900             # enter time of start of background noise sample (default = 0) **** Enter data****
bne = 600               # enter time of end of background noise sample (default = 600) **** Enter data****
bnstart = eventTime - bnst            
bnend = eventTime + bne               

# bandpass filter - select to suit system noise and range of quake **** Enter data****
filt = [0.0009, 0.001, 0.1, 0.11]
#filt = [0.09, 0.1, 0.8, 0.9]
#filt = [0.009, 0.01, 0.5, 0.6]
#filt = [0.29, 0.3, 0.8, 0.9]
#filt = [0.03, 0.033, 2, 2.1]    # use for mL estimates
#filt = [0.69, 0.7, 1.7, 1.8]
filt = [0.69, 0.7, 2, 2.1]       #distant quake
#filt = [0.69, 0.7, 3, 3.1]
#filt = [0.69, 0.7, 4, 4.1]
#filt = [0.69, 0.7, 6, 6.1]
#filt = [0.69, 0.7, 8, 8.1]
#filt = [0.99, 1, 10, 10.1]
#filt = [0.09, 0.1, 10, 10.1]
#filt = [0.69, 0.7, 10, 10.1]
#filt = [0.99, 1, 20, 20.1]
#filt = [0.69, 0.7, 20, 20.1]
#filt = [2.99, 3, 20, 20.1]        #use for local quakes
#filt = [0.69, 0.7, 49, 50]

# set the FDSN server location and channel names
ch = '*HZ' # ENx = accelerometer channels; EHx or SHZ = geophone channels

# get waveform and copy it for independent removal of instrument response
trace0 = rs.get_waveforms('AM', stn, '00', ch, start, end)
trace0.merge(method=0, fill_value='latest')         #fill in any gaps in the data to prevent a crash
trace0.detrend(type='demean')                       #demean the data
trace1 = trace0.copy()
trace2 = trace0.copy()
rawtrace = trace0.copy()            #save a raw copy of the trace for the spectrogram

#get waveform for background noise and copy it for independent removal of instrument response
bn0 = rs.get_waveforms('AM', stn, '00', ch, bnstart, bnend)
bn0.merge(method=0, fill_value='latest')         #fill in any gaps in the data to prevent a crash
bn0.detrend(type='demean')                       #demean the data
bn1 = bn0.copy()                                #copy for velocity
bn2 = bn0.copy()                                #copy for acceleration

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

#Calculate the Phase Arrivals
model = TauPyModel(model='iasp91')
arrs = model.get_travel_times(depth, great_angle_deg)
print(arrs)             # print the arrivals for reference when setting delay and duration
no_arrs = len(arrs)     # the number of arrivals

#calculate Rayleigh and Love Wave arrival Time
rayt = distance/3.2206
print("Rayleigh Arrival Time: ", rayt)
lovet = distance/4.2941
print("Love Arrival Time: ", lovet)

# Calculate infrasound travel time for Boom signal - may be useful for explosions and eruptions
infraSL = distance/0.3062       #306.2m/s for -40°C
infraSav = distance/0.32        # calculated from Tonga Eruption pressure wave
infraS0 = distance/0.331        #331m/s for 0°C
infraSE = distance/0.3547       #354.7m/s for +40°C

#Calculate Earthquake Total Energy
qenergy = 10**(1.5*mag+4.8)

# Create output traces
outdisp = trace0.remove_response(inventory=inv,pre_filt=filt,output='DISP',water_level=60, plot=False) # convert to Disp
outvel = trace1.remove_response(inventory=inv,pre_filt=filt,output='VEL',water_level=60, plot=False) # convert to Vel
outacc = trace2.remove_response(inventory=inv,pre_filt=filt,output='ACC',water_level=60, plot=False) # convert to Acc
jerk = outacc.copy()    # create a trace for Jerk (d3x/dt3)
jerk.differentiate()    # differentiate acceleration to get Jerk
outSE = outvel.copy()   # create a trace for Specific Energy by copying velocity trace
outSE[0].data = outSE[0].data*outSE[0].data/2   # Specific Energy = (velocity^2)/2 = E/m

#Calculate maximums
disp_max = outdisp[0].max()
vel_max = outvel[0].max()
acc_max = outacc[0].max()
se_max = vel_max*vel_max/2
jmax = jerk[0].max()
mLDv = np.log10(abs(disp_max/1e-6))+2.234*np.log10(distance)-1.199   #calculate estimate magnitude
mLVv = np.log10(abs(vel_max/1e-6))+2.6235*np.log10(distance)-3.415   #calculate estimate magnitude
mLAv = np.log10(abs(acc_max/1e-6))+3.146*np.log10(distance)-6.154   #calculate estimate magnitude

#Create background noise traces
bndisp = bn0.remove_response(inventory=inv,pre_filt=filt,output='DISP',water_level=60, plot=False) # convert to Disp
bnvel = bn1.remove_response(inventory=inv,pre_filt=filt,output='VEL',water_level=60, plot=False) # convert to Vel
bnacc = bn2.remove_response(inventory=inv,pre_filt=filt,output='ACC',water_level=60, plot=False) # convert to Acc
bnjerk = bnacc.copy()   # create a trace for Jerk (d3x/dt3)
bnjerk.differentiate()  # differentiate acceleration to get Jerk   

# Calculate background noise limits using standard deviation
bnsamp = 15                             #sample size in seconds
bns = int((bnend - bnstart)/bnsamp)     #calculate the number of samples in the background noise traces
bnd = divTrace(bndisp[0],bns)           #divide the displacement background noise trace into equal traces
bnv = divTrace(bnvel[0],bns)            #divide the velocity background noise trace into equal traces
bna = divTrace(bnacc[0],bns)            #divide the acceleration background noise trace into equal traces
bnj = divTrace(bnjerk[0],bns)           #divide the jerk background noise trace into equal traces
for j in range (0, bns):                #find the sample interval with the minimum background noise amplitude
    if j == 0:
        bndispstd = abs(bnd[j].std())
        bnvelstd = abs(bnv[j].std())
        bnaccstd = abs(bna[j].std())
        bnjstd = abs(bnj[j].std())
    elif abs(bnd[j].std()) < bndispstd:
        bndispstd = abs(bnd[j].std())
    elif abs(bnv[j].std()) < bnvelstd:
        bnvelstd = abs(bnv[j].std())
    elif abs(bna[j].max()) < bnaccstd:
        bnaccstd = abs(bna[j].std())
    elif abs(bnj[j].max()) < bnjstd:
        bnjstd = abs(bnj[j].std())
bnsestd = bnvelstd*bnvelstd/2           #calculate the max background noise level for the specific energy

# Create Signal Envelopes
disp_env = filter.envelope(outdisp[0].data)     #create displacement envelope
vel_env = filter.envelope(outvel[0].data)       #create velocity envelope
acc_env = filter.envelope(outacc[0].data)       #create acceleration envelope
j_env = filter.envelope(jerk[0].data)           #create jerk envelope
se_env=vel_env*vel_env/2                        #create specific energy envelope from velocity envelope!

#set up map plot
if great_angle_deg < 5:      #set satellite height based on separation
    sat_height = 1000000
elif great_angle_deg < 25:
    sat_height = 10000000
elif great_angle_deg > 120:
    sat_height = 1000000000000
elif great_angle_deg > 90:
    sat_height = 1000000000
else:
    sat_height = 100000000
    
latC = (latE+latS)/2        #latitude 1/2 way between station and event/earthquake - may need adjusting!
lonC = (lonE+lonS)/2        #longitude 1/2 way between station and event/earthquake - may need adjusting!
if abs(lonE-lonS) > 180:
    lonC = lonC + 180
if great_angle_deg > 150:
    projection = ccrs.Orthographic(
        central_latitude = latC,
        central_longitude = lonC)
    mtext = 'Orthographic projection.'
else:
    projection=ccrs.NearsidePerspective(
        central_latitude=latC,
        central_longitude=lonC,
        satellite_height=sat_height)      #adjust satellite height to best display station and event/earthquake
    mtext = 'Satellite Viewing Height = '+str(int(sat_height/1000))+' km.'
projection._threshold = projection._threshold/20    #reduce threshold so great circle lines are smooth

# set up plot
fig = plt.figure(figsize=(20,14), dpi=150)       # set to page size in inches
gsouter = gs.GridSpec(1, 3, width_ratios = [10.5, 2.5, 7], wspace = 0.1)
gsleft = gs.GridSpecFromSubplotSpec(3, 1, subplot_spec = gsouter[0], height_ratios = [4, 1, 1], hspace = 0.15)
gsright = gs.GridSpecFromSubplotSpec(4, 1, subplot_spec = gsouter[2], height_ratios = [2, 2, 1, 1], hspace = 0.1)
gsl2 = gs.GridSpecFromSubplotSpec(4, 1, subplot_spec = gsleft[0], hspace = 0)
ax1 = fig.add_subplot(gsl2[0])            # displacement waveform
ax2 = fig.add_subplot(gsl2[1])            # velocity Waveform
ax3 = fig.add_subplot(gsl2[2])            # acceleration waveform
ax9 = fig.add_subplot(gsl2[3])             # jerk Waveform
ax6 = fig.add_subplot(gsleft[1])            # specific energy waveform 
ax4 = fig.add_subplot(gsleft[2])            # velocity spectrogram
ax5 = fig.add_subplot(gsright[2])           # PSD
ax7 = fig.add_subplot(gsright[0], polar=True)       # TAUp plot
ax8 = fig.add_subplot(gsright[1], projection=projection)    # map
ax10 = fig.add_subplot(gsright[3])         # FFT
fig.suptitle("M"+str(mag)+" Earthquake - "+locE+" - "+eventTime.strftime(' %d/%m/%Y %H:%M:%S UTC'), weight='black', color='b', size='x-large')      #Title of the figure
fig.text(0.05, 0.95, "Filter: "+str(filt[1])+" to "+str(filt[2])+"Hz")          # Filter details
fig.text(0.52, 0.07, 'Separation =\n'+str(round(great_angle_deg,3))+u"\N{DEGREE SIGN}"+' or '+str(int(distance))+'km.', color = 'b')   #distance between quake and station
fig.text(0.52, 0.03, 'Latitude: '+str(latE)+u"\N{DEGREE SIGN}"+'\nLongitude: '+str(lonE)+u"\N{DEGREE SIGN}"+'\nDepth: '+str(depth)+'km.')  #quake lat, lon and depth
fig.text(0.52, 0.11, 'Quake Energy: '+f"{qenergy:0.1E}"+'J.', color = 'r')        #Earthquake energy
fig.text(0.52, 0.095, 'Equiv. to '+f"{qenergy/4.18e9:0.1E}"+' t TNT.', color = 'r')
fig.text(0.7, 0.95, 'Event ID: '+eventID)
fig.text(0.95, 0.95, 'Station: AM.'+stn+'.00.'+ch, ha='right',size='large')
fig.text(0.95, 0.935, sab, color='r', ha='right')   # Raspberry Shake and Boom or Raspberry Shake
fig.text(0.95, 0.92, 'Oberon Citizen Science Network', size = 'small', ha='right')
fig.text(0.98, 0.905, '#ShakeNet', ha='right')
fig.text(0.98, 0.89, '@raspishake', ha='right')
fig.text(0.98, 0.875, '@AlanSheehan18', ha='right')  #Twitter Handle  **** Enter data****
fig.text(0.98, 0.86, '@matplotlib', ha='right')
fig.text(0.98, 0.845, '#Python', ha='right')
fig.text(0.98, 0.83, '#CitizenScience', ha='right')
fig.text(0.98, 0.815, '#Obspy', ha='right')
fig.text(0.98, 0.8, '#Cartopy', ha='right')

# Set Directory for output Plots
pics = "D:/Pictures/Raspberry Shake and Boom/2025/"      # Edit to suit **** Enter data****

# plot logos
rsl = plt.imread("RS logo.png")
newaxr = fig.add_axes([0.935, 0.915, 0.05, 0.05], anchor='NE', zorder=-1)
newaxr.imshow(rsl)
newaxr.axis('off')

#perspective map viewing height
fig.text(0.90, 0.37, mtext, rotation=90, size='x-small')

#print notes
fig.text(0.91, 0.37, 'NOTES:  '+notes1, rotation=90)                 # add any notes about the report **** Enter data****
fig.text(0.927, 0.37, notes2, rotation=90)                 # add any notes about the report **** Enter data****
fig.text(0.944, 0.37, notes3, rotation=90)                 # add any notes about the report **** Enter data****

#end trace notes and maxima
fig.text(0.5, 0.72, 'Energy is', size='x-small',rotation=90, va='center')
fig.text(0.505, 0.72, 'proportional to V²', size='x-small',rotation=90, va='center')
fig.text(0.5, 0.85, 'Displacement biases', size='x-small',rotation=90, va='center')
fig.text(0.505, 0.85, 'low frequencies', size='x-small',rotation=90, va='center')
fig.text(0.5, 0.58, 'Acceleration biases', size='x-small',rotation=90, va='center')
fig.text(0.505, 0.58, 'high frequencies', size='x-small',rotation=90, va='center')
fig.text(0.5, 0.28, 'E/m = v²/2', size='x-small',rotation=90, va='center')
fig.text(0.505, 0.28, 'For weak arrivals', size='x-small',rotation=90, va='center')
fig.text(0.51, 0.85, 'Max D = '+f"{disp_max:.3E}"+' m', size='small',rotation=90, va='center',color='b')
fig.text(0.51, 0.72, 'Max V = '+f"{vel_max:.3E}"+' m/s', size='small',rotation=90, va='center',color='g')
fig.text(0.51, 0.58, 'Max A = '+f"{acc_max:.3E}"+' m/s²', size='small',rotation=90, va='center',color='r')
fig.text(0.51, 0.28, 'Max SE = '+f"{se_max:.3E}"+' J/kg', size='small',rotation=90, va='center',color='g')
fig.text(0.5, 0.11, 'Unfiltered Spectrogram', size='x-small', rotation=90, va='center')
fig.text(0.5, 0.455, 'Max Jerk =', size='small', rotation=90, color='purple', va='center')
fig.text(0.507, 0.455, f"{jmax:.3E}"+' m/s³', size='small', rotation=90, color='purple', va='center')
if calcmL:
    fig.text(0.52, 0.85, 'MLDv = '+str(np.round(mLDv,1))+' +/- 1.40', size='small',rotation=90, va='center')
    fig.text(0.52, 0.72, 'MLVv = '+str(np.round(mLVv,1))+' +/- 1.56', size='small',rotation=90, va='center')
    fig.text(0.52, 0.58, 'MLAv = '+str(np.round(mLAv,1))+' +/- 1.89', size='small',rotation=90, va='center')

# print signal to noise ratios
fig.text(0.515, 0.85, 'S/N = '+f"{abs(disp_max/(3*bndispstd)):.3}", size='x-small', rotation=90, va='center', color='b')
fig.text(0.515, 0.72, 'S/N = '+f"{abs(vel_max/(3*bnvelstd)):.3}", size='x-small', rotation=90, va='center', color='g')
fig.text(0.515, 0.58, 'S/N = '+f"{abs(acc_max/(3*bnaccstd)):.3}", size='x-small', rotation=90, va='center', color='r')
fig.text(0.515, 0.455, 'S/N = '+f"{abs(jmax/(3*bnjstd)):.3}", size='x-small', rotation=90, va='center', color='purple')
fig.text(0.515, 0.28, 'S/N = '+f"{abs(se_max/(3*bnsestd)):.3}", size='x-small', rotation=90, va='center', color='g')

# print background noise data
fig.text(0.53, 0.33, 'Background Noise:', size='small')
fig.text(0.53, 0.32, 'Displacement:', color='b', size='small')
fig.text(0.53, 0.31, 'SD = '+f"{bndispstd:.3E}"+' m', color='b', size='small')
fig.text(0.53, 0.3, '3SD = '+f"{(3*bndispstd):.3E}"+' m', color='b', size='small')
fig.text(0.53, 0.29, 'Velocity:', color='g', size='small')
fig.text(0.53, 0.28, 'SD = '+f"{bnvelstd:.3E}"+' m/s', color='g', size='small')
fig.text(0.53, 0.27, '3SD = '+f"{(3*bnvelstd):.3E}"+' m/s', color='g', size='small')
fig.text(0.53, 0.26, 'Acceleration:', color='r', size='small')
fig.text(0.53, 0.25, 'SD = '+f"{bnaccstd:.3E}"+' m/s²', color='r', size='small')
fig.text(0.53, 0.24, '3SD = '+f"{(3*bnaccstd):.3E}"+' m/s²', color='r', size='small')
fig.text(0.53, 0.23, 'Jerk:', color='purple', size='small')
fig.text(0.53, 0.22, 'SD = '+f"{bnjstd:.3E}"+' m/s³', color='purple', size='small')
fig.text(0.53, 0.21, '3SD = '+f"{(3*bnjstd):.3E}"+' m/s³', color='purple', size='small')
fig.text(0.53, 0.20, 'Specific Energy:', color='g', size='small')
fig.text(0.53, 0.19, 'SD = '+f"{bnsestd:.3E}"+' J/kg', color='g', size='small')
fig.text(0.53, 0.18, '3SD = '+f"{(3*bnsestd):.3E}"+' J/kg', color='g', size='small')
fig.text(0.53, 0.17, 'BN parameters:', size='small')
fig.text(0.53, 0.16, 'Minimum SD over:', size='small')
fig.text(0.53, 0.15, 'Start: Event time - '+str(bnst)+' s.',size='small')
fig.text(0.53, 0.14, 'End: Event time + '+str(bne)+' s.',size='small')
fig.text(0.53, 0.13, 'BN Sample size = '+str(bnsamp)+' s.',size='small')

#plot traces
ax1.plot(trace0[0].times(reftime=eventTime), outdisp[0].data, lw=1, color='b')      # displacement waveform
fmtax(ax1, 0, False)    #axis, limit, no negatives
ax1.margins(x=0)
ax1.set_ylabel("Vertical Displacement, m", size='small')
ax2.plot(trace0[0].times(reftime=eventTime), outvel[0].data, lw=1, color='g')       # velocity Waveform
fmtax(ax2, 0, False)    #axis, limit, no negatives
ax2.margins(x=0)
ax2.set_ylabel("Vertical Velocity, m/s", size ='small')
ax3.plot(trace0[0].times(reftime=eventTime), outacc[0].data, lw=1, color='r')       # acceleration waveform
fmtax(ax3, 0, False)    #axis, limit, no negatives
ax3.margins(x=0)
ax3.set_ylabel("Vertical Acceleration, m/s²", size='small')         
ax4.specgram(x=rawtrace[0], NFFT=256, noverlap=128, Fs=100, cmap='viridis')         # velocity spectrogram
ax4.xaxis.set_minor_locator(AutoMinorLocator(10))
ax4.set_yscale('log')               # set logarithmic y scale - comment this out for linear scale
ax4.set_ylim(0.5,50)              #limits for log scale
#plot filter limits on spectrogram
ax4.axhline(y=filt[1], lw=1, color='r', linestyle='dotted')
ax4.axhline(y=filt[2], lw=1, color='r', linestyle='dotted')
ax4.set_ylabel("Velocity Frequency, Hz", size='small')
ax4.set_xlabel('S e c o n d s   a f t e r   S t a r t   o f   T r a c e ,   s', size='small', alpha=0.5, labelpad=0)
ax9.plot(trace0[0].times(reftime=eventTime), jerk[0].data, lw=1, color='purple')       # jerk waveform
fmtax(ax9, 0, False)    #axis, limit, no negatives
ax9.margins(x=0)
ax9.set_ylabel("Vertical Jerk, m/s³", size='small')         
ax9.set_xlabel('S e c o n d s   a f t e r   E v e n t ,   s', size='small', alpha=0.5, labelpad=0)
ax6.plot(trace0[0].times(reftime=eventTime), outSE[0].data, lw=1, color='g', linestyle=':')  #specific kinetic energy Waveform
fmtax(ax6, 0, True)    #axis, limit, no negatives
ax6.set_xlabel('S e c o n d s   a f t e r   E v e n t ,   s', size='small', alpha=0.5, labelpad=0)
ax6.set_ylabel('Specific Energy, J/kg', size='small')

#plot PSD
#calculate NFFT for PSD
if duration >= 82:
    nfft = 8192
else:
    nfft = duration*100
#ax5.psd(x=rawtrace[0], NFFT=nfft, noverlap=0, Fs=100, color='k', lw=1, label='Unfiltered')    # velocity PSD raw data comment out if not required/desired
ax5.psd(x=trace0[0], NFFT=nfft, noverlap=0, Fs=100, color='b', lw=1, label='Disp')      # displacement PSD filtered
ax5.psd(x=trace1[0], NFFT=nfft, noverlap=0, Fs=100, color='g', lw=1, label='Vel')       # velocity PSD filtered
ax5.psd(x=trace2[0], NFFT=nfft, noverlap=0, Fs=100, color='r', lw=1, label='Acc')       # acceleration PSD filtered
ax5.psd(x=jerk[0], NFFT=nfft, noverlap=0, Fs=100, color='purple', lw=1, label='Jerk')   # jerk PSD filtered
ax5.legend(frameon=False, fontsize='x-small')
ax5.set_xscale('log')               #use logarithmic scale on PSD
#ax5.set_yscale('linear')
#ax5.set_yscale('log')
#plot filter limits on PSD
ax5.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
ax5.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
ax5.set_xlim(filt[1]*.75, int(filt[2]+1))
ax5.set_ylabel("PSD, dB",size='small')
ax5.set_xlabel('F r e q u e n c y ,   H z', size='small', alpha=0.5, labelpad=-9)
secax_x5 = ax5.secondary_xaxis('top', functions=(one_over, inverse))        #PSD secondary axis
secax_x5.set_xlabel('P e r i o d ,   s', size='small', alpha=0.5, labelpad=-9)

# fourier analysis plot
rfft = np.fft.rfft(rawtrace[0].data)
dfft = np.fft.rfft(outdisp[0].data)
vfft = np.fft.rfft(outvel[0].data)
afft = np.fft.rfft(outacc[0].data)
jfft = np.fft.rfft(jerk[0].data)
xfft = np.fft.rfftfreq(outvel[0].data.size, d = 1/100)
#ax10.plot(xfft, abs(rfft), color='k', lw=1, label='Unfiltered')
#ax10.plot(xfft, abs(dfft), color='b', lw=1, label='Disp')
ax10.plot(xfft, abs(vfft), color='g', lw=1, label='Vel')
#ax10.plot(xfft, abs(afft), color='r', lw=1, label='Acc')
#ax10.plot(xfft, abs(jfft), color='purple', lw=1, label='Jerk')
ax10.legend(frameon=False, fontsize='x-small')
#ax10.set_xscale('log')               #use logarithmic scale on PSD
#ax10.set_yscale('linear')
#ax10.set_yscale('log')
# plot filter limits on FFT
ax10.axvline(x=filt[1], linewidth=1, linestyle='dotted', color='r')
ax10.axvline(x=filt[2], linewidth=1, linestyle='dotted', color='r')
if filt[2] >=4:
    fxt = filt[2]+1
else:
    fxt = filt[2]*1.25
ax10.set_xlim(filt[1]*.75, fxt)
ax10.set_ylabel("FFT Spectrum",size='small')
ax10.set_xlabel('F r e q u e n c y ,   H z', size='small', alpha=0.5, labelpad=0)
fmtax(ax10, 0, True)    #axis, limit, no negatives
    
#plot background noise limits
plot_noiselims(ax1, bndispstd, -bndispstd)      #displacement noise limits - comment out if not desired
plot_noiselims(ax2, bnvelstd, -bnvelstd)        #velocity noise limits - comment out if not desired
plot_noiselims(ax3, bnaccstd, -bnaccstd)        #acceleration noise limits - comment out if not desired
plot_noiselims(ax9, bnjstd, -bnjstd)        #jerk noise limits - comment out if not desired
plot_se_noiselims(ax6, bnsestd)                 #specific kinetic energy noise limits - comment out if not desired

# plot Signal envelopes
if plot_envelopes:
    ax1.plot(trace0[0].times(reftime=eventTime), disp_env, 'b:')    #displacement envelope
    ax2.plot(trace0[0].times(reftime=eventTime), vel_env, 'g:')     #velocity envelope
    ax3.plot(trace0[0].times(reftime=eventTime), acc_env, 'r:')     #acceleration envelope
    ax9.plot(trace0[0].times(reftime=eventTime), j_env, color = 'purple', linestyle = ':')   #jerk envelope
#envelope for specific kinetic plot IS the specific energy graph.
#Energy is a scalar, so in vibrations alternates between kinetic and potential energy states.
ax6.plot(trace0[0].times(reftime=eventTime), se_env, 'g')      #specific energy envelope

#plot secondary axes - set time interval (dt) based on the duration to avoid crowding
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

tbase = start - start.second +(int(start.second/dt)+1)*dt       #find the first time tick

#clear the first tick if it will overprint the Y axis scale factor
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

# Set up Secondary Axes
secax_x1 = ax1.secondary_xaxis('top')       #Displacement secondary axis
sax(secax_x1, tticks)
secax_x4 = ax4.secondary_xaxis('top')      #spectrogram secondary axis
sax(secax_x4, sticks)
secax_x6 = ax6.secondary_xaxis('top')       #Specific Energy secondary axis
sax(secax_x6, tticks)

#add grid to graphs
ax4.grid(color='dimgray', ls = '-.', lw = 0.33)
grid(ax5)

# Clean up partially hidden xticks
ax1.tick_params(axis = 'x', colors = 'w')
ax2.tick_params(axis = 'x', colors = 'w')
ax3.tick_params(axis = 'x', colors = 'w')

#plot map
ax8.coastlines(resolution='110m')
ax8.stock_img()
# Create a feature for States/Admin 1 regions at 1:50m from Natural Earth to display state borders
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax8.add_feature(states_provinces, edgecolor='gray')
ax8.gridlines()
#plot station position on map
ax8.plot(lonS, latS,
     color='red', marker='v', markersize=12, markeredgecolor='black',
     transform=ccrs.Geodetic(),
     )
#plot event/earthquake position on map
ax8.plot(lonE, latE,
     color='yellow', marker='*', markersize=20, markeredgecolor='black',
     transform=ccrs.Geodetic(),
     )
#plot dashed great circle line from event/earthquake to station
ax8.plot([lonS, lonE], [latS, latE],
     color='blue', linewidth=2, linestyle='--', 
     transform=ccrs.Geodetic(),
     )

# build array of arrival data
y2 = 0.93        #start near middle of page but maximise list space
dy = 0.008      # linespacing
fig.text(0.53, y2, 'Phase',size='x-small')         #print headings
fig.text(0.565, y2, 'Time',size='x-small')
fig.text(0.6, y2, 'UTC',size='x-small')
fig.text(0.63, y2, 'Vertical Component', size='x-small')
pphases=[]          #create an array of phases to plot
pfile=''            #create phase names for filename
alf=1.0          #set default transparency
for i in range (0, no_arrs):                    #print data array
    y2 -= dy
    if arrs[i].time >= delay and arrs[i].time < (delay+duration):       #list entries in the plots are black
        alf=1.0
    else:                                                               #list entries not in plots are greyed out
        alf=0.53
    fig.text(0.53, y2, arrs[i].name, size='x-small', alpha=alf)       #print phase name
    fig.text(0.565, y2, str(round(arrs[i].time,3))+'s', size='x-small', alpha=alf)     #print arrival time
    arrtime = eventTime + arrs[i].time
    fig.text(0.6, y2, arrtime.strftime('%H:%M:%S'), size='x-small', alpha=alf)
    if allphases or (arrs[i].time >= delay and arrs[i].time < (delay+duration)):      #build the array of phases
        pphases.append(arrs[i].name)
        pfile += ' '+arrs[i].name
    if arrs[i].name.endswith('P') or arrs[i].name.endswith('p') or arrs[i].name.endswith('Pdiff') or arrs[i].name.endswith('Pn'):                    #calculate and print the vertical component of the signal
        fig.text(0.63, y2, str(round(100*math.cos(math.radians(arrs[i].incident_angle)),1))+'%', alpha = alf, size='x-small')
    elif arrs[i].name.endswith('S') or arrs[i].name.endswith('s') or arrs[i].name.endswith('Sn') or arrs[i].name.endswith('Sdiff'):
        fig.text(0.63, y2, str(round(100*math.sin(math.radians(arrs[i].incident_angle)),1))+'%', alpha = alf, size='x-small')
y2 -= 2*dy
fig.text(0.53, y2, str(no_arrs)+' arrivals total.', size='xx-small')     #print number of arrivals

#print(pphases)      #print the phases to be plotted on ray path diagram

# print the Rayleigh Surface Wave arrival time
y2 -= 2*dy
fig.text(0.53, y2, 'Love', size='x-small')
y2 -= dy
fig.text(0.53, y2, 'Surface Wave: '+str(round(lovet,1))+'s:', size='x-small')
arrtime = eventTime + lovet
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
y2 -= dy
fig.text(0.53, y2, 'Rayleigh', size='x-small')
y2 -= dy
fig.text(0.53, y2, 'Surface Wave: '+str(round(rayt,1))+'s:', size='x-small')
arrtime = eventTime + rayt
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
    
#print infrasound arrival window
y2 -= 2*dy
fig.text(0.53, y2, 'Infrasound Window', size='x-small')
y2 -= dy
fig.text(0.53, y2, 'Start:         '+str(round(infraSE,1))+'s:', size='x-small')
arrtime = eventTime + infraSE
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
y2 -= dy
fig.text(0.53, y2, 'Average:    '+str(round(infraSav,1))+'s:', size='x-small')
arrtime = eventTime + infraSav
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
y2 -= dy
fig.text(0.53, y2, '0°C:           '+str(round(infraS0,1))+'s:', size='x-small')
arrtime = eventTime + infraS0
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
y2 -= dy
fig.text(0.53, y2, 'End:           '+str(round(infraSL,1))+'s:', size='x-small')
arrtime = eventTime + infraSL
fig.text(0.6, y2, arrtime.strftime('%H:%M:%S UTC'), size='x-small')
    
# print phase key
y2 = 0.7          # line y position
dy = 0.008      # linespacing
fig.text(0.98, y2, 'Phase Key', size='small', ha='right')      #print heading
pkey = ['P:   compression wave', 'p:   strictly upward compression wave', 'S:   shear wave', 's:   strictly upward shear wave', 'K:   compression wave in outer core', 'I:   compression wave in inner core', 'c:   reflection off outer core', 'diff:   diffracted wave along core mantle boundary', 'i:   reflection off inner core', 'n:   wave follows the Moho (crust/mantle boundary)']
for i in range (0, 10):
    y2 -=dy
    fig.text(0.98, y2, pkey[i], size='x-small', ha='right')      #print the phase key

#plot phase arrivals
plot_arrivals(ax1, 0, 0.8, 0.95, False)          #plot arrivals on displacement plot
plot_arrivals(ax2, 0, 0.8, 0.95, False)          #plot arrivals on velocity plot
plot_arrivals(ax3, 0, 0.8, 0.95, False)          #plot arrivals on acceleration plot
plot_arrivals(ax9, 0, 0.8, 0.95, False)          #plot arrivals on jerk plot
plot_arrivals(ax4, delay, 0.6, 1.8, False)      #plot arrivals on spectrogram plot
plot_arrivals(ax6, 0, 0.9, 1, True)            #plot arrivals on energy plot

# get the limits of the y axis so text can be consistently placed
ax4b, ax4t = ax4.get_ylim()
ax4.text(2, ax4t*0.45, 'Plot Start Time: '+start.strftime(' %d/%m/%Y %H:%M:%S.%f UTC (')+str(delay)+' seconds after event).', size='small')      # explain difference in x time scale

#adjust subplots for readability
plt.subplots_adjust(hspace=0.3, wspace=0.1, left=0.05, right=0.95, bottom=0.05, top=0.92)

#plot the ray paths
arrivals = model.get_ray_paths(depth, great_angle_deg, phase_list=pphases)      #calculate the ray paths
ax7 = arrivals.plot_rays(plot_type='spherical', ax=ax7, fig=fig, phase_list=pphases, show=False, legend=True)   #plot the ray paths
if no_arrs > 23:
    ax7.legend(loc = 'upper left', fontsize = 'xx-small')
    
if allphases:
    fig.text(0.92, 0.75, 'Show All Phases', size='small')
else:
    fig.text(0.92, 0.75, 'Show Phases\nVisible in Traces', size='small')
if great_angle_deg > 103 and great_angle_deg < 143:
    ax7.text(great_angle_rad,6000, 'Station in P and\nS wave shadow', size='x-small', rotation=180-great_angle_deg, ha='center', va='center')
elif great_angle_deg >143:
    ax7.text(great_angle_rad,6000, 'Station in S\nwave shadow', size='x-small', rotation=180-great_angle_deg, ha='center', va='center')
    
#label Station
ax7.text(great_angle_rad,7000, stn, ha='center', va='center', alpha=.7, size='small', rotation= -great_angle_deg)
    
# add boundary depths
ax7.text(math.radians(315),5550, '660km', ha='center', va='center', alpha=.7, size='small', rotation=45)
ax7.text(math.radians(315),3300, '2890km', ha='center', va='center', alpha=.7, size='small', rotation=45)
ax7.text(math.radians(315),1010, '5150km', ha='center', va='center', alpha=.7, size='small', rotation=45)

# Annotate regions
ax7.text(0, 0, 'Solid\ninner\ncore',
        horizontalalignment='center', verticalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
ocr = (model.model.radius_of_planet -
       (model.model.s_mod.v_mod.iocb_depth +
        model.model.s_mod.v_mod.cmb_depth) / 2)
ax7.text(math.radians(180), ocr, 'Fluid outer core',
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
mr = model.model.radius_of_planet - model.model.s_mod.v_mod.cmb_depth / 2
ax7.text(math.radians(180), mr, 'Solid mantle',
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

#create phase identifier for filename
if allphases:
    pfile = ' All'

#print filename on bottom left corner of diagram
filename = pics+'M'+str(mag)+'Quake '+locE+eventID+eventTime.strftime('%Y%m%d %H%M%S UTC'+stn+pfile+'.png')
fig.text(0.02, 0.01,filename, size='x-small')

# add github repository address for code
fig.text(0.98, 0.01,'https://github.com/sheeny72/RPiSandB', size='x-small', ha='right')


#print standard text to copy for posting on Social Media (Twitter)
print('M'+str(mag)+' #earthquake '+locE+' detected on '+sab+' ('+nw+'.'+stn+'.00.'+ch+') @raspishake #python #CitizenScience #ShakeNet #Obspy @matplotlib #Cartopy #seismology #OCSN')

# save the final figure if the plot is ready
if save_plot:
    plt.savefig(filename)

# show the final figure
plt.show()
