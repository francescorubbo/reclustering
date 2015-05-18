import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')
import matplotlib.mlab as mlab

dobckg = True

jtypes = [
#    '',
    'rcTop','vrTop','ak10']
jlabels = [
#    'R=0.4',
    r'R_{RC}=1.0','VR(173.5 GeV)','R=1.0']
labeldict = dict(zip(jtypes,jlabels))

from numpy import load,arange

bins = arange(0.,8.,1.)

for jt in jtypes:
    signal_jmulti = load('output/signal_jmulti_'+jt+'.npy')
    if dobckg:
        bckg_jmulti = load('output/bckg_jmulti_'+jt+'.npy')
        
    n,b,patches = plt.hist(signal_jmulti,bins=bins,
                           histtype='step',label=labeldict[jt])

    if dobckg:
        plt.hist(bckg_jmulti,bins=bins,
                 color=patches[0].get_edgecolor(),
                 histtype='step',linestyle='dashed')

plt.xlabel('$N_{j}$')
plt.ylabel('a.u.')
plt.legend()
plt.savefig('plots/jmulti.png')
plt.yscale('log')
plt.savefig('plots/jmulti_log.png')
