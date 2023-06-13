# -*- coding: utf-8 -*-
"""
Created on Sun May 21 12:22:53 2023

@author: al72
"""

from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime, Stream
import matplotlib.pyplot as plt
from obspy.taup import TauPyModel
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.transforms import blended_transform_factory
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees, degrees2kilometers

rs = Client('https://data.raspberryshake.org/')

# Build a station list of local stations so unwanted stations can be commented out
# as required to save typing
def stationList(sl):
    sl += ['R21C0']
    sl += ['R811A']
    sl += ['R9AF3']
    sl += ['R571C']
    sl += ['R6D2A']
    #sl += ['RF35D']
    sl += ['R7AF5']
    #sl += ['R26B1']
    #sl += ['R3756']
    #sl += ['R6707']
    #sl += ['RB18D']
    #sl += ['R9A9D']
    #sl += ['RCF6A']
    #print(sl)
    return sl

# Build a stream of traces from each of the selected stations    
def buildStream(strm):
    n = len(slist)      # n is the number of traces (stations) in the stream
    tr1 = []
    for i in range(0, n):
        inv = rs.get_stations(network='AM', station=slist[i], level='RESP')  # get the instrument response
        
        #read each epoch to find the one that's active for the event
        k=0
        while True:
            sta = inv[0][k]         #station metadata
            if sta.is_active(time=eventTime):
                break
            k += 1
        latS = sta.latitude     #active station latitude
        lonS = sta.longitude     #active station longitude
        #eleS = sta.elevation     #active station elevation is not required for this program
        print(sta)      # print the station on the console so you know which, if any, station fails to have data
        trace = rs.get_waveforms('AM', station=slist[i], location = "00", channel = 'EHZ', starttime = start, endtime = end)
        trace.merge(method=0, fill_value='latest')         #fill in any gaps in the data to prevent a crash
        trace.detrend(type='demean')                       #detrend the data
        tr1 = trace.remove_response(inventory=inv,zero_mean=True,pre_filt=ft,output='VEL',water_level=60, plot=False) # convert to Vel
        # save data in the trace.stats for use later
        tr1[0].stats.distance = gps2dist_azimuth(latS, lonS, latE, lonE)[0] # distance from the event to the station in metres
        tr1[0].stats.latitude = latS        # save the station latitude from the inventory with the trace
        tr1[0].stats.longitude = lonS       # save the station longitude from the inventory with the trace
        tr1[0].stats.colour = colours[i]    # assign a colour to the station/trace
        strm += tr1
    #strm.plot(method='full', equal_scale=False)
    return strm

# function to convert kilometres to degrees
def k2d(x):
    return kilometers2degrees(x)

# function to convert degrees to kilometres
def d2k(x):
    return degrees2kilometers(x)

# Build a list of local places for the map
# Lat Long Data from https://www.latlong.net/
# format ['Name', latitude, longitude, markersize]
#comment out those not used to minimise typing
places = [['Oberon', -33.704922, 149.862900, 2],
          ['Bathurst', -33.419281, 149.577499, 4],
          ['Lithgow', -33.480930, 150.157410, 4],
          ['Mudgee', -32.590439, 149.588684, 4],
          ['Orange', -33.283333, 149.100006, 4],
          ['Sydney', -33.868820, 151.209290, 6],
          ['Newcastle', -32.926670, 151.780014, 6],
          ['Coonabarabran', -31.273911, 149.277420, 4],
          ['Gulgong', -32.362492, 149.532104, 2],
          #['Narrabri', -30.325060, 149.782974, 4],
          ['Muswellbrook', -32.265221, 150.888184, 4],
          #['Tamworth', -31.092749, 150.932037, 4],
          #['Boorowa', -34.437340, 148.717972, 2],
          #['Cowra,', -33.828144, 148.677856, 4],
          #['Goulburn', -34.754539, 149.717819, 4],
          #['Grafton', -29.690960, 152.932968, 4],
          #['Coffs Harbour', -30.296350, 153.115692, 4],
          #['Armidale', -30.512960, 151.669418, 4],
          #['Brisbane', -27.469770, 153.025131, 6]
          ]

# Enter event data (estimate by trial and error for unregistered events)    
eventTime = UTCDateTime(2023, 6, 10, 6, 9, 18) # (YYYY, m, d, H, M, S) **** Enter data****
latE = -32.3                           # quake latitude + N -S **** Enter data****
lonE = 149.8                        # quake longitude + E - W **** Enter data****
depth = 0                             # quake depth, km **** Enter data****
mag = 1                              # quake magnitude **** Enter data****
eventID = 'unknown'               # ID for the event **** Enter data****
locE = "Ulan, NSW, Australia"                # location name **** Enter data****

slist = []
stationList(slist)
# bandpass filter - select to suit system noise and range of quake
#ft = [0.1, 0.1, 0.8, 0.9]
#ft = [0.3, 0.3, 0.8, 0.9]
#ft = [0.5, 0.5, 2, 2.1]
#ft = [0.7, 0.7, 2, 2.1]       #distant quake
#ft = [0.7, 0.7, 3, 3.1]
#ft = [0.7, 0.7, 4, 4.1]
#ft = [0.7, 0.7, 6, 6.1]
#ft = [0.7, 0.7, 8, 8.1]
#ft = [1, 1, 10, 10.1]
ft = [1, 1, 20, 20.1]
#ft = [3, 3, 20, 20.1]        #use for local quakesprint(filt[1], filt[2])
colours = ['r', 'b', 'g', 'k', 'c', 'm', 'purple', 'orange', 'gold', 'midnightblue']    # array of colours for stations and phases
plist = ('P', 'S')      # phase list for plotting

#set up the plot
delay = 0           # for future development for longer distance quakes - leave as 0 for now!
duration = 60       #adjust duration to get detail required
start = eventTime + delay   # for future development for longer distance quakes
end = start + duration      # for future development for longer distance quakes

# Build the stream of traces/stations
st = Stream()
buildStream(st)

#set up the figure
fig = plt.figure(figsize=(20,14), dpi=100)       # set to page size in inches

#build the section plot
ax1 = fig.add_subplot(1,2,1)
st.plot(type='section', plot_dx=20e3, recordlength=duration, time_down=True, linewidth=.3, alpha=0.8, grid_linewidth=.25, show=False, fig=fig)

# Plot customization: Add station labels to offset axis
ax = ax1.axes
transform = blended_transform_factory(ax.transData, ax.transAxes)
for t in st:
    ax.text(t.stats.distance / 1e3, 1.0, t.stats.station, rotation=90,
            va="bottom", ha="center", color=t.stats.colour, transform=transform, zorder=10)

#setup secondary x axis
secax_x1 = ax1.secondary_xaxis('top', functions = (k2d, d2k))   #secondary axis in degrees separation

#plot arrivals times
model = TauPyModel(model="iasp91")

axl, axr = ax1.get_xlim()   # get the left and right limits of the section plot
if axl<0:           #if axl is negative, make it zero to start the range for phase plots
    axl=0
for j in range (int(axl), int(axr)):    # plot phase arrivals every kilometre
    arr = model.get_travel_times(depth, k2d(j), phase_list=plist)
    n = len(arr)
    for i in range(0,n):
        ax.plot(j, arr[i].time, marker='o', markersize=1, color = colours[plist.index(arr[i].name)], alpha=0.3)
        if j/20 == int(j/20):       # periodically plot the phase name
            ax.text(j, arr[i].time, arr[i].name, color=colours[plist.index(arr[i].name)], alpha=0.5, ha='center', va='center')
    j+=1
                
#plot the map
ax2 = fig.add_subplot(1,2,2, projection=ccrs.PlateCarree())
mt = -30    # latitude of top of map
mb = -35    # latitude of the bottom of the map
ml = 148    # longitude of the left side of the map
mr = 152    # longitude of the right side of the map
ax2.set_extent([ml,mr,mt,mb], crs=ccrs.PlateCarree())
#ax2.coastlines(resolution='110m')  # use for large scale maps
#ax2.stock_img()                    # use for large scale maps

# Create a features
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.OCEAN)
ax2.add_feature(cfeature.COASTLINE)
ax2.add_feature(states_provinces, edgecolor='gray')
ax2.add_feature(cfeature.LAKES, alpha=0.5)
ax2.add_feature(cfeature.RIVERS)
ax2.gridlines(draw_labels=True)
#plot event/earthquake position on map
ax2.plot(lonE, latE,
     color='yellow', marker='*', markersize=20, markeredgecolor='black',
     transform=ccrs.Geodetic(),
     )
# print the lat, long, and event time beside the event marker
ax2.text(lonE+0.1, latE-0.05, "("+str(latE)+", "+str(lonE)+")\n"+eventTime.strftime('%d/%m/%y %H:%M:%S UTC'))

#plot station positions on map
for tr in st:
    ax2.plot(tr.stats.longitude, tr.stats.latitude,
             color=tr.stats.colour, marker='H', markersize=12, markeredgecolor='black',
             transform=ccrs.Geodetic(),
             )

#plot places
for pl in places:
    ax2.plot(pl[2], pl[1], color='k', marker='o', markersize=pl[3], markeredgecolor='k', transform=ccrs.Geodetic(), label=pl[0])
    ax2.text(pl[2], pl[1]-0.1, pl[0], horizontalalignment='center', transform=ccrs.Geodetic())

#add notes to map
#ax2.text((ml+mr)/2, mt-0.2, 'M'+str(mag)+' Earthquake at '+locE, ha='center')  # use for identified earthquakes
ax2.text((ml+mr)/2, mt-0.2, 'Likely Ulan Mine Blast at '+locE, ha='center')     # use for unidentified events
ax2.text((ml+mr)/2, mt-0.3, 'Depth = '+str(depth)+' km. ID = '+eventID, ha='center')
ax2.text((ml+mr)/2, mt-0.4, 'Filter = '+str(ft[1])+' to '+str(ft[2])+' Hz.', ha='center')


plt.subplots_adjust(wspace=0.1)

# add a plt.savefig(filename) line here if required.

plt.show()