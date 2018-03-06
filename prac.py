#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from tkFileDialog import *
import tkMessageBox 
import os, sys
from collections import defaultdict
import filecmp

#Create window
window=Tk()
window.title("Cerca fitxers Redundants")
window.minsize(500,300)

#Variables

dir_NameDst = StringVar()
dir_NameSrc = StringVar()
dicc_fitx_ig = defaultdict(list)
dicc_fitx_semb = defaultdict(list)
fit_desti = Listbox()

#Function source
def dirNameSrc():
	dir_NameSrc.set(os.path.abspath(askdirectory()))

#Function dest
def dirNameDst():
	dir_NameDst.set(os.path.abspath(askdirectory()))

#Function 
def omplirDicc(fit_font):
	for path, dirs, files in os.walk(dir_NameDst.get()):
		for f in files:
			#fit_desti.insert(END, f)
			for fi in fit_font:
				if filecmp.cmp(dir_NameSrc.get()+'/'+fi, path+'/'+f, shallow=False) and dir_NameSrc.get()!=path:
					dicc_fitx_ig[f].append(path)
				elif fi == f and dir_NameSrc.get()!=path:
					dicc_fitx_semb[f].append(path)


#Cerca de fitxers semblants
def dicIgual():
	try:
		fit_font = os.listdir(dir_NameSrc.get())
		asd = os.listdir(dir_NameDst.get())
		omplirDicc(fit_font)
		fit_or = filter(lambda fil: fil in dicc_fitx_ig.keys() and fil in dicc_fitx_semb.keys(), fit_font)
		for var in fit_or:
			lista_or.insert(END, var)

		for key, val in dicc_fitx_ig.iteritems():
			lista_ig.insert(END, '~/'+os.path.relpath(val[0], dir_NameSrc.get())+'/'+key)

		for key, val in dicc_fitx_semb.iteritems():
			lista_semb.insert(END, '~/'+os.path.relpath(val[0], dir_NameSrc.get())+'/'+key)

	except IOError, e:
		tkMessageBox.showerror("Error", "Introduzca directorios")
		


def seleccionar_tots(lista):
	for num in range(0, lista.size()):
		print lista.size(), num, lista
		lista.activate(num)

#GUI's First Line: ask origin directory

fDirectFont = Frame(window)
bDirectFont = Button(fDirectFont, text = 'Escolliu directori font', command = dirNameSrc)
lDirectFont = Label(fDirectFont, textvariable = dir_NameSrc, relief = "sunken")

bDirectFont.pack(side = LEFT)
lDirectFont.pack(side = LEFT, expand = TRUE, fill = X)


#GUI's Second Line: ask destination directory and search
fDirectDest = Frame(window)
bDirectDest = Button(fDirectDest, text = 'Escolliu directori destí', command = dirNameDst)
lDirectDest = Label(fDirectDest, textvariable = dir_NameDst, relief = "sunken")
bCerca = Button(fDirectDest, text = 'Cerca', command = dicIgual)

bDirectDest.pack(side = LEFT)
lDirectDest.pack(side = LEFT, expand = TRUE, fill = X)
bCerca.pack(side = LEFT)

#GUI's last line: exit button
fSortir = Frame(window)
bSortir = Button(fSortir, text = 'Sortir', command = window.quit)

bSortir.pack(side = LEFT)


#Frame for GUI's scrollboxes
fFitxers = Frame(window)

#GUI's frame for Originals scrollbox
fOriginals = Frame(fFitxers)
lOriginals = Label(fOriginals, text = 'Fitxers Originals:')
scrolOriginal = Scrollbar(fOriginals, orient = VERTICAL)
lista_or = Listbox(fOriginals, yscrollcommand = scrolOriginal.set)
scrolOriginal.config(command = lista_or.yview)


#GUI's second-to-last: selecciona tots/cap
fSelecciona = Frame(window)
bTots = Button(fSelecciona, text = 'Selecciona Tots', command = seleccionar_tots(lista_or))
bCap = Button(fSelecciona, text = 'Selecciona Cap', command = window.quit)

bTots.pack(side = LEFT)
bCap.pack(side = LEFT)



lOriginals.pack(side = TOP, anchor = W)
scrolOriginal.pack(side = RIGHT, fill = Y)
lista_or.pack(side = LEFT, expand = TRUE, fill = BOTH)


#GUI's frame for Iguals i Semblants
fIgualSembl = Frame(fFitxers)

#GUI's frame for Iguals
fIguals = Frame(fIgualSembl)
lIguals = Label(fIguals, text = '    Fitxers Iguals:')

lIguals.pack(side = TOP, anchor = W)

#Iguals' Scrollbox
fIgualScroll = Frame(fIguals)
scrollIguals = Scrollbar(fIgualScroll, orient = VERTICAL)
lista_ig = Listbox(fIgualScroll, yscrollcommand = scrollIguals.set)
scrollIguals.config(command = lista_ig.yview)

scrollIguals.pack(side = LEFT, fill = Y)
lista_ig.pack(side = RIGHT, expand = TRUE, fill = X)

#Iguals' Buttons
fFitxIgualButton = Frame(fIguals)
bEsborra = Button(fFitxIgualButton, text = 'Esborra', command = window.quit)
bHLink = Button(fFitxIgualButton, text = 'Hard Link', command = window.quit)
bSLink = Button(fFitxIgualButton, text = 'Soft Link', command = window.quit)
bSelecTotsA = Button(fFitxIgualButton, text = 'Selec Tots', command = window.quit)
bSelecCapA = Button(fFitxIgualButton, text = 'Selec Cap', command = window.quit)

bEsborra.pack(side = TOP, anchor = W)				
bHLink.pack(side = TOP, anchor = W)				
bSLink.pack(side = TOP, anchor = W)				
bSelecTotsA.pack(side = TOP, anchor = W)				
bSelecCapA.pack(side = TOP, anchor = W)
fIgualScroll.pack(side = LEFT)
fFitxIgualButton.pack(side = LEFT)
fIguals.pack(side = TOP, expand = TRUE, fill = X)

#GUI's frame for Semblants
fSembl = Frame(fIgualSembl)
lSembl = Label(fSembl, text = '    Fitxers Semblants')

lSembl.pack(side = TOP, anchor = W)

#Semblants' ScrollBox
fSemblScroll = Frame(fSembl)
scrollSembl = Scrollbar(fSemblScroll, orient = VERTICAL)
lista_semb = Listbox(fSemblScroll, yscrollcommand = scrollSembl.set)
scrollSembl.config(command = lista_semb.yview)

scrollSembl.pack(side = LEFT, fill = Y)
lista_semb.pack(side = RIGHT, expand = TRUE, fill = X)
			
#GUI's buttons for 'Fitxers Semblants'
fFitxSemblButton = Frame(fSembl)
bCompara = Button(fFitxSemblButton, text = 'Compara', command = window.quit)
bRenombra = Button(fFitxSemblButton, text = 'Renombra', command = window.quit)
bEsborra = Button(fFitxSemblButton, text = 'Esborra', command = window.quit)
bSelecTotsB = Button(fFitxSemblButton, text = 'Selec Tots', command = window.quit)
bSelecCapB = Button(fFitxSemblButton, text = 'Selec Cap', command = window.quit)

bCompara.pack(side = TOP, anchor = W)
bRenombra.pack(side = TOP, anchor = W)
bEsborra.pack(side = TOP, anchor = W)
bSelecTotsB.pack(side = TOP, anchor = W)
bSelecCapB.pack(side = TOP, anchor = W)

fSemblScroll.pack(side = LEFT)
fFitxSemblButton.pack(side = LEFT)
fSembl.pack(side = TOP, expand = TRUE, fill = X)

#Pack frames
fDirectFont.pack(side = TOP, expand = TRUE, fill = X)
fDirectDest.pack(side = TOP, expand = TRUE, fill = X)
fSortir.pack(side = BOTTOM, expand = TRUE, fill = X)
fSelecciona.pack(side = BOTTOM, expand = TRUE, fill = X)
fOriginals.pack(side = LEFT, expand = TRUE, fill = BOTH)
fIgualSembl.pack(side = LEFT, expand = TRUE, fill = X)
fFitxers.pack(side = LEFT, expand = TRUE, fill = X)

window.mainloop()
