#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *
import time
import random

pygame.init()

## czas co jaki odświeża się ekran
FPS = 60
fpsClock = pygame.time.Clock()

### ustawienia okna gry
oknogry = pygame.display.set_mode((1500,800))

pygame.display.set_caption('sprawdź co wiesz')

GRAY = (255, 255, 255)

###### NIE ######
NIE_SZER = 750  # szerokość
NIE_WYS = 250  # wysokość
RED = (255, 0, 0)  # kolor wypełnienia
NIE_POZ = (0, 550)  # pozycja zapisana w tupli
# utworzenie powierzchni NIE, wypełnienie jej kolorem
NIE = pygame.Surface([NIE_SZER, NIE_WYS])
NIE.fill(RED)

###### TAK ######
TAK_SZER = 750 # szerokość
TAK_WYS = 250 # wysokość
GREEN = (154, 205, 50)  # kolor wypełnienia
TAK_POZ = (750, 550)  # pozycja zapisana w tupli
# utworzenie powierzchni TAK, wypełnienie jej kolorem
TAK = pygame.Surface([TAK_SZER, TAK_WYS])
TAK.fill(GREEN)

#### PYTANIA ######

# ustawienie prostokąta zawierającego nie
NIE_prost = NIE.get_rect()
NIE_prost.x = NIE_POZ[0]
NIE_prost.y = NIE_POZ[1]

# ustawienie prostokąta zawierającego TAK
TAK_prost = TAK.get_rect()
TAK_prost.x = TAK_POZ[0]
TAK_prost.y = TAK_POZ[1]

## początkowe ustawienie mrówki i narysowanie jej
mrowka_Img = pygame.image.load('mrowka.jpg')
mrowka_x = 650
mrowka_y = 340
direction = 'left'

## wyświetlanie czasu po prawej stronie ekranu


# komunikaty tekstowe ###################################################


instrukcja = 'Kolor czerwony obrazuje odpowiedź "nie", kolor zielony "tak". Gdy mrówka znajdzie się po odpowiedniej stronie - mrugnij. Powodzenia!'

fontObj = pygame.font.Font('freesansbold.ttf', 22)


lista_pytan =  [ ["pytanie 1" , 0] , ["pytanie 2", 1] , ["pytanie 3", 1] ]

random.shuffle(lista_pytan)

numer_pytania = 0

def drukuj_instrukcja():
    tekst1 = fontObj.render(instrukcja, True, (0, 0, 0))
    tekst_prost1 = tekst1.get_rect()
    tekst_prost1.center = (750, 25)
    oknogry.blit(tekst1, tekst_prost1)

def drukuj_pytania(lista_pytan, numer_pytania):
    pyt = fontObj.render(lista_pytan[numer_pytania][0], True, (0, 0, 0))
    pyt_prost = pyt.get_rect()
    pyt_prost.center = (750, 100)
    oknogry.blit(pyt, pyt_prost)



### pętla główna programu##

while True:
    oknogry.fill(GRAY)


## wyświetlanie instrukcji
    drukuj_instrukcja()

## wyświetlanie pytań
    drukuj_pytania(lista_pytan, numer_pytania)


  ### printowanie dowolnego pytania


## ruch mrówki
    if direction == 'right':
        mrowka_x += 4
        if mrowka_x == 1250:
            mrowka_Img = pygame.transform.flip(mrowka_Img, True, False)
            direction = 'left'

    elif direction == 'left':
        mrowka_x -= 4
        if mrowka_x == 50:
            mrowka_Img = pygame.transform.flip(mrowka_Img, True, False)
            direction = 'right'


    oknogry.blit(mrowka_Img, (mrowka_x, mrowka_y))

# narysuj NIE w oknie gry
    oknogry.blit(NIE, NIE_prost)

# narysuj TAK w oknie gry
    oknogry.blit(TAK, TAK_prost)


## zamykanie okna gry##
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

## aktualizacja czasu i oknagry
    pygame.display.update()
    fpsClock.tick(FPS)
