#!/bin/python3

'''
Python script for extracting and rebuild NeoGeo rom from Prime Gaming implementation made by Code Mystics.
Orginal bash script by Lionel Cordesses, Tomasz Bednarz, Luca Dal Molin
The unswizzle function is a python reimplementation of the original C version made by Ack
source: https://www.arcade-projects.com/threads/samurai-shodown-v-perfect-on-real-hardware.13565/page-2

Luca Dal Molin, 2023
'''

import os
from tempfile import mkdtemp
from shutil import rmtree

def unswizzle(file,tmpdir):
    offsets=[(4,0),(4,8),(0,0),(0,8)]
    
    inf=open(file,'rb')
    outodd=open(os.path.join(tmpdir,"odd"),'wb')
    outeven=open(os.path.join(tmpdir,"even"),'wb')
    
    while tile:=inf.read(128):
        for block in range(0,4):
            for row in range(0,8):
                planes=[0,0,0,0]
                offset=offsets[block][0] + offsets[block][0]*8 + row*8
                
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
                outodd.write(planes[1]).to_bytes(1,byteorder='big',signed=False))
                outeven.write(planes[2]).to_bytes(1,byteorder='big',signed=False))
                outeven.write(planes[3]).to_bytes(1,byteorder='big',signed=False))
    
    inf.close()
    outodd.close()
    outeven.close()

d=dict()
v=[("system","s2.bin"),("sound","v1.bin"),("z80","m1.bin"),("68k","p1.bin")]

d["kof97"]={
"id": "232",
"system": [(0,131072,"s1.s1")],
"sound": [(0,4194304,"v1.v1"),(4194304,4194304,"v2.v2"),(8388608,4194304,"v2.v2")],
"z80": [(0,131072,"m1.m1")],
"68k": [(0,1048576,"p1.p1"),(1048576,4194304,"p2.sp2")],
"sprite-odd": [(0,8388608,"c1.c1"),(8388608,8388608,"c3.c3"),(16777216,4194304,"c5.c5")],
"sprite-even": [(0,8388608,"c2.c2"),(8388608,8388608,"c4.c4"),(16777216,4194304,"c6.c6")]
}

srcdir="/home/dalmo/Giochi/lutris/amazon/the-king-of-fighters-97-global-match/drive_c/game/Data/rom/"
outdir="/home/dalmo/Documenti/goNCommand-main/"

tmppath=outdir

unswizzle(os.path.join(srcdir,"c1.bin"),tmppath)

'''
tmppath=mkdtemp()

if not os.path.exists(outdir):
    os.makedirs(outdir,exist_ok=True)

for typ,ofile in v:
    f=open(os.path.join(srcdir,ofile),mode='rb')
    vector=d["kof97"][typ]
    for start,size,name in vector:
        f.seek(start)
        data=f.read(size)
        g=open(os.path.join(tmppath,d["kof97"]["id"]+"-"+name),mode='wb')
        g.write(data)
        g.close()
    f.close()

#rmtree(tmppath)
'''
