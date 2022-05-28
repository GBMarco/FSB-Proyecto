#!/usr/bin/env python3
# -- coding: utf-8 --
# ## #############################################################
# usb_access.py
#
# Authors: Sandra Susana Pérez Gutiérrez
#	   Brandon Silva Barrera
#	   Javier Adán Troncoso Moreno
#		García Barriga Marco Antonio
# Licence: MIT
# Date:    2022.04.03
# 

# Functions to play the multimedia of an USB memory. 
#
# ## #############################################################

import os
import time
import tkinter 
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import vlc
import ctypes 
import math

#Library used by VLC player
x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XInitThreads()

#To play media in VLC with a button 
def play(player, root, button):
	player.play()
	button.destroy()
	button_pause = tkinter.Button(root, text = "Pausar", width = 30, command = lambda: pause(player, root, button_pause))
	button_pause.pack()
	
#To pause media in VLC with a button
def pause(player, root, button):
	player.pause()
	button.destroy()
	button_play = tkinter.Button(root, text = "Reproducir", width = 30, command = lambda: play(player, root, button_play))
	button_play.pack()
	
#To stop the player of VLC and relaunch the file selection.
def stop(player, root, path_usb):
	player.stop()
	relaunch(root, path_usb)

def play_multimedia(path_multimedia, root, path_usb):
	root.destroy()
	playing = tkinter.Tk()
	playing.title("Reproduciendo " + path_multimedia)
	playing.geometry("500x100")
	
	try:
		#Play the media with VLC.
		player = vlc.MediaPlayer(path_multimedia)
		player.play()
		
		button_stop = tkinter.Button(playing, text = "Escoger otro archivo", width = 30, command = lambda: stop(player, playing, path_usb))
		button_stop.pack()
		
		button_pause = tkinter.Button(playing, text = "Pausar", width = 30, command = lambda: pause(player, playing, button_pause))
		button_pause.pack()
	except: 
		label_error = tkinter.Label(root, text = "Error al reproducir el video, intente nuevamente por favor.")
		label_error.pack()
		raise RuntimeError('Fallo al reproducir multimedia')
	#When the multimedia ends the window is closed and the interfaz
	#is relaunched
	time.sleep(1)
	duration_multimedia = player.get_length() + 1000
	#At the end of playing the media, the window closes and a file is requested again. 
	playing.after(duration_multimedia, stop, player, playing, path_usb)
	playing.mainloop()

def play_music(path_usb, root):
	root.destroy()
	#Window to close the bucle when is closed
	aux_window = tkinter.Tk()
	aux_window.title("Detener reproducción de audios")
	label = tkinter.Label(aux_window, text = "Cierre esta ventana para detener el bucle")
	label.pack()
	#Find the names of the files in the USB
	files = get_files_name(path_usb)
	audio_files = []
	# Save only the names the audios in a list
	for arch in files:
		if (arch[-4:] == ".mp3"):
			audio_files.append(arch)
	#Make the required objects to play the media in VLC
	media_player = vlc.MediaListPlayer()
	player = vlc.Instance()
	#Collect the audios in a VLC media list 
	media_list = player.media_list_new()
	for audio in audio_files:
		media = player.media_new(path_usb + audio)
		media_list.add_media(media)
	#Play the list in a bucle	
	media_player.set_media_list(media_list)	
	media_player.set_playback_mode(vlc.PlaybackMode.loop)
	media_player.play()
	
	aux_window.mainloop()

#To choose between play one video or all in loop.			
def video_mode(path_usb, root):
	root.destroy()
	video_mode = tkinter.Tk()
	video_mode.title("Elegir modo de video")
	video_mode.geometry("500x100")
	button1 = tkinter.Button(video_mode, text = "Reproducir videos uno tras otro", width = 30, command = lambda: play_videos(video_mode, path_usb))
	button1.pack()
	button2 = tkinter.Button(video_mode, text = "Seleccionar un video", width = 30, command = lambda: play_video(video_mode, path_usb))
	button2.pack()
	
#Play one video
def play_video(root, path_usb):
	root.destroy()
	window = tkinter.Tk()
	window.title("Elegir video")
	window.geometry("500x100")
	label_select = tkinter.Label(window, text = "No se ha seleccionado un archivo multimedia")
	label_select.pack()
	#A video file is chosen.
	path_multimedia = filedialog.askopenfilename(initialdir = path_usb, filetypes = [
		("all video format", ".mp4"),
		("all video format", ".avi")])
	
	if len(path_multimedia) > 0:
		if (path_multimedia[-4:] == ".mp4") or (path_multimedia[-4] == ".avi"):
			#If a video file is chosen then it is played.
			play_multimedia(path_multimedia, window, path_usb)
	
def play_videos(root, path_usb):
	root.destroy()
	#Window to close the bucle when is closed
	aux_window = tkinter.Tk()
	aux_window.title("Detener reproducción de videos")
	label = tkinter.Label(aux_window, text = "Cierre esta ventana para detener el bucle")
	label.pack()
	files = get_files_name(path_usb)
	video_files = []
	# Save only the names of videos in a list
	for arch in files:
		if (arch[-4:] == ".mp4") or (arch[-4:] == ".avi"):
			video_files.append(arch)
	#Make the required objects to play the media in VLC
	media_player = vlc.MediaListPlayer()
	player = vlc.Instance()
	#Collect the audios in a VLC media list 
	media_list = player.media_list_new()
	for video in video_files:
		media = player.media_new(path_usb + video)
		media_list.add_media(media)
	#Play the list in a loop.	
	media_player.set_media_list(media_list)	
	media_player.set_playback_mode(vlc.PlaybackMode.loop)
	media_player.play()
	
	aux_window.mainloop()

def show_image(path_image, root, path_usb):
	#Width and height must be adapted to the size of window.
	size_max_width = 750
	size_max_height = 500
	root.destroy()
	window = tkinter.Tk()
	window.attributes("-zoomed", True)
	window.title("Mostrando imagen " + path_image)
	#Image preparation with the pillow library.
	image_unprepared = Image.open(path_image)
	size = image_unprepared.size
	if size[0] > size_max_width:
		image_unprepared = image_unprepared.resize((size_max_width, math.floor((size_max_width/size[0])*size[1])))
		size = image_unprepared.size
	if size[1] > size_max_height:
		image_unprepared = image_unprepared.resize((math.floor((size_max_height/size[1])*size[0]), size_max_height))
	window.image_unprepared = ImageTk.PhotoImage(image_unprepared)
	#Show the imagen in a label
	image_prepared = tkinter.Label(window, image = window.image_unprepared)
	image_prepared.pack()
	#Relaunch the file selection.
	button_stop = tkinter.Button(window, text = "Escoger otro archivo", width = 30, command = lambda: relaunch(window, path_usb))
	button_stop.pack()
	window.mainloop()

#Global variable to make a index to show images in loop.
index = None

#Function used by tkinter to refresh the image in the window
def change_index(window, image_duration ,len_list, image_prepared, path_usb, image_files):
	global index
	if index >= len_list - 1:
		index = 0
	else:
		index = index + 1
		#print(index)
	path_image = path_usb + image_files[index]
	size_max_width = 750
	size_max_height = 750
	#Image preparation with the pillow library.
	image_unprepared = Image.open(path_image)
	size = image_unprepared.size
	if size[0] > size_max_width:
		image_unprepared = image_unprepared.resize((size_max_width, math.floor((size_max_width/size[0])*size[1])))
		size = image_unprepared.size
	if size[1] > size_max_height:
		image_unprepared = image_unprepared.resize((math.floor((size_max_height/size[1])*size[0]), size_max_height))
	window.image_unprepared = ImageTk.PhotoImage(image_unprepared)
	image_prepared.config(image = window.image_unprepared)
	#Refresh the image and pass the information required to the next image.
	window.after(image_duration*1000, change_index, window, image_duration, len(image_files), image_prepared, path_usb, image_files)

#Show images in a loop.
def show_images(path_usb, root):
	global index
	index = 0
	#Image duration in the window 
	image_duration = 1

	root.destroy()
	#Make a list of images in USB memory.
	files = get_files_name(path_usb)
	image_files = []
	# Save the names of images in a list
	for image in files:
		if (image[-4:] == ".png") or (image[-4:] == ".jpg") or (image[-5:] == ".jpeg"):
			image_files.append(image)
			
	#Show all the images in certain time interval
	path_image = path_usb + image_files[index]
	size_max_width = 750
	size_max_height = 750
	window = tkinter.Tk()
	window.attributes("-zoomed", True)
	window.title("Mostrando imágenes ")
	#Image preparation with the pillow library.
	image_unprepared = Image.open(path_image)
	size = image_unprepared.size
	if size[0] > size_max_width:
		image_unprepared = image_unprepared.resize((size_max_width, math.floor((size_max_width/size[0])*size[1])))
		size = image_unprepared.size
	if size[1] > size_max_height:
		image_unprepared = image_unprepared.resize((math.floor((size_max_height/size[1])*size[0]), size_max_height))
	window.image_unprepared = ImageTk.PhotoImage(image_unprepared)
	#Put the image in the window
	image_prepared = tkinter.Label(window, image = window.image_unprepared)
	image_prepared.pack()
	#Refresh image in the window and send the information required to show
	#The next image
	window.after(image_duration*1000, change_index, window, image_duration, len(image_files), image_prepared, path_usb, image_files)

	window.mainloop()
	
#To choose a media file from USB memory.	
def choose_multimedia(path_usb, root):
	label_select = tkinter.Label(root, text = "No se ha seleccionado un archivo multimedia")
	label_select.pack()
	path_multimedia = filedialog.askopenfilename(initialdir = path_usb, filetypes = [
		("image", ".jpg"),
		("image", ".jpeg"),
		("image", ".png"),
		("all video format", ".mp4"),
		("all video format", ".avi"),
		("audio files", ".mp3")])
	#If a file is chosen then run the appropriate function. 
	if len(path_multimedia) > 0:
		label_select.configure(text = path_multimedia)
		if (path_multimedia[-4:] == ".mp4") or (path_multimedia[-4] == ".avi"):
			play_multimedia(path_multimedia, root, path_usb)
		elif (path_multimedia[-4:] == ".jpg") or (path_multimedia[-5] == ".jpeg") or (path_multimedia[-4:] == ".png"):
			show_image(path_multimedia, root, path_usb)
		elif (path_multimedia[-4:] == ".mp3") or (path_multimedia[-4] == ".avi"):
			play_multimedia(path_multimedia, root, path_usb)
	else: #When a file is not chosen.
		label_select.configure(text = "No se ha seleccionado un archivo multimedia")
	
def get_USBs_name():
	#Search the USBs conected.
	try:
		names_usb_files = os.listdir("/media/centro_multimedia/")
	except FileNotFoundError:
		raise RuntimeError('Failed to open USB and know its files')
	except:
		raise RuntimeError('Failed to open USB')
	
	return names_usb_files

def get_files_name(path_usb):
	#The memory content is reviewed.
	try:
		#The names of the files are obtained.
		names_usb_files = [arch for arch in os.listdir(path_usb) if os.path.isfile(os.path.join(path_usb, arch))]
	except FileNotFoundError:
		raise RuntimeError('Failed to open USB and know its files')
	except:
		raise RuntimeError('Failed to open USB')
	
	return names_usb_files
	
#The functionalities are chosen with a flag system that depends on the type of files. 
def identify_files_type(names_usb_files):
	is_music, is_video, is_photo = False, False, False 
	for arch in names_usb_files:
		if arch[-4:]=='.mp3':
			is_music = True
		if (arch[-4:]=='.mp4') or (arch[-4:]=='.avi'):
			is_video = True
		if (arch[-4:]=='.png') or (arch[-4:]=='.jpg'):
			is_photo = True
		if (is_music == True) and (is_video == True) and (is_photo == True):
			break
	flags = [is_music, is_video, is_photo]
	return flags

#Return the functionality to be executed with the flags of files in USB.
def play_mode(path_usb):
	names_usb_files = get_files_name(path_usb)
	flags_files_type = identify_files_type(names_usb_files) #[is_music, is_video, is_photo]
	if (flags_files_type[0]==False) and (flags_files_type[1]==False) and (flags_files_type[2]==False):
		return "no_media_in_usb"#no_media_in_usb()
	elif (flags_files_type[0]==True) and (flags_files_type[1]==False) and (flags_files_type[2]==False):
		return "music"
	elif (flags_files_type[0]==False) and (flags_files_type[1]==True) and (flags_files_type[2]==False):
		return "video"
	elif (flags_files_type[0]==False) and (flags_files_type[1]==False) and (flags_files_type[2]==True):
		return "photo"
	else:
		return "multimedia"
	
#Launch the 
def interface_usb(path_usb, usb_connected):
	root = tkinter.Tk()
	root.geometry("500x200")
	root.title("Reproductor multimedia")
	if usb_connected==True:
		label_root = tkinter.Label(root, text = "Memoria USB conectada")
		label_root.pack()
		action = play_mode(path_usb)
	else:
		label_root = tkinter.Label(root, text = "No se ha detectado una memoria USB conectada")
		label_root.pack()
	#Execute the appropriate function to play the media.	
	if action == "multimedia":
		button1 = tkinter.Button(root, text = "Elegir archivo", width = 30, command = lambda: choose_multimedia(path_usb, root))
		button1.pack()
	elif action == "music":
		button1 = tkinter.Button(root, text = "Reproducir audios en bucle infinito", width = 30, command = lambda: play_music(path_usb, root))
		button1.pack()
	elif action == "video":
		label1 = tkinter.Label(root, text = "Reproduciendo video")
		label1.pack()
		video_mode(path_usb, root)
	elif action == "photo":
		label1 = tkinter.Label(root, text = "Reproduciendo imágenes")
		label1.pack()
		show_images(path_usb, root)
	else: #When there are no media files.
		label1 = tkinter.Label(root, text = "No se detectó algún archivo multimedia en la USB")
		label1.pack()
		label2 = tkinter.Label(root, text = "Formatos válidos \n Imágenes: jpg, jpeg y png \n Videos: avi y mp4 \n Audio: mp3")
		label2.pack()
		
	root.mainloop()

#Relaunch the interface that runs the appropriate functionality.
def relaunch(root, path_usb):
	#print(path_usb + "re")
	root.destroy()
	interface_usb(path_usb, True)	
	
#Initial interface.
#Show the USB conected and the user choose one if there are several.
#If are one USB interface_usb function is launched.
#when there are no USB then a message is displayed.
#In case of error a warning message is displayed. 
def start_usb_function():
	pre_path_usb = "/media/centro_multimedia/"
	list_usb = get_USBs_name()
	if len(list_usb) == 0:
		root = tkinter.Tk()
		root.geometry("300x100")
		root.title("No se detectó alguna USB conectada")
		root.mainloop()
	elif len(list_usb) == 1:
		interface_usb(pre_path_usb + list_usb[0] + "/", True)
	elif len(list_usb) > 1:
		root = tkinter.Tk()
		root.geometry("500x200")
		root.title("Escoja la USB desde donde se reproducirá la multimedia")	
		#Buttons to choose an USB.
		for i in range(0, len(list_usb)):
			tkinter.Button(root, text = list_usb[i], width = 30, command = lambda i=i: relaunch(root, pre_path_usb + list_usb[i] + "/")).pack()
			
		root.mainloop()
	else:
		root = tkinter.Tk()
		root.geometry("300x100")
		root.title("Ocurrió un error, intente de nuevo por favor")
		root.mainloop()
