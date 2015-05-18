import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')
import matplotlib.mlab as mlab

dobckg = False
ptcut = 500

jtypes = [
#    '',
    'rcTop','vrTop','ak10']
jlabels = [
#    'R=0.4',
    r'R_{RC}=1.0',r'VR($\rho=2\cdot 173.5$ GeV)',r'R=1.0']
labeldict = dict(zip(jtypes,jlabels))

from numpy import load,arange

bins = arange(0.,350.,5.)

for jt in jtypes:
    signal_jmasses = load('output/signal_jmass_'+jt+'.npy')
    signal_jpts = load('output/signal_jpt_'+jt+'.npy')

    if dobckg:
        bckg_jmasses = load('output/bckg_jmass_'+jt+'.npy')
        bckg_jpts = load('output/bckg_jpt_'+jt+'.npy')
        
    signal_jmasses = signal_jmasses[
        (signal_jpts>ptcut)
        ]
    if dobckg:
        bckg_jmasses = bckg_jmasses[bckg_jpts>ptcut]

    n,b,patches = plt.hist(signal_jmasses,bins=bins,
                           histtype='step',label=labeldict[jt])

    if dobckg:
        plt.hist(bckg_jmasses,bins=bins,
                 color=patches[0].get_edgecolor(),
                 histtype='step',linestyle='dashed')

plt.xlabel('$m_{j}$ [GeV]')
plt.ylabel('a.u.')
plt.legend()
plt.savefig('plots/jmasses_pt%d.png'%ptcut)
plt.yscale('log')
plt.savefig('plots/jmasses_pt%d_log.png'%ptcut)
