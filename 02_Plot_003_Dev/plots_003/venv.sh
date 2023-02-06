#!/bin/bash

# install script to create paper specific python environemnt
# SMG 20220127+PO edited 20220430
# should be run whenever environment is altered using ./"this script" from paper python directory

#a) create an enviroment 
#b) activate the enviroment
#c) install all the requiremnts 

python3.8 -m venv venv_003    # a) create an environment



#b) activate the enviroment 
#------------------1)trick to activate the enviroment is to get absolute path to the current folder----
#------------------2)Then add it to the line startted with source path+name of the env+ /bin/activate
#------------------3)then call the script in terminal using: source and the name of the script 


# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
#echo $SCRIPTPATH

# Let's call this script venv.sh

#source "/home/stiladmin/development/testP1repo/Dev/plots_003/venv_003/bin/activate"
source "$SCRIPTPATH/venv_003/bin/activate"

#install all the requiremnts 
pip3 install --upgrade pip
pip3 install packaging
pip install -r requirements.txt # install all the requirements (libraries)
