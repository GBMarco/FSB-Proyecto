#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# prueba.py
#
# Authors: Sandra Susana Pérez Gutiérrez
#	   Brandon Silva Barrera
#	   Javier Adán Troncoso Moreno
#		García Barriga Marco Antonio
# Licence: MIT
# Date:    2022.05.22
# 
# Auxiliary program to lauch the usb functions. 
#
# ## #############################################################
import usb_access
import sys
#usb_access.start_usb_function()
print("/media/centro_multimedia/"+" ".join(sys.argv[1:])+"/")
usb_access.interface_usb("/media/centro_multimedia/"+" ".join(sys.argv[1:])+"/", True)
