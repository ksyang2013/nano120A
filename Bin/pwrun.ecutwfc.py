#!/usr/bin/python
#writen by Prof. Kesong Yang (kesong@ucsd.edu) for NANO110 in Oct. 2017
#Revised for NANO120A, 2023
#Usage Example: python pwrun.ecutwfc.py ./ 10:5:50

import os, os.path, sys, re
from os import listdir
from os.path import isfile, join

if len(sys.argv) != 3:
    sys.stderr.write("Usage Example: python pwrun.ecutwfc.py ./ 10:5:50\n")
    exit(0)

list_ecutwfc = []
mypath = sys.argv[1]
s = str(sys.argv[2])
etmp = s.split(":")
for i in range(int(etmp[0]),int(etmp[2])+1,int(etmp[1])):
    list_ecutwfc.append(i)

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in onlyfiles:
    if "scf.in" in i:
        pwfile = i.split(".")[0]+".scf.in"

pwin = open(pwfile,'r')
pwin_lines = pwin.readlines()
count_lines = len(pwin_lines)

print (list_ecutwfc)
for i in range(0,len(list_ecutwfc)):
    ecut = list_ecutwfc[i]
    cur_dir = os.getcwd()
    abs_path = os.path.abspath(cur_dir)
    if os.path.exists(str(ecut)):
        sys.stderr.write("Folder " + str(ecut) + " Exists!\n")
    else:
        command = "mkdir " + str(ecut)
        os.system(command)
    os.chdir(str(ecut))
    cp_cmd = "cp ../*UPF ."
    os.system(cp_cmd)
    print (abs_path + "/" + str(ecut))
    fout = open(pwfile,'w')
    for j in range(0,count_lines):
        line = pwin_lines[j]
        if (line.find("ecutwfc")>=0):
            newline = re.sub("ecutwfc.*?,", "ecutwfc= " + str("%.1f" % ecut) +",", line, re.DOTALL)
            fout.write("%s" % newline)
        else :
            fout.write("%s" % line)
        fout.flush()
    fout.close()
    os.chdir(abs_path)

#Next generate a sbatch script for the job

pw_sbatch = open('sbatch.expanse.pw_x.ecut.sh', 'w')
str_sbatch = """#!/bin/bash
#SBATCH --account=csd709          #account name
#SBATCH --nodes=1                 #no. of nodes
#SBATCH --partition=shared       #job runing type
#SBATCH --ntasks-per-node=16      #no. of taks (cpu cores) per node
#SBATCH --time=00:30:00
#SBATCH --error=myjob.err
#SBATCH --output=myjob.out
#SBATCH --job-name=nano120A        #job name
#SBATCH --mail-type=ALL

module purge
module load slurm
module load cpu
module load gcc/9.2.0
module load openmpi
module load quantum-espresso/6.7.0-openblas

### Run QE
export OMP_NUM_THREADS=1
"""

newline=""
for i in range(0,len(list_ecutwfc)):
    ecut = list_ecutwfc[i]
    newline = "cd " + str(ecut) + "\n";
    newline = newline + "mpirun --map-by core --mca btl_openib_if_include \"mlx5_2:1\" --mca btl openib,self,vader pw.x < " + pwfile + " >  " + pwfile.replace("in", "out") + "\n"
    newline = newline + "cd ..\n"
    str_sbatch = str_sbatch + newline;
pw_sbatch.write("%s" % str_sbatch)


