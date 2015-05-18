import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

ptcut = 200
suffix = '_fake_jet0.npy'

jtypes = [
    'rc',
    'vr',
    'ak10']
jlabels = [
    r'R_{RC}=1.0',
    r'VR($\rho=2\cdot 173.5$ GeV)',
    r'R=1.0']
labeldict = dict(zip(jtypes,jlabels))

from numpy import load,arange

bins = arange(0.,350.,5.)

for jt in jtypes:
    jmasses = load('output/signal_jmass_'+jt+suffix)
    jpts = load('output/signal_jpt_'+jt+suffix)
    jistoploose = load('output/signal_jistoploose_'+jt+suffix)
    jistopmedium = load('output/signal_jistopmedium_'+jt+suffix)
    
    jmasses = jmasses[(jpts>ptcut)]
    
    n,b,patches = plt.hist(jmasses,bins=bins,
                           histtype='step',label=labeldict[jt])

plt.xlabel('$m_{j}$ [GeV]')
plt.ylabel('a.u.')
plt.legend()
plt.savefig('plots/jmasses_pt%d_fake.png'%ptcut)
plt.yscale('log')
plt.savefig('plots/jmasses_pt%d_fake_log.png'%ptcut)
