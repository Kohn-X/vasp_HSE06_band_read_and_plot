import numpy as np

###==============================================================
def kptsread(path,kstart):

	with open(path+'OUTCAR','r') as f:
		lines = f.readlines()

	P0=[i for i,line in enumerate(lines) if 'k-points           NKPTS' in line]
	nkpt = int(lines[P0[-1]].strip().split()[3])

	P1=[i for i,line in enumerate(lines) if 'k-points in units of 2pi/SCALE and weight' in line]
	ckpts=np.zeros((nkpt,3))
	for i in range(nkpt):
		ckpts[i,:]=list(map(float,lines[P1[-1]+1+i].strip().split()[0:3]))

	dist=np.power(np.power(np.diff(ckpts[kstart:,],axis=0),2).sum(axis=1),0.5)   
	xkpts=np.concatenate(([0],dist),axis=0).cumsum()	
	return xkpts

###==============================================================
def eigenread(path,soc): ### read eigenvalues from the EIGENVAL file

	with open(path+'EIGENVAL','r') as f:
		lines = f.readlines()

	enum = int(lines[5].strip().split()[0])       # number of electrons
	nkpt = int(lines[5].strip().split()[1])       # number of KPOINTS
	nbnd = int(lines[5].strip().split()[2])       # number of bands
	
	if soc == 0 or soc == 1:
		band = []; kpt = []
		for i in range(nkpt):
			k_idx = 7 + i*(nbnd+2)
			for j in range(nbnd):
				b_idx = k_idx + j + 1
				band.append(float(lines[b_idx].strip().split()[1]))

		bands = np.array(band).reshape(nkpt,nbnd)
		return bands

	elif soc == -1:
		upband = []; downband = [];kpt = []
		for i in range(nkpt):
			k_idx = 7 + i*(nbnd+2)
			for j in range(nbnd):
				b_idx = k_idx + j + 1
				upband.append(float(lines[b_idx].strip().split()[1]))
				downband.append(float(lines[b_idx].strip().split()[2]))

		upbands = np.array(upband).reshape(nkpt,nbnd)
		downbands = np.array(downband).reshape(nkpt,nbnd)
		return upbands,downbands

###==============================================================
path='./'
soc=0           # 0:nosoc and non-spinolarized; 1:soc; -1:spin-polarized
kstart=16       # start kpoints
eigs=eigenread(path,soc)[kstart:,:]
nelect=8
eigs=eigs-max(eigs[:,int(8/2)])     ### set VBM to zero
print(eigs.shape)
xpts=kptsread(path,kstart)
print(xpts.shape)
bands=np.c_[xpts,eigs]
np.savetxt('./bands.txt',bands)
np.save('./Eband.npy', bands)
