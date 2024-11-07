# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 03:27:00 2024

@author: jo_cb
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import eqsig as eq

#%% Input
wall_number_tag = '1'       # Use '1', '2' or '3'
measurment = 'd'            # Use 'a' for acceleration, 'd' for laser displacement
case = 1                    # index of the desired test "case_tag"
accelerometer = 2           # 0 for "sis" accelerometer, 
                            # 1 for 'IP' and 2 for 'OoP' accelerometers
laser = 1                   # 0 for base displacement laser sensor and
                            # 1 for top displacement laser sensor

#%% Functions
case_tags = ['025', '050', 'WN1', '075',
             'WN2', '100', 'WN3', '150',
             'WN4', 'Sine_sweep', 'WN5']

if wall_number_tag == '1' or wall_number_tag == '2' or wall_number_tag == '3':
    ntag = 1
else:
    ntag = 0

if measurment == 'a':
    if accelerometer == 0:
        acc_type = 'IP seismic'
    elif accelerometer == 1:
        acc_type = 'IP piezo-electric'
    elif accelerometer == 2:
        acc_type = 'OoP piezo-electric'
    else:
        acc_type = 0
    meas, disp_type = 1, 1
elif measurment == 'd':
    if laser == 0:
        disp_type = 'Base'
    elif laser == 1:
        disp_type = 'Top'
    meas, acc_type = 1, 1
else:
    meas = 0

if isinstance(case, int) and case < 11 and case >= 0:
    caso = 1
else:
    caso = 0

def procesar_data_acc(acc,dt=1/600.):
    """
    Minimum post-processing for acceleration data usage

    Parameters
    ----------
    acc : array with raw acceleration data. Notice, if eqsig will be used for
            further processing of the data, be sure to use the appropiate
            units.
    dt : float value with the inverse of the sample frequency (600 Hz)

    Returns
    -------
    acc : array with acceleration data in 200 Hz and rolling average correction

    """
    for i in range(1,len(acc)):
        if np.abs(acc[i]) > 10:
            acc[i] = acc[i-1]
    a = eq.AccSignal(acc,dt)
    a.remove_rolling_average(mtype='acceleration', freq_window=3) 
    a.remove_rolling_average(mtype='velocity', freq_window=3) 
    a.correct_me()
    a_raw = a.values
    
    acc = sp.signal.decimate(a_raw,3)
    a = eq.AccSignal(acc,dt/3)
    a.remove_rolling_average(mtype='acceleration', freq_window=3) 
    a.remove_rolling_average(mtype='velocity', freq_window=3) 
    a.correct_me()
    acc = a.values
    return acc

def procesar_data_disp(disp,dt=1/600.):
    """
    Minimum post-processing for displacement data usage

    Parameters
    ----------
    disp : array with raw displacement data.
    dt : float value with the inverse of the sample frequency (600 Hz)

    Returns
    -------
    d : array with displacement data in 200 Hz and average correction

    """
    d_raw = eq.Signal(disp, dt)
    d_raw.remove_average()
    d = sp.signal.decimate(d_raw.values,3)
    return d


#%% Retrieving data
if ntag != 0 and meas != 0 and acc_type != 0 and caso != 0:
    if measurment == 'a':
        ind = accelerometer
        file_name = f'Muro{wall_number_tag}_{measurment}_{case_tags[case]}.txt'
        a_raw = np.loadtxt(file_name)[ind]
        a = procesar_data_acc(a_raw)
        t_raw = np.loadtxt(f'Time_{case_tags[case]}.txt')
        t = sp.signal.decimate(t_raw,3)
        plt.plot(t,a)
        plt.xlabel('Time [sec]')
        plt.ylabel('Acceleration [g]')
        plt.title(f'{acc_type} acceleration of wall {wall_number_tag}')
    else:
        ind = laser
        file_name = f'Muro{wall_number_tag}_{measurment}_{case_tags[case]}.txt'
        d_raw = np.loadtxt(file_name)[ind]
        d = procesar_data_disp(d_raw)
        t_raw = np.loadtxt(f'Time_{case_tags[case]}.txt')
        t = sp.signal.decimate(t_raw,3)
        plt.plot(t,d)
        plt.xlabel('Time [sec]')
        plt.ylabel('Displacement [mm]')
        plt.title(f'{disp_type} IP displacement of wall {wall_number_tag}')
else:
    print('Please check input data.')
    if ntag == 0:
        print('Variable "wall_number_tag" should be a string equal to "1", "2" or "3".')
    if meas == 0:
        print('Variable "measurment" should be a string equal to "a" or "d".')
    if acc_type == 0:
        print('Variable "accelerometer" should be an integer equal to 0, 1 or 2.')
    if caso == 0:
        print('Variable "case" should be any integer from 0 to 10.')
