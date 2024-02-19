import numpy as np
import matplotlib.pyplot as plt
import os
import re

def parse():

    if os.path.isdir('./pydata'):

        print(f"pydata directory exists")

        os.chdir('./pydata/')

        ens_data = [line for line in open('./energy.txt') if line.strip()] # internal energy without entropy
        ens = np.array([float(num) for line in ens_data for num in re.findall(r'-?\d+\.?\d*', line)])
        ens = ens.ravel().reshape(-1,3)

        free_data = [line for line in open('./free.txt') if line.strip()] # internal energy
        # free = np.array([line.split() for line in free_data[1:] if isfloat(line.split()[0])],dtype=float)
        free = np.array([float(num) for line in free_data for num in re.findall(r'-?\d+\.?\d*', line)])
        free = free.ravel().reshape(-1,1)

        etot = np.loadtxt(fname = './etot.txt')
        mdpress = np.loadtxt(fname = './press.txt')
        temp = np.loadtxt(fname = './temp.txt')

        time, err = np.loadtxt(fname = './ERR.dat',unpack=True)
        time2, beef = np.loadtxt(fname = './BEEF.dat',unpack=True)
        time3, ctifor = np.loadtxt(fname = './CTIFOR.dat',unpack=True)
    
    else:

        print(f"pydata directory does not exist")

        os.system("mkdir pydata")

        os.system("grep 'energy  without' OUTCAR > ./pydata/energy.txt")
        os.system("grep 'free  energy' OUTCAR > ./pydata/free.txt")
        os.system("grep 'ETOT' OUTCAR | awk '{print $5}' > ./pydata/etot.txt")
        os.system("grep 'Total+kin' OUTCAR | awk '{print ($2+$3+$3)/3.}' > ./pydata/press.txt")
        os.system("grep '(temperature' OUTCAR | cut -c 57-64 | awk '{print $1}' > ./pydata/temp.txt")

        # ML ERROR COMMANDS
        os.system("grep ERR ML_LOGFILE|grep -v '#'|awk '{print $2, $4}' > ./pydata/ERR.dat")
        os.system("grep BEEF ML_LOGFILE|grep -v '#'|awk '{print $2, $4}' > ./pydata/BEEF.dat")
        os.system("grep BEEF ML_LOGFILE|grep -v '#'|awk '{print $2, $6}' > ./pydata/CTIFOR.dat")

        os.chdir('./pydata/')

        ens_data = [line for line in open('./energy.txt') if line.strip()] # internal energy without entropy
        ens = np.array([float(num) for line in ens_data for num in re.findall(r'-?\d+\.?\d*', line)])
        ens = ens.ravel().reshape(-1,3)

        free_data = [line for line in open('./free.txt') if line.strip()] # internal energy
        # free = np.array([line.split() for line in free_data[1:] if isfloat(line.split()[0])],dtype=float)
        free = np.array([float(num) for line in free_data for num in re.findall(r'-?\d+\.?\d*', line)])
        free = free.ravel().reshape(-1,1)

        etot = np.loadtxt(fname = './etot.txt')
        mdpress = np.loadtxt(fname = './press.txt')
        temp = np.loadtxt(fname = './temp.txt')

        time, err = np.loadtxt(fname = './ERR.dat',unpack=True)
        time2, beef = np.loadtxt(fname = './BEEF.dat',unpack=True)
        time3, ctifor = np.loadtxt(fname = './CTIFOR.dat',unpack=True)

    return ens[:,0], free[:,0], etot, mdpress, temp, time, err, time2, beef, time3, ctifor

if __name__ == "__main__":
        
    ens, free, etot, mdpress, temp, time, err, time2, beef, time3, ctifor = parse()

    fig, axs = plt.subplots(2,2)
    axs[0,0].plot(etot,color='dodgerblue')
    axs[0,0].set_ylabel('ETOT (eV)')
    axs[0,0].set_xlabel('Timesteps (fs)')

    axs[1,0].plot(ens,color='dodgerblue')
    axs[1,0].set_ylabel('Energy (eV)')
    axs[1,0].set_xlabel('Timesteps (fs)')

    axs[0,1].plot(mdpress,color='dodgerblue')
    axs[0,1].set_ylabel('Pressure (GPa)')
    axs[0,1].set_xlabel('Timesteps (fs)')

    axs[1,1].plot(temp,color='dodgerblue')
    axs[1,1].set_xlabel('Timesteps (fs)')
    axs[1,1].set_ylabel('Temperature (K)')

    axs[0][0].grid(True)
    axs[0][1].grid(True)
    axs[1][0].grid(True)
    axs[1][1].grid(True)

    fig.tight_layout()

    plt.savefig('./plots.png',dpi=400,format='png')
    plt.show()

    plt.plot(time, err, color='dodgerblue', zorder=4, label='ERR')
    plt.plot(time2, beef, color='darkgray', zorder=0, label='BEEF')
    plt.plot(time3, ctifor, color='darkred', zorder=2, label='CTIFOR')

    plt.xlabel('Molecular Dynamics Step', size=13)
    plt.ylabel('Error in Force (eV/$\AA$)', size=13)
    plt.legend()
    plt.savefig('./MLerr.png',dpi=400,format='png')
    plt.show()
