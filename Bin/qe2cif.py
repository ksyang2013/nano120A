#!/usr/bin/env python
#A short script for produce cif file from quantum espresso output file 
#Usage pwo2cif si.geo.out

import sys, numpy as np
from numpy import linalg as LA

def CalculatePara(latt_vec):
    a1= latt_vec[0,:]
    a2= latt_vec[1,:]
    a3= latt_vec[2,:]
    a, b, c = LA.norm(a1), LA.norm(a2), LA.norm(a3)
    cosBC = np.dot(a2,a3)/(b*c)
    cosAC = np.dot(a1,a3)/(a*c)
    cosAB = np.dot(a1,a2)/(a*b)
    alpha =np.degrees(np.arccos(cosBC))
    beta =np.degrees(np.arccos(cosAC))
    gamma =np.degrees(np.arccos(cosAB))
    return(a, b, c, alpha, beta, gamma)

def GenerateCIF(latt_vec, coor_atoms, list_atom_name):
    a, b, c, alpha, beta, gamma = CalculatePara(latt_vec)
    coor_atoms[:,0] = coor_atoms[:,0]*a/a
    coor_atoms[:,1] = coor_atoms[:,1]*a/b
    coor_atoms[:,2] = coor_atoms[:,2]*a/c
    str_cif=""
    str_cif += "loop_\n"
    str_cif += "Prof. Kesong Yang\n"
    str_cif += "kesong@ucsd.edu\n"
    str_cif += "Department of NanoEngineering, UC San Diego\n"
    str_cif += "data_ Title Generated from PW outputfile, written by Prof. Yang (kesong@ucsd.edu) for NANO110 in 2017, Revised for NANO120A in 2021\n"
    str_cif += "_pd_phase_name  Title\n"
    str_cif += "_cell_length_a " + str(a) + "\n"
    str_cif += "_cell_length_b " + str(b) + "\n"
    str_cif += "_cell_length_c " + str(c) + "\n"
    str_cif += "_cell_angle_alpha " + str(alpha) + "\n"
    str_cif += "_cell_angle_beta " + str(beta) + "\n"
    str_cif += "_cell_angle_gamma " + str(gamma) + "\n"
    str_cif += "_symmetry_space_group_name_H-M  'P1'" + "\n"
    str_cif += "_symmetry_Int_Tables_Number  1" + "\n"
    str_cif += "loop_" + "\n"
    str_cif += "_symmetry_equiv_pos_site_id" + "\n"
    str_cif += "_symmetry_equiv_pos_as_xyz_" + "\n"
    str_cif += "1 x,y,z" + "\n"
    str_cif += "loop_" + "\n"
    str_cif += "_atom_site_label" + "\n"
    str_cif += "_atom_site_occupancy" + "\n"
    str_cif += "_atom_site_fract_x" + "\n"
    str_cif += "_atom_site_fract_y" + "\n"
    str_cif += "_atom_site_fract_z" + "\n"
    str_cif += "_atom_site_thermal_displace_type" + "\n"
    str_cif += "_atom_site_B_iso_or_equiv" + "\n"
    str_cif += "_atom_site_type_symbol" + "\n"
    for i in range(0,nat):
        fract_xyz = str(coor_atoms[i,0]) + ' ' + str(coor_atoms[i,1]) + ' ' + str(coor_atoms[i,2])
        str_tmp = list_atom_name[i]+str(i+1)+' 1.0 ' + fract_xyz + ' Biso 1.0 ' + list_atom_name[i]
        str_cif += str_tmp + "\n"
    return str_cif

pwfile = sys.argv[1]

list_vec=[]
list_coor=[]
list_celldm_1=[]
list_celldm_2=[]
list_celldm_3=[]
coor_atoms_tmp = np.zeros(shape=(0,3))
list_coor_atoms = []
list_atom_name = []

fread_pw =  open(pwfile,'r')
for line in fread_pw:
    if (line.find("number of atoms/cell") > -1):
        data = [x.strip() for x in line.split()]
        nat=int(data[-1])
    if (line.find("celldm(1)=")> -1):
        data = [x.strip() for x in line.split()]
        list_celldm_1.append(float(data[1]))
        list_celldm_2.append(float(data[3]))
        list_celldm_3.append(float(data[5]))
    if (line.find("crystal axes:")> -1):
        a1 = next(fread_pw, '')
        data = [x.strip() for x in a1.split()]
        vec_a1 = np.array([float(data[3]), float(data[4]), float(data[5])])
        a2 = next(fread_pw, '')
        data = [x.strip() for x in a2.split()]
        vec_a2 = np.array([float(data[3]), float(data[4]), float(data[5])])
        a3 = next(fread_pw, '')
        data = [x.strip() for x in a3.split()]
        vec_a3 = np.array([float(data[3]), float(data[4]), float(data[5])])
        latt_vec = np.vstack((vec_a1, vec_a2, vec_a3))
        list_vec.append(latt_vec)
    if (line.find("site n.     atom") > -1):
        coor_atoms_i = np.zeros(shape=(0,3))
        coor_atoms_tmp = np.zeros(shape=(0,3))
        list_atom_name = []
        for i in range(0,nat):
            atom_i = next(fread_pw, '')
            data = [x.strip() for x in atom_i.split()]
            list_atom_name.append(data[1])
            coor_atom_i = np.array([float(data[6]), float(data[7]), float(data[8])])
            coor_atoms_tmp = np.vstack((coor_atoms_tmp, coor_atom_i))
        list_coor_atoms.append(coor_atoms_tmp)
fread_pw.close()

#calculate lattice parameters
latt_ini = list_vec[0]
a, b, c, alpha, beta, gamma = CalculatePara(latt_ini)
latt_last = list_vec[-1]
a, b, c, alpha, beta, gamma = CalculatePara(latt_last)

#Normalization to conver alat unit to "crystal" or "angstrom"
for i in range(0, len(list_celldm_1)):
    list_vec[i][0,:]*=list_celldm_1[0]*0.529177   #angstrom unit
    list_vec[i][1,:]*=list_celldm_1[0]*0.529177
    list_vec[i][2,:]*=list_celldm_1[0]*0.529177
    if abs(list_celldm_2[i]) > 1e-8:
        list_coor_atoms[i][:,1] /= list_celldm_2[i]
    else:
        list_coor_atoms[i][:,2] *= (b/a)                     #format it according to lattice vectors
    if abs(list_celldm_3[i]) > 1e-8:
        list_coor_atoms[i][:,2] /= list_celldm_3[i]                     #format it according to lattice vectors
    else:
        list_coor_atoms[i][:,2] *= (c/a)                     #format it according to lattice vectors
    list_coor_atoms[i][:,2] -= np.min(list_coor_atoms[i][:,2])   #put the atoms into the cell (c-axis)
    list_coor_atoms[i] = list_coor_atoms[i]*list_celldm_1[0]*0.529177   #get angstrom type
    list_coor_atoms[i] = np.dot(list_coor_atoms[i], LA.inv(list_vec[i])) #get crystal type
last_coor_atoms = list_coor_atoms[-1].astype(float)



str_cif = GenerateCIF(latt_last, last_coor_atoms, list_atom_name)
pwout_file = pwfile + ".cif"
fw_cif = open(pwout_file, "w")
fw_cif.write("%s" % str_cif)
fw_cif.close()
sys.stdout.write(pwout_file + " was successfully generated!\n")

