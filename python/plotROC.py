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

from numpy import load,concatenate,zeros,ones
from sklearn import metrics

for jt in jtypes:
    jvartrue = load('output/bckg_'+var+'_'+jt+suffixtrue)
    jvarfake = load('output/bckg_'+var+'_'+jt+suffixfake)
    y_true = concatenate( ( ones(len(jvartrue)), zeros(len(jvarfake)) ) )
    y_scores = concatenate((jvartrue,jvarfake))

    fpr,tpr,thresholds = metrics.roc_curve(y_true,y_scores)
    plt.plot(tpr,fpr,label=labeldict[jt])

plt.plot([0, 1], [0, 1], 'k--')
plt.legend()
plt.savefig('plots/ROC.png')
