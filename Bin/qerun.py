#!/usr/bin/env python  

"""
File Name: qerun.py
Created Time: 2021-12-30 21:39:10
Author: Prof. KESONG YANG,  UC San Diego  
Email: kesong@ucsd.edu

A simple python code to generate job script for Quantum Espresso on Expanse@XSEDE and submit the job
Usage example: qerun.py  "pw.x < Si2.scf.in > Si2.scf.out"
"""

import sys,os,getpass

if len(sys.argv) == 2 :
    strCmd = sys.argv[1]
else:
    sys.stderr.write("usage: python program.py ...")
    exit(0)

strJobScript="""#!/bin/bash
#SBATCH --account=csd709
#SBATCH --nodes=1
#SBATCH --partition=shared
#SBATCH --ntasks-per-node=16
#SBATCH --time  00:60:00
#SBATCH -e  err.%j
#SBATCH -o  out.%j
#SBATCH --job-name  nano120A
#SBATCH --export=ALL

module purge
module load slurm
module load cpu
module load gcc/9.2.0
module load openmpi
module load quantum-espresso/6.7.0-openblas

### Run QE
export OMP_NUM_THREADS=1
mpirun --map-by core --mca btl_openib_if_include "mlx5_2:1" --mca btl openib,self,vader  """

strJobScript = strJobScript + strCmd + "\n"

jobScript = "jobscript_qe.sh"
fid = open(jobScript, "w")
n = fid.write(strJobScript)
fid.close()

#print("Generating job script :\n")
#print(strJobScript)
os.system("sbatch " + jobScript)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

