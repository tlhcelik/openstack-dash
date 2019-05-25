#!/bin/bash

cd
source admin-openrc.sh
cd openstack-dash
nohup python main.py & > outputs
