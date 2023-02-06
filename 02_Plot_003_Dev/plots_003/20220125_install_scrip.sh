#!/bin/bash
# install script to create paper specific python environemnt
# SMG 20220127
# should be run whenever environment is altered using ./"this script" from paper python directory

#python3.8 -m venv venv_003    # create an environment

activate(){
        . venv_003/bin/activate # activate the environment
}
activate 



