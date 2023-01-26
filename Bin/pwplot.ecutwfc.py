#!/usr/bin/python
#writen by Prof. Kesong Yang (kesong@ucsd.edu) for NANO110 in Nov. 2017
#usage: python ./pwplot.ecutwfc.py ./

import os, os.path, sys, re, bz2
from os import listdir
from os.path import isfile, join

if len(sys.argv) !=2:
    sys.stderr.write("Usage: python ./pwplot.ecutwfc.py ./\n")
    exit(0)

dirs = [d for d in os.listdir('.') if os.path.isdir(d)]

dirs_num = []
List_ENCUT =[]
List_TOTEN  =[]
List_TOTEN_PER_ATOM  =[]

mypath = sys.argv[1]
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyfiles:
    if "scf.in" in i:
        pwfile_in = i.split(".")[0]+".scf.in"
pwfile_out = pwfile_in.replace("in","out")

#Function to get TOTEN from PWOUT
def GetTotenFromPWOUT(directory):
    TOTEN = 0
    file_outcar =  open(directory+'/'+pwfile_out, 'r')
    for line in file_outcar:
        if (line.find("!    total energy              =")> -1):
            data = [x.strip() for x in line.split()]
            TOTEN = data[-2]
    file_outcar.close()
    return TOTEN;

outcar_dir = dirs[0]
TOTEN = GetTotenFromPWOUT(outcar_dir)

for d in dirs:
    dirs_num.append(int(d))
dirs_num.sort()

for d_num in dirs_num:
    List_ENCUT.append(d_num)
    TOTEN_i = GetTotenFromPWOUT(str(d_num))
    List_TOTEN.append(float(TOTEN_i))

file_data = open("data.txt", "w")
for i in range(0,len(List_ENCUT)):
    s = str(List_ENCUT[i]) + "  " + str(List_TOTEN[i]) + '  \n'
    file_data.write(s)
file_data.close()    



eps_name = pwfile_in.replace(".scf.in", "") + '_toten_ecut.eps'
png_name = eps_name.replace("eps", "png")

file_plot = open("gnuplot_cutoff.gp", "w")
script = """#written by Kesong Yang [kesong@ucsd.edu], 2016, UCSD
    set terminal postscript color portrait dashed enhanced 'Times-Roman'
    """ 
script += 'set output "'
script += eps_name
script += "\"\n"
script += "set title \""
script += "   [TOTEN vs. Cutoff Energy]"
script += "\"\n"
script += """
    set ylabel "Total Energy/atom (Ry)"
    set xlabel 'Cutoff Energy (Ry)'

    plot 'data.txt' using 1:2w lp pt 7 ps 2 lc 3 lt -1 title "Total Energy (Ry)"
    """

file_plot.write("%s" % script)
file_plot.close()

os.system("gnuplot gnuplot_cutoff.gp")
cmd_convert = 'convert ' + eps_name + ' ' + png_name
os.system(cmd_convert)

