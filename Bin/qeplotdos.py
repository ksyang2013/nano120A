#!/usr/bin/env python  

"""
File Name: qeplotdos2.py
Created Time: 2022-01-06 16:53:09
Author: Prof. KESONG YANG,  UC San Diego  
Mail: kesong@ucsd.edu

A simple python code to plot density of states (DOS) produced from Quantum Espresso 
This script uses pandas, matplotlib
Usage example: qeplotdos.py Si2_dos.dat
"""

import pandas as pd
import matplotlib.pyplot as plt
import os, os.path, sys, re, bz2

dosfile = sys.argv[1]
system_name = dosfile.replace(".dat","")

with open(dosfile, 'r', encoding='utf-8') as f:
    lines = f.read()
    first = lines.split("\n")[0]
    vdata = first.split()
    Efermi = float(vdata[-2])

data = pd.read_csv(dosfile, header=1, delim_whitespace=True)
num_col = len(data.columns)
E = data[data.columns[0]] - Efermi
S = data[data.columns[1]]
fig, ax = plt.subplots()
ax.plot(E, S, '-')
plt.axvline(x=0, color='r', linestyle='--')
textstr = '$E_f$'
ax.text(0.2, max(S)*0.95, textstr)
plt.xlim(-6, 4)
plt.ylim((0, max(S)*1.1))
plt.xlabel('Energy (eV)')
plt.ylabel('Density of States')
outfile = system_name + "_DOS.eps"
plt.savefig(outfile, format='eps', dpi=1000)
#os.system("open " + outfile)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

