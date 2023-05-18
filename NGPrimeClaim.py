#!/bin/python3

'''
Python script for extracting and rebuild NeoGeo rom from Prime Gaming implementation made by Code Mystics.
Orginal bash script by Lionel Cordesses (lioneltrs), Tomasz Bednarz (tomasz_bednarz_pl), Luca Dal Molin
The unswizzle function is a python reimplementation of the original C version made by Ack
source: https://www.arcade-projects.com/threads/samurai-shodown-v-perfect-on-real-hardware.13565/page-2
Name suggestion by RealRelativeEase, based on vcromclaim by Bryan Cain (Plombo)

Luca Dal Molin, 2023
'''

import os
from tempfile import mkdtemp
from shutil import rmtree
from zipfile import ZipFile
from json import load
from sys import argv

v=[("system","s2.bin"),("sound","v1.bin"),("z80","m1.bin"),("68k","p1.bin")]

def unswizzle(file,tmpdir):
    offsets=[(4,0),(4,8),(0,0),(0,8)]
    
    inf=open(file,'rb')
    outodd=open(os.path.join(tmpdir,"odd"),'wb')
    outeven=open(os.path.join(tmpdir,"even"),'wb')
    
    while tile:=inf.read(128):
        for block in range(0,4):    
            for row in range(0,8):
                planes=[0,0,0,0]
                offset=offsets[block][0] + offsets[block][1]*8 + row*8
                
                for i in range(3,-1,-1):
                    data=tile[offset+i]
                    planes[0]=planes[0] << 1;
                    planes[0]=planes[0] | ((data >> 4) & 0x1)
                    planes[0]=planes[0] << 1
                    planes[0]=planes[0] | ((data >> 0) & 0x1)
                    planes[1]=planes[1] << 1
                    planes[1]=planes[1] | ((data >> 5) & 0x1)
                    planes[1]=planes[1] << 1
                    planes[1]=planes[1] | ((data >> 1) & 0x1)
                    planes[2]=planes[2] << 1
                    planes[2]=planes[2] | ((data >> 6) & 0x1)
                    planes[2]=planes[2] << 1
                    planes[2]=planes[2] | ((data >> 2) & 0x1)
                    planes[3]=planes[3] << 1
                    planes[3]=planes[3] | ((data >> 7) & 0x1)
                    planes[3]=planes[3] << 1
                    planes[3]=planes[3] | ((data >> 3) & 0x1)
       
                outodd.write(planes[0].to_bytes(1,byteorder='big',signed=False))
                outodd.write(planes[1].to_bytes(1,byteorder='big',signed=False))
                outeven.write(planes[2].to_bytes(1,byteorder='big',signed=False))
                outeven.write(planes[3].to_bytes(1,byteorder='big',signed=False) )      
    inf.close()
    outodd.close()
    outeven.close()

def main():
    if len(argv)==2:
        if argv[1]=="help":
            print("Script for extracting Neo Geo ROM from Code Mystics implementation.")
            print("Usage:")
            print("\tNGPrimeClaim game srcdir outdir, for extracting the game;")
            print("\tNGPrimeClaim help, print this message;")
            print("\tNGPrimeClaim list, print all the games that are supported.")
        elif argv[1]=="list":
            for f in os.listdir("json"):
                print(os.path.splitext(f)[0])
        else:
            print("Command not recognized! Use NGPrimeClaim help.")
    elif len(argv)==4:
        gamename=argv[1]
        srcdir=argv[2]
        outdir=argv[3]

        if not os.path.exists("json/{}.json".format(gamename)):
            print("Game not yet implemented.")
            exit()

        if not os.path.exists(srcdir):
            print("Source dir does not exist.")
            exit()

        if not os.path.exists(outdir):
            try:
                os.makedirs(outdir,exist_ok=True)
            except:
                print("Error on creating output dir.")
                exit()

        tmppath=mkdtemp()

        f=open("json/{}.json".format(gamename))
        d=load(f)
        f.close()

        game_id=d["id"]

        for typ,ofile in v:
            f=open(os.path.join(srcdir,ofile),mode='rb')
            print("Working on {} files".format(typ))
            for l in d[typ]:
                f.seek(l["start"])
                data=f.read(l["size"])
                g=open(os.path.join(tmppath,game_id+"-"+l["name"]),mode='wb')
                g.write(data)
                g.close()
            f.close()

        print("Start unswizzle...")
        unswizzle(os.path.join(srcdir,"c1.bin"),tmppath)
        print("Finish unswizzle...")

        path=os.path.join(tmppath,"odd")
        f=open(path,mode='rb')
        print("Working on odd sprites")
        for l in d["sprite-odd"]:
            f.seek(l["start"])
            data=f.read(l["size"])
            g=open(os.path.join(tmppath,game_id+"-"+l["name"]),mode='wb')
            g.write(data)
            g.close()
        f.close()
        os.remove(path)

        path=os.path.join(tmppath,"even")
        f=open(path,mode='rb')
        print("Working on even sprites")
        for l in d["sprite-even"]:
            f.seek(l["start"])
            data=f.read(l["size"])
            g=open(os.path.join(tmppath,game_id+"-"+l["name"]),mode='wb')
            g.write(data)
            g.close()
        f.close()
        os.remove(path)

        z=ZipFile(os.path.join(outdir,"{}.zip").format(gamename),'w')
        print("Preparing the zip")
        for f in os.listdir(tmppath):
            z.write(os.path.join(tmppath,f),f)
        z.close()

        rmtree(tmppath)
        print("ROM successfully extracted")
    else:
        print("Error on usage! Use NGPrimeClaim help.")
    
if __name__=="__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
