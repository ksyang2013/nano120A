To use scripts, one needs to install pandas, matplotlib by running following commands:

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install matplotlib
pip install pandas

After finishing the above commands, run the the command "chmod +x *.py" to make these scripts executable.

To use these scripts, you have two options:

Option 1: Copy the scripts that you would like to use to your working directory and use it. Example: ./qerun.py "pw.x < Si2.scf.in > Si2.scf.out"

Option 2: To avoid the copy command each time, you may add the current path (use "pwd" command to get your path) to your .bashrc file (in the end of your .bashrc). See example below:

export PATH="$PATH:/home/key021/temp_project/nano120A/Bin:."

After doing above, use command "source ~/.bashrc" or log out and log in to make it take effect. 


