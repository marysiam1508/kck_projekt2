# -*- coding: utf-8 -*-

import multiprocessing as mp
import pygame as pygame
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pygame.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################



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
    instrukcja1 = 'Naciśnij tak by zacząć grę'
    pytanie1 = 'Królowa mrówek może przeżyć do 25 lat'
    ###Domyślnie odp tak
    pytanie2 = 'Mrówka pokazywana 50 ms pozostanie w pamięci ikonicznej dłużej niż mrówka eksponowana 100 ms'
    ###Odpowiedź tak
    pytanie3 = 'Istnieje około 1000 gatunków mrówek'
    ###Odpowiedź nie
    pytanie4 = 'Mrówka należy do rodziny pajęczaków'
    ###Odpowiedź nie
    pytanie5 = 'Zdanie: jeżeli mrówka jest owadem, to Ziemia jest płaska jest prawdziwe'
    ###Odpowiedź nie

    font = pygame.font.Font('freesansbold.ttf', 22)



    numer_pytania = 0

    def drukuj_instrukcja():
        tekst1 = font.render(instrukcja, True, (0, 0, 0))

        tekst_prost1 = tekst1.get_rect()
        tekst_prost1.center = (750, 25)
        oknogry.blit(tekst1, tekst_prost1)

    ### pętla główna programu##
    turn= 0
    pkt=0
    while True:
        oknogry.fill(GRAY)
    ## wyświetlanie instrukcji
        drukuj_instrukcja()



    ## ruch mrówki
    ###Odpwiedź nie === murwka_x <750
    ###Odpowiedźnie === mruwka_x>750


    #
    ####
        if blink.value == 1:
            print('BLINK!')
            past_dir = direction
            direction = 'null'
            blink.value = 0



        if turn == 0:
            pyt= font.render('Naciśnij tak by zacząć grę', True, (0, 0, 0))
            oknogry.blit(pyt,(650,100))
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
            elif direction == 'null':
                if mrowka_x<750 :

                    direction = past_dir  ### Przykład
                    turn+=1


                elif mrowka_x>750:

                    direction = past_dir
                    turn+=1
                    bli




        if turn==1:

            pyt= font.render(pytanie1, True, (0, 0, 0))
            oknogry.blit(pyt,(550,100))
            score =font.render('Punkty:'+str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100)) ### Manipuluj X i Y aby ustawić napis
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
            elif direction == 'null':
                if mrowka_x<750:
                    pkt+=0
                    turn+=1
                    direction = past_dir


                elif mrowka_x>750:
                    pkt+=1
                    turn+=1
                    direction = past_dir


        if turn ==2:

            pyt= font.render(pytanie2, True, (0, 0, 0))
            oknogry.blit(pyt,(350,100))
            score =font.render('Punkty:'+str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100)) ### Manipuluj X i Y aby ustawić napis
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
            elif direction == 'null':
                if mrowka_x<750:# and ruch == True:
                    pkt+=0
                    turn+=1
                    direction = past_dir

                if mrowka_x>750:# and ruch == True:
                    pkt+=1
                    turn+=1
                    direction = past_dir

        if turn == 3:

            pyt= font.render(pytanie3, True, (0, 0, 0))
            oknogry.blit(pyt,(550,100))
            score =font.render('Punkty:'+str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100)) ### Manipuluj X i Y aby ustawić napis
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
            elif direction == 'null':
                if mrowka_x<750 :#and ruch == True:
                    pkt+=1
                    turn+=1

                    direction = past_dir

                if mrowka_x>750:# and ruch == True:
                    pkt+=0
                    turn+=1
                    direction = past_dir

        if turn == 4:

            pyt= font.render(pytanie4, True, (0, 0, 0))
            oknogry.blit(pyt,(550,100))
            score =font.render('Punkty:'+str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100)) ### Manipuluj X i Y aby ustawić napis
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
            elif direction == 'null':
                if mrowka_x<750:# and ruch == True:
                    pkt+=1
                    turn+=1

                    direction = past_dir

                if mrowka_x>750:# and ruch == True:
                    pkt+=1
                    turn+=1
                    direction = past_dir

        if turn ==5:

            pyt= font.render(pytanie5, True, (0, 0, 0))
            oknogry.blit(pyt,(420,100))
            score =font.render('Punkty:'+str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100)) ### Manipuluj X i Y aby ustawić napis
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
            elif direction == 'null':
                if mrowka_x<750:# and ruch == True:
                    pkt+=1
                    turn+=1

                if mrowka_x>750:# and ruch == True:
                    pkt+=0
                    turn+=1

        if turn ==6:
            score = font.render ('Punkty:' +str(pkt),True,(0,0,0))
            oknogry.blit(score,(100,100))











    #########################
    #                       #
    #                       #
    #########################
        oknogry.blit(mrowka_Img, (mrowka_x, mrowka_y))
        # narysuj NIE w oknie gry
        oknogry.blit(NIE, NIE_prost)
        # narysuj TAK w oknie gry
        oknogry.blit(TAK, TAK_prost)
            #####TUTAJ JEST MIEJSCE W KTÓRYM WYŚWIETLA SIĘ PYTANIE
        pygame.display.flip()

    ## zamykanie okna gry##
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_program.set()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    past_dir = direction

                    time.sleep(2)

    ## aktualizacja czasu i oknagry
        pygame.display.update()
        fpsClock.tick(FPS)
