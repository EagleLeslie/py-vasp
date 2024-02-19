import numpy as np
import os
from vasp_main import Xdatcar

def xdatcar_slicer(nblocks):
    xdat = Xdatcar()

    # nblocks = 4
    time_intervals = int((xdat.ntimesteps-2000)/nblocks)

    t0 = 2000
    tf = t0 + time_intervals

    t0 = int(t0)
    tf = int(tf)

    # print(f"XDATCAR SLICER")
    # print(f"{xdat.scale}")
    # print(f"{xdat.cell[0,0]:0.6f}    {xdat.cell[1,0]:0.6f}    {xdat.cell[2,0]:0.6f}")
    # print(f"{xdat.cell[0,1]:0.6f}    {xdat.cell[1,1]:0.6f}    {xdat.cell[2,1]:0.6f}")
    # print(f"{xdat.cell[0,2]:0.6f}    {xdat.cell[1,2]:0.6f}    {xdat.cell[2,2]:0.6f}")
    # print(f"   {xdat.atypes[0]}    {xdat.atypes[1]}    {xdat.atypes[2]}")
    # print(f"   {xdat.nelem[0]}    {xdat.nelem[1]}    {xdat.nelem[2]}")

    # for time in range(0, 5):
    #     print(f"Direct configuration=     {time}")
    #     for atom in range(0,xdat.totatoms):
    #         print(f"   {xdat.xyz[time,atom,0]:0.8f}   {xdat.xyz[time,atom,1]:0.8f}   {xdat.xyz[time,atom,2]:0.8f}")

    for blocks in range(nblocks):
        f = open(f"XDATCAR_{blocks}", "w")
        f.write(f"XDATCAR SLICER BLOCKS {t0} - {tf}")
        f.write(f"\n{xdat.scale}")
        f.write(f"\n{xdat.cell[0,0]:0.6f}    {xdat.cell[1,0]:0.6f}    {xdat.cell[2,0]:0.6f}")
        f.write(f"\n{xdat.cell[0,1]:0.6f}    {xdat.cell[1,1]:0.6f}    {xdat.cell[2,1]:0.6f}")
        f.write(f"\n{xdat.cell[0,2]:0.6f}    {xdat.cell[1,2]:0.6f}    {xdat.cell[2,2]:0.6f}")
        f.write(f"\n   {xdat.atypes[0]}    {xdat.atypes[1]}    {xdat.atypes[2]}")
        f.write(f"\n   {xdat.nelem[0]}    {xdat.nelem[1]}    {xdat.nelem[2]}")

        for time in range(t0, tf):
            f.write(f"\nDirect configuration=     {time-t0+1}")
            for atom in range(0,xdat.totatoms):
                f.write(f"\n   {xdat.xyz[time,atom,0]:0.8f}   {xdat.xyz[time,atom,1]:0.8f}   {xdat.xyz[time,atom,2]:0.8f}")

        f.close()
        t0 = t0 + time_intervals
        tf = tf + time_intervals

if __name__ == "__main__":
    nblocks = 4
    xdatcar_slicer(nblocks)

    for blocks in range(nblocks):
        os.system(f"cp XDATCAR_{blocks} XDATCAR")
        os.system(f"./main")
        os.system(f"mv vacfout vacfout_{blocks}")
        os.system(f"mv vacf.txt vacf_{blocks}.txt")

