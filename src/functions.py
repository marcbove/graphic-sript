#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import askdirectory
import tkMessageBox, os, filecmp

dir_NameDst = ''
dir_NameSrc = ''
lista_ig = []
lista_semb = []
lista_x_act_src = [] 
lista_x_act_dest = []
lista_or = []
dicc_fitx_ig = {}
dicc_fitx_semb = {}

def dirName(name_dir):
	try:
		name_dir.set(os.path.abspath(askdirectory(title='Escoja un directorio', mustexist=1)))
	except AttributeError, e:
		pass
#Function 
def omplirDicc(fit_font):
	for path, dirs, files in os.walk(dir_NameDst.get()):
		for f in files:
			if f.endswith('txt'):
				a = f.replace(' ', '')
				for fi in fit_font:
					b = fi.replace(' ', '')
					if b == a and filecmp.cmp(dir_NameSrc.get()+'/'+fi, path+'/'+(f), shallow=False) and dir_NameSrc.get()!=path and (path.find("/home/milax/.local/share/Trash/files/") == -1) and not os.path.islink(path+'/'+f):
						if path+'/'+f not in dicc_fitx_ig[fi]:
							dicc_fitx_ig[fi].append(os.path.relpath(path+'/'+f))

					elif b == a and dir_NameSrc.get()!=path and not os.path.islink(path+'/'+f) and (path.find("/home/milax/.local/share/Trash/files/") == -1):
						if path+'/'+f not in dicc_fitx_semb[fi]:
							dicc_fitx_semb[fi].append(os.path.abspath(path+'/'+f))

#Cerca de fitxers semblants
def dicIgual():
	try:
		vaciarListas(lista_or)
		fit_font = filter(lambda x: x.endswith('.txt'), os.listdir(dir_NameSrc.get()))
		asd = os.listdir(dir_NameDst.get())
		omplirDicc(fit_font)
		fit_or = filter(lambda fil: fil in dicc_fitx_ig.keys() or fil in dicc_fitx_semb.keys(), fit_font)

		for var in fit_or:
			lista_or.insert(END, var)

	except OSError, e:
		tkMessageBox.showerror("Error", "Introduzca directorios!")

#Funcio que omple segons una Listbox i un diccionari una de les ListBox
def llenarListas(lista, diccionario):
	lista.delete(0,END)
	for key, val in diccionario.iteritems():
			for i in val:
				lista.insert(END, '~/'+os.path.relpath(i, dir_NameSrc.get()))

#Funció que selecciona tots els fitxers de la llista passada per paràmetre
def seleccionar_tots_or(lista):
	if not lista.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	else:
		if lista.size()!=len(lista.curselection()):
			lista.selection_set(0, END)
			llenarListas(lista_ig, dicc_fitx_ig)
			llenarListas(lista_semb, dicc_fitx_semb)
		
def seleccionar_tots(lista):
	if not lista.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	else:
		if lista.size()!=len(lista.curselection()):
			lista.selection_set(0, END)

def onselect(evt):
	click = evt.widget
	lista = []
	lista2 = []
	lista3 = []
	if click.get(0,END):
		
		for i in range (0, lista_ig.size()):
			lista.append(lista_ig.get(i))
		for i in range (0, lista_semb.size()):
			lista2.append(lista_semb.get(i))		

		for elem in click.curselection():
			lista3.append(click.get(elem))
		for elem in click.curselection():
				for key, value in dicc_fitx_semb.iteritems():
					if key in lista3:
						if key==click.get(elem):
							for i in value:
								c = i.replace(dir_NameDst.get(), '~')
								if c not in lista2:
									lista_semb.insert(END, c) #Hay que poner solo el relpath
									lista2.append(c)
					if key not in lista3:
						for i in value:
							c=i.replace(dir_NameDst.get(), '~')
							for a in range(0, lista_semb.size()):
								if c==lista_semb.get(-a):
									lista_semb.delete(-a)
									lista2.remove(c)

				for key, value in dicc_fitx_ig.iteritems():
					if key in lista3:
						if key==click.get(elem):
							for i in value:
								c=i.replace(dir_NameDst.get(), '~')
								if c not in lista:
									lista_ig.insert(END, c)	#Hay que poner solo el relpath
									lista.append(c)
		
					if key not in lista3:
						for i in value:
							c=i.replace(dir_NameDst.get(), '~')
							for a in range(0, lista_ig.size()):
								if c==lista_ig.get(-a):
									lista_ig.delete(-a)
									lista.remove(c)

	if len(click.curselection()) == 0:
		lista_ig.delete(0,END)
		lista_semb.delete(0,END)

		
				
def vaciarListas(lista):
	if lista.get(0,END):
		lista.delete(0, END)

#Funció que deselecciona tots els fitxers de la llista passada per paràmetre
def deseleccionar_tots_or(lista):
	if not lista.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	else:
		lista.selection_clear(0, END)
		vaciarListas(lista_ig)
		vaciarListas(lista_semb)

def deseleccionar_tots(lista):
	if not lista.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	else:
		lista.selection_clear(0, END)

#Funció que omple les llistes necessàries per la GUI de compara
def llena_Listas(lista_inode, lista_path, lista_num):
	for val in lista_semb.curselection():
		lista_inode.insert(END, os.stat(os.path.abspath(lista_semb.get(val).replace('~/', ''))).st_ino) 
		lista_path.insert(END, lista_semb.get(val).replace('~/', ''))
			
	lista_num_dest, lista_num_src = listas_semb_ig(lista_semb, dicc_fitx_semb)

	for i in range(0, len(lista_num_dest)):
		with open(lista_num_dest[i], 'r') as dest:
			dest_array = dest.read().split('\n')
		for elem in lista_or.get(0,END):
			if elem.replace(' ', '')==os.path.basename(lista_num_dest[i]).replace(' ', ''):
				fitx_or = dir_NameSrc.get()+'/'+elem
		with open(fitx_or , 'r') as src:
			src_array = src.read().split('\n')				
		lista_num.insert(END,len(filter(lambda x: x not in src_array, dest_array)))
				
#listas para pasar por parametros 
def listas_semb_ig(lista, diccionari_fitxer):
	lista_x_act_dest = [lista.get(i) for i in lista.curselection()]
	lista_x_act_src = []
	for key, value in diccionari_fitxer.iteritems():
		for i in range(0, len(lista_x_act_dest)):
			elem_x = os.path.abspath(dir_NameDst.get()+lista_x_act_dest[i].replace('~', ''))
			if elem_x in value:
				lista_x_act_src.append(key)
				lista_x_act_dest[i]=elem_x

	return lista_x_act_dest, lista_x_act_src

#Funció que linka segons el tipus que es passa per paràmetre
#Esborra de les estructures 
def link(type):
	if not lista_ig.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	elif lista_ig.curselection() == ():
		tkMessageBox.showinfo("Information", "Selecciona alguno de los ficheros de la lista")
	else: 
		lista_ig_x_dest, lista_ig_x_src = listas_semb_ig(lista_ig, dicc_fitx_ig)
		esborra(lista_ig, dicc_fitx_ig)
		for i in range (0, len(lista_ig_x_dest)):
			if type == 'soft':
				os.symlink(dir_NameSrc.get()+'/'+lista_ig_x_src[i],lista_ig_x_dest[i])
				
			elif type == 'hard':
				os.link(dir_NameSrc.get()+'/'+lista_ig_x_src[i],lista_ig_x_dest[i])
			
			else:
				print 'Tipo no correcto'


#Esborra els fitxers seleccionats dels directoris, llistes i diccionaris
def esborra(lista, diccionari):
	if not lista.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	elif lista.curselection() == ():
		tkMessageBox.showinfo("Information", "Selecciona alguno de los ficheros de la lista")
	else:
		#Obtenim les llistes amb tots els elements seleccionats (paths) de desti i font 
		lista_x_act_dest, lista_x_act_src = listas_semb_ig(lista, diccionari)
		#Per cada fitxer que esta activat en la llista es canvia el path pel complet, s'esborren els de desti de les carpetes, les listes i diccionaris
		for fitxer in lista_x_act_dest:
			fitxer=fitxer.replace('~',dir_NameDst.get())
			os.remove(fitxer)
			for key, value in diccionari.iteritems():
				if fitxer in value:
					diccionari[key].remove(fitxer)

		for elem_tupla in lista.curselection()[::-1]:
			lista.delete(elem_tupla)
		
#Renombra els fitxers activats de la llista de fitxers semblants canviant '.txt' per '(copia).txt'
#Esborra de la ListBox de fitxers semblants els fitxers als quals se'ls ha canviat el nom
def renombra():
	if not lista_semb.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	elif lista_semb.curselection() == ():
		tkMessageBox.showinfo("Information", "Selecciona alguno de los ficheros de la lista")
	else: 
		for a in lista_semb.curselection():
			b=lista_semb.get(a)
			copia = askstring('Input', 'Escull el prefix de la copia:')

			if copia is None:
				tkMessageBox.showinfo("Information", "Ha cancelado el renombramiento")

			else:
				
				b = b.replace('~', dir_NameDst.get())
				c = b.replace(os.path.basename(b), copia+os.path.basename(b))

				os.rename(b, c)
				for key, value in dicc_fitx_semb.iteritems():
					if b in value:
						dicc_fitx_semb[key].remove(b)

		if copia is not None:
			for elem_tupla in lista_semb.curselection()[::-1]:	
					lista_semb.delete(elem_tupla)
			
#Función crea GUI compara
def compara_graf():
	if not lista_semb.get(0,END):
		tkMessageBox.showwarning("Warning", "No hay ficheros en la lista. Lista vacia!")
	elif lista_semb.curselection() == ():
		tkMessageBox.showinfo("Information", "Selecciona alguno de los ficheros de la lista")
	else:
		ventanacomparacion = Toplevel()
		ventanacomparacion.minsize(500,200)
		ventanacomparacion.maxsize(500,200)

		#Creació de frames per les llistes d'inodes, path i el número de línies diferents
		fcomp = Frame(ventanacomparacion)
		finode = Frame(fcomp)
		fpath = Frame(fcomp)
		fnum = Frame(fcomp)

		#Creació de les labels inode, path i número de línies diferents
		linode = Label(finode, text = 'Inode:')
		lpath = Label(fpath, text = 'Path:')
		lnum = Label(fnum, text ='Num. Lín. Dif')

		#Creació de les scrollbars de les llistes de inodes, path i número de lín. dif. al seu frame 
		scrolInode = Scrollbar(finode, orient = VERTICAL)
		scrolpath = Scrollbar(fpath, orient = VERTICAL)
		scrolnum = Scrollbar(fnum, orient = VERTICAL)

		#Creació de les llistes (inodes, path, núm. lín. dif) al seu frame
		lista_inode = Listbox(finode, yscrollcommand = scrolInode.set)
		lista_path = Listbox(fpath, yscrollcommand = scrolpath.set)
		lista_num = Listbox(fnum, yscrollcommand = scrolnum.set)

		#Configuració de les scrollbars de les llistes
		scrolInode.config(command = lista_inode.yview)
		scrolpath.config(command = lista_path.yview)
		scrolnum.config(command = lista_num.yview)

		#Empaquetament de les estructures de Inode al seu frame
		linode.pack(side = TOP)
		lista_inode.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrolInode.pack(side = LEFT, fill = Y)

		#Empaquetament de les estructures de Path al seu frame
		lpath.pack(side = TOP)
		lista_path.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrolpath.pack(side = LEFT, fill = Y)

		#Empaquetament de les estructures de Núm. Lín. Dif al seu frame
		lnum.pack(side = TOP)
		lista_num.pack(side = LEFT, expand = TRUE, fill = BOTH)
		scrolnum.pack(side = LEFT, fill = Y)

		#Empaquetament dels frames
		finode.pack(side = LEFT, expand = TRUE, fill = BOTH)
		fpath.pack(side = LEFT, expand = TRUE, fill = BOTH)
		fnum.pack(side = LEFT, expand = TRUE, fill = BOTH)
		fcomp.pack(side = LEFT, expand = TRUE, fill = BOTH)

		#Omple les Listbox
		llena_Listas(lista_inode, lista_path, lista_num)

def sortir(window):
	if  tkMessageBox.askquestion('Sortir', "Segur que voleu sortir de l'aplicació?", icon= 'warning') == 'yes':
		window.quit()
		os.system('./destruccio_fitxers.sh')