import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

suffixtrue = '_true_jet0.npy'
suffixfake = '_fake_jet0.npy'
var = 'jmass'

jtypes = [
    'rc',
    'vr',
    'ak10'
    ]
jlabels = [
    r'R_{RC}=1.0',
    r'VR($\rho=2\cdot 173.5$ GeV)',
    r'R=1.0']
labeldict = dict(zip(jtypes,jlabels))

from numpy import load,arange

bins = 100
if 'nconst' in var:
    bins=7

ymax = 0.
for jt in jtypes:
    jvar = load('output/bckg_'+var+'_'+jt+suffixtrue)        
    n,b,patches = plt.hist(jvar,bins=bins,normed=True,
                           histtype='step',label=labeldict[jt])
    if max(n)>ymax:
        ymax = max(n)
    
    bins = b
    jvar = load('output/bckg_'+var+'_'+jt+suffixfake)
    n,b,patches = plt.hist(jvar,bins=bins,normed=True,
                           color=patches[0].get_edgecolor(),
                           histtype='step',linestyle='dashed')

    if max(n)>ymax:
        ymax = max(n)

plt.ylim([0,ymax*1.2])
#plt.xlabel('[GeV]')
#plt.ylabel('a.u.')
plt.legend()
plt.savefig('plots/'+var+'.png')
plt.yscale('log')
plt.savefig('plots/'+var+'_log.png')
