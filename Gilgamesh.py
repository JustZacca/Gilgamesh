import mysql.connector
import os
import pyfiglet
from termcolor import colored
import colorama
import subprocess as sp
import sys
import hashlib
from progressbar import DataTransferBar
from requests_download import download, HashTracker, ProgressTracker
from pathlib import Path
import os.path
import time
import sqlite3 as lite

conn = None
conn = lite.connect('anidb.db')
mycursor = conn.cursor()

tmp = sp.call('cls',shell=True)

colorama.init()



ascii_banner = pyfiglet.figlet_format("Gilgamesh")
print(ascii_banner)

print ('Anime Downloader v1.2\n\n\n')
menu = 0
print (colored("1- Lista anime \n2- Ricerca per nome \n3- exit\n" , 'green'))
menu = int(input())

keep = True

while keep == True:
    
    if (menu) == 1:
        print("Ora verrá stampata la lista")
        

        mycursor.execute("select distinct anime from episodi where anime not like '%/%'")

        myresult = mycursor.fetchall()

        co = int(0)
        while co < len(myresult):
            print(myresult[co][0])
            co += 1
        
        print (colored("1- Ricerca per nome \n2-exit: ", 'green'))
        men = int(input())
        if (men) == 1:
            menu +=1
            tmp = sp.call('cls',shell=True)
        if (men) == 2:
            menu +=1
    if (menu) == 2:
        tmp = sp.call('cls',shell=True)
        sanime = str(input("Scrivi il titolo dell'anime da cercare: "))
        sanime = (sanime.replace(" ",""))

        

        mycursor.execute("SELECT distinct Anime FROM episodi where Anime like '%"+sanime+"%'")
        
        animelist = mycursor.fetchall()
        if len(animelist) != 0:

            i = int(0)
            c = int(0)
            while i < len(animelist):
            
                print(i,'- ',animelist[i][c])
                i += 1
            print(i,'- Scegli un altro anime')
            chose = int(input("Scegli il risultato: "))
            if chose == i:
                exit()
            title = str(animelist[chose][c])
            
            mycursor.execute("SELECT distinct Anime,server FROM episodi where Anime = '"+title+"'")

            selserver = mycursor.fetchall() 

            a = int(0)
            tmp = sp.call('cls',shell=True)
            print (colored(''+title+'\n' , 'green'))
            while a < len(selserver):
                print(a,'- ',selserver[a][1])
                a += 1 
            
            chose = int(input("\nScegli il server(la scelta é ininfluente): "))
            server = str(selserver[chose][1])

            
            mycursor.execute("SELECT link,N FROM episodi where Anime = '"+title+"' and server ='"+server+"'")

            episodi = mycursor.fetchall() 

            if not os.path.exists(title):
                os.makedirs(title)

            n = str(len(episodi))
            num = int(input("\nScrivi il numero di episodi (se scrivi 0 uscirai dal download) episodi totali "+n+": "))

            i = int(0)
            c = int(0)
            tmp = sp.call('cls',shell=True)
            title = title.replace('/','')
            ascii_banner = pyfiglet.figlet_format(title)
            print(ascii_banner)
            print (colored('\nNumero episodi = '+n , 'green'))
            while i != num:
                
                

                print('\n\n\n')
                link = str(episodi[c][0])
                n = str(episodi[c][1])
                
                file_name = Path(link).name 
                path = title+'/'+file_name
                if(os.path.exists(path)):
                    print('Ep '+file_name+' giá presente')
                    c += 1 
                else:
                    link = link.replace('http:/','http://')
                    link = link.replace('http:///','http://')
                    link = link.replace('https:///','http://')
                    link = link.replace('https:/','http://')
                    

                    hasher = HashTracker(hashlib.sha256())
                    progress = ProgressTracker(DataTransferBar())


                    print('Download di ') 
                    print(colored(file_name,'green'))
                    download(link,path, trackers=(hasher, progress)) 
                    manc = num - i
                    manc = str(manc)
                    print('Download finito con successo!! ne mancano '+manc)    
                      
                    i += 1
                    c += 1

                    if i < num:     
                        print('Si passa al prossimo \n')
                    else:
                        print('Fine!')
            print('\n\n\nIl programma si sta chiudendo, arrivederci')
            time.sleep(10)
            exit()




        else:
            print('Zero risultati')
            print (colored("1- Ricerca per nome \n2-exit: ", 'green'))
        men = int(input())
        if (men) == 1:
            menu +=1
            tmp = sp.call('cls',shell=True)
        if (men) == 2:
            menu +=1

            
    if(menu) == 3:
        
        exit()