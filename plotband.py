import os.path
import numpy as np
from matplotlib import rc
from pylab import *
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import map_coordinates
import matplotlib.pyplot as plt

#define font as serif! this font is good.
rc('font',family='times new roman')
#rc('font',family='serif', serif='times new roman')
rcParams['mathtext.fontset'] = 'stix' #'custom'
#rc('font', serif='times new roman')
# adjust the distance between tick and ticklabels
# set before the figure is created
rcParams['xtick.major.pad'] = 10
rcParams['ytick.major.pad'] = 10

###================================================================================
def PlotEband(ax,path1,low,high,xticknum,xtickname,yticknum,ytickname,ylabel,title):
	
	bands=np.load(path1+'Eband.npy').T
	print(bands.shape)
	print("Plot band from EIGENVAL")

	nbnd,nkpt = bands.shape
	nbnd = nbnd-1
	
	for i in range(nbnd):
		if min(bands[i+1])>high or max(bands[i+1])<low:
			pass
		else:
			ax.plot(bands[0],bands[i+1],color='b',lw=1.5)

	xticknum = bands[0,xticknum]
	ax.set_xticks(xticknum)
	ax.set_xticklabels(xtickname,fontsize='20')
	ax.set_yticks(yticknum)
	ax.set_yticklabels(ytickname,fontsize='20')
	
	ax.set_xlim(bands[0,0],bands[0,-1])
	ax.set_ylim(low,high)
	ax.set_ylabel(ylabel,fontsize='25')
	ax.yaxis.set_label_coords(-0.12,0.5)

	ax.set_title(title,y=1.02,fontsize='25')
	
	for i in xticknum[1:len(xticknum)-1]:
		ax.axvline(i,color='k',ls=':',lw=1)
	
	ax.axhline(0,color='k',ls=':',lw=1)

###=============================================
fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0.20,0.1,0.7,0.8])

path1='./'

low = -6                  # energy interval
high = 6

yticknum = range(-6,7,2)
ytickname = map(str,yticknum)
ylabel = 'E$\minus$E$_\mathrm{F}$ (eV)'

xticknum = [0,20,40,59]
xtickname = ['L','$\Gamma$','X','U']

title='HSE06 band (Si)'

PlotEband(ax,path1,low,high,xticknum,xtickname,yticknum,ytickname,ylabel,title)

#plt.savefig('Eband.pdf',format='pdf')

plt.show()
