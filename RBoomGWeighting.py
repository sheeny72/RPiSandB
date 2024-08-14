# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 08:19:54 2024

Modified to module on Wed Jun 26 17:08:00 2034

@author: al72 a.k.a. @AlanSheehan18

Infrasound module for G weighting of Raspberry Boom signal and related functions 
to emulate Sound Pressure Level meter output and infrasound compliance limits

This module cannot account for frequency distribution changes within the sample period.
This is not an issue for constant noise, but could be a source of inaccuracy in
G weighted results for transient signals. For this reason, minimal sample periods are
recommended for transient signals.

The G weighting for transient signals can be approximated by applying octave, or 1/3
octave, or arbitrary narrow band, filtering across the sample bandwidth. Apply the G
weighting to each sample before adding the waveforms to get an approximation of the G
weighted waveform. Obviously the narrower the bandwidths of the sub samples, the better
the approximation of the true G weighted signal.

To install, copy this module to the same directory as your code or in PYTHONPATH directory
"""

import numpy as np
from obspy.signal import filter
import matplotlib.pyplot as plt

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
    fs = 100    # sampling frequency for Raspberry Boom
    ns = len(y[0].data)   #number of samples

    fstep = fs / ns     # frequency interval
    f = np.linspace(0, (ns-1)*fstep, ns)     #frequency steps

    # FFT
    yfft = np.fft.fft(y[0].data)
    #normalise the FFT
    y_mag = np.abs(yfft)/ns     
    f_plot = f[0:int(ns/2+1)]
    lfft = 2*y_mag[0:int(ns/2+1)]
    lfft[0] = lfft[0]/2     # do not multiply DC value
    
    return f_plot, lfft

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
    maxp = np.abs(y).max()   #find the max pressure amplitude of waveform
    
    return maxp

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
    maxpp = peak(y)*2
    
    return maxpp

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
    yav = np.mean(np.abs(y.data))
    
    return yav

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
    # calculate y rms
    yrms = np.mean(y.data**2)
    yrms = np.sqrt(yrms)
    
    return yrms

def leq(dB):
    """
    Equivalent infrasound Pressure Level, Leq is the RMS value of the Infrasound pressure level
    
    Parameters
    ----------
    dB : array of float64 
        array of float64 with response removed. dB

    Returns
    -------
    yleq : float64
        waveform root mean square (RMS) amplitude for the sample. Pa
    
    """
    # calculate y rms
    yleq = np.mean(dB**2)
    yleq = np.sqrt(yleq)
        
    return yleq

def sel(dB):
    """
    Infrasound Exposure Level, SEL
    
    Parameters
    ----------
    dB : trace 
        Obspy waveform trace with response removed. dB

    Returns
    -------
    ysel : float64
        waveform root mean square (RMS) amplitude for the sample. Pa
    
    """
    ysel = leq(dB) + 10*np.log10(len(dB.data)/100)
    
    return ysel

def pa2db(y):    
    """
    Convert Pascals (Pa) to linear (unweighted) decibels (dBL)
    
    Parameters
    ----------
    y : array of float
        Obspy waveform trace with response removed. Pa

    Returns
    -------
    db : trace
        array of decibel (dB) values
    
    """
    db = 10*np.log10(y*y) + 93.979400087        #convert to sound pressure level

    return db

def db2pa(db):    
    """
    Convert decibels (dB) to Pascals (Pa)
    
    Parameters
    ----------
    db : array of float 
        array of decibel (dB) values

    Returns
    -------
    x : array of float
        Obspy wave form stream. dBL
    
    """
    x = 0.00002*10**(db/20)        #convert to sound pressure level

    return x

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
    pk = peak(y)
    pspl = pa2db(pk)
    
    return pspl

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
    fftdB = []
    for i in range (0, len(lfft.data)):
        fftdB.append(pa2db(abs(lfft[i])))
        
    return fftdB

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
    fftdBG = []
    for i in range (0, len(fftdB)):
        if f_plot[i] == 0:
            fftdBG.append(fftdB[i+1]+34.142*np.log(f_plot[i+1])-41.332)
        elif f_plot[i] < 1:
            fftdBG.append(fftdB[i]+34.142*np.log(f_plot[i])-41.332)
        elif f_plot[i] <= 3.15:
            fftdBG.append(fftdB[i]-1.7406*f_plot[i]**4+15.961*f_plot[i]**3-55.565*f_plot[i]**2+95.938*f_plot[i]-97.475)
        elif f_plot[i] < 12.5:
            fftdBG.append(fftdB[i]+17.396*np.log(f_plot[i])-40.037)
        elif f_plot[i] <= 20:
            fftdBG.append(fftdB[i]-.0976*f_plot[i]**2+3.8393*f_plot[i]-28.738)
        elif f_plot[i] < 31.5:
            fftdBG.append(fftdB[i]-.0108*f_plot[i]**2-.5724*f_plot[i]+24.782)
        else:
            fftdBG.append(fftdB[i]+.0076*f_plot[i]**2-1.4868*f_plot[i]+35.262)
            
    return fftdBG

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
    fftG = []
    for i in range (0, len(fftdB)):
        fftG.append(db2pa(fftdBG[i]))
    return fftG

# ====================== octave band functions ======================

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
    oct = [[-10, 0.016, 0.0152587890625],
           [-9, 0.0315, 0.030517578125],
           [-8, 0.063, 0.06103515625],
           [-7, 0.125, 0.1220703125],
           [-6, 0.25, 0.244140625],
           [-5, 0.5, 0.48828125],
           [-4, 1, 0.9765625],
           [-3, 2, 1.953125],
           [-2, 4, 3.90625],
           [-1, 8, 7.8125],
           [0, 16, 15.625],
           [1, 31.5, 31.25],
           [2, 63, 62.5]]
    
    return oct

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
    
    fl = fc/np.sqrt(2)
    
    return fl

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
    
    fu = fc*np.sqrt(2)
    
    return fu

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
    octBL = octave()
    for i in range(0, len(octBL)):
        obl = octFL(octBL[i][2])
        if obl >= fl:
            break
        
    if octFU(octBL[i][2]) > fu:
        print('Filter bandwidth too narrow for octave band')
    else:
        return octBL[i], i

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
    octBH = octave()
    for i in range(0, len(octBH)):
        obu = octFU(octBH[i][2])
        if obu > fu:
            break
    i-=1    
    if octFL(octBH[i][2]) < fl:
        print('Filter bandwidth too narrow for octave band')
    else:
        return octBH[i], i

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
    octBL = octave()
    for i in range(0, len(octBL)):
        obl = octFL(octBL[i][2])
        if obl >= fl:
            break
    i -=1 
    
    return octBL[i], i

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
    octBH = octave()
    for i in range(0, len(octBH)):
        obu = octFU(octBH[i][2])
        if obu > fu:
            break
        
    return octBH[i], i

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
    octB = [[]]
    #print(octB)
    octs = octave()
    
    if within:
        j = octBandLow(fl, fu)[1]
        k = octBandHigh(fl, fu)[1]
    else:
        j = octBandLow1(fl, fu)[1]
        k = octBandHigh1(fl, fu)[1]
    #print(j, k, octs[j][2])

    for i in range(0, (k-j)+1):
        if i ==0:
            octB = [octs[i+j]]
        else:
            octB += [octs[i+j]]
        #print(oct13B)
        octB[i] += [octFL(octs[i+j][2])]
        octB[i] += [octFU(octs[i+j][2])]
        
    return octB   

    
#=============== 1/3 octave band functions ====================
    
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
    oct13 = [[-28,	0.008,	0.0199526231496888],
             [-27,	0.016,	0.0251188643150958],
             [-26,	0.0315,	0.0316227766016838],
             [-25,	0.04,	0.0398107170553497],
             [-24,	0.05,	0.0501187233627272],
             [-23,	0.063,	0.0630957344480193],
             [-22,	0.08,   0.0794328234724281],
             [-21,	0.1, 	0.1],
             [-20,	0.125,	0.125892541179417],
             [-19,	0.16,   0.158489319246111],
             [-18,	0.2,  	0.199526231496888],
             [-17,	0.25,	0.251188643150958],
             [-16,	0.315,	0.316227766016838],
             [-15,	0.4,  	0.398107170553497],
             [-14,	0.5,  	0.501187233627272],
             [-13,  0.63,  	0.630957344480193],
             [-12,	0.8,  	0.794328234724281],
             [-11,  1,     	1],
             [-10,	1.25,   1.25892541179417],
             [-9,   1.6,    1.58489319246111],
             [-8,   2,	    1.99526231496888],
             [-7,   2.5,   	2.51188643150958],
             [-6,   3.15,	3.16227766016838],
             [-5, 	4, 	    3.98107170553497],
             [-4, 	5,   	5.01187233627272],
             [-3,   6.3, 	6.30957344480193],
             [-2, 	8,   	7.94328234724282],
             [-1, 	10,  	10],
             [0,  	12.5,   12.5892541179417],
             [1,  	16,  	15.8489319246111],
             [2,  	20,  	19.9526231496888],
             [3,  	25,  	25.1188643150958],
             [4,  	31.5,   31.6227766016838],
             [5,  	40,  	39.8107170553498],
             [6,    50,     50.1187233627272]]
 
    return oct13

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
    
    fl = fc/2**(1/6)
    
    return fl

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
    
    fu = fc*2**(1/6)
    
    return fu

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
    oct13BL = octave13()
    for i in range(0, len(oct13BL)):
        o13bl = oct13FL(oct13BL[i][2])
        if o13bl >= fl:
            break
        
    if oct13FU(oct13BL[i][2]) > fu:
        print('Filter bandwidth narrower than 1 octave!')
    else:
        return oct13BL[i], i

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
    oct13BH = octave13()
    for i in range(0, len(oct13BH)):
        o13bu = oct13FU(oct13BH[i][2])
        if o13bu > fu:
            break
    i-=1    
    if oct13FL(oct13BH[i][2]) < fl:
        print('Filter bandwidth narrower than 1 octave!')
    else:
        return oct13BH[i], i

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
    oct13BL = octave13()
    for i in range(0, len(oct13BL)):
        o13bl = oct13FL(oct13BL[i][2])
        if o13bl >= fl:
            break
    
    i -= 1
    return oct13BL[i], i

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
    oct13BH = octave13()
    for i in range(0, len(oct13BH)):
        o13bu = oct13FU(oct13BH[i][2])
        if o13bu > fu:
            break

    return oct13BH[i], i

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
    oct13B = [[]]
    #print(oct13B)
    oct13s = octave13()
    
    if within:
        j = oct13BandLow(fl, fu)[1]
        k = oct13BandHigh(fl, fu)[1]
    else:
        j = oct13BandLow1(fl, fu)[1]
        k = oct13BandHigh1(fl, fu)[1]
    #print(j, k, oct13s[j][2])

    for i in range(0, (k-j)+1):
        if i ==0:
            oct13B = [oct13s[i+j]]
        else:
            oct13B += [oct13s[i+j]]
        #print(oct13B)
        oct13B[i] += [oct13FL(oct13s[i+j][2])]
        oct13B[i] += [oct13FU(oct13s[i+j][2])]
        
    return oct13B   


#==================== sum waveforms =====================
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
    c = a.copy()
    c[0].data = a[0].data+b[0].data
    
    return c

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
    c = st[0].copy()
    for i in range (1, len(st)):
        c.data = c.data + st[i].data
        
    return c
    
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
    for i in range (0, len(a)):
        ax.axvline(a[i][3], lw=1, linestyle='--', color='g')
        
    ax.axvline(a[i][4], lw=1, linestyle='--', color='g')
    
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
    z.stats.max = peak(z)
    z.stats.mean = average(z)
    z.stats.rms = rms(z)
    
    return z
    
            
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
    st = a.copy()
    for i in range (0, len(bands)):
        b = a.copy()
        if i ==0:
            st[i].data = filter.bandpass(b[0], bands[i][3], bands[i][4], 100, corners=4, zerophase=True)
            
        else:
            b[0].data = filter.bandpass(b[0], bands[i][3], bands[i][4], 100, corners=4, zerophase=True)
            st.append(b[0])
        st[i].stats.filter = str(bands[i][3])+' - '+str(bands[i][4])+' Hz'
        update_trace_stats(st[i])
    
    return st

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
    n = len(a)

    fig1 = plt.figure(figsize=(12,18), dpi=150)    #12 x 18 inches

    a.plot(fig = fig1, automerge = False, equal_scale = False)
    fig1.suptitle(title1+' '+title2)

    for i in range (0, n):
        fig1.text(0.94, (i+0.3)/(n+0.5), a[i].stats.filter, size = 'x-small', ha = 'right')
        fig1.text(0.11, (i+0.3)/(n+0.5), 'Max/Mean/RMS: '+str(a[i].stats.max)+' / '+str(a[i].stats.mean)+' / '+str(a[i].stats.rms), size = 'x-small', color='r')

    # save the final figure if the plot is ready
    if save:
        plt.savefig(file+title2+'.png')

    # show the final figure
    plt.show()

    
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
    
    j = 0
    bandGs = []
    for i in range(0, len(f)):
        if f[i] >= bands[j][3]:
            if f[i] > bands[j][4]:
                j += 1
                if j > len(bands)-1:
                    break
                bandGs.append([fftL[i], fftG[i]])
            else:
                if bandGs == []:
                    bandGs.append([fftL[i], fftG[i]])
                elif fftL[i] > bandGs[j][0]:
                    bandGs[j] = [fftL[i], fftG[i]]
                    
    return bandGs

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
    gwaves = lwaves.copy()
    for i in range(0, len(lwaves)):
        gwaves[i].data = lwaves[i].data*bandGs[i][1]/bandGs[i][0] 
        gwaves[i] = update_trace_stats(gwaves[i])
        
    return gwaves