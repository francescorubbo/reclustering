import ROOT as r
from sys import stdout,argv
from numpy import array

lepmulti = 1
samp = 'bckg'

fnamedict = {'signal':'output_signal.root',
             'bckg':'output_bckg.root',
             }

filename = fnamedict[samp]
ff = r.TFile(filename)
tree = ff.Get('outtree')
nentries = tree.GetEntries()

jtypes = ['rcTop','vrTop','ak10']
                                                                         
jmulti = {k:[] for k in jtypes}

def getjetvars(thetree,jtype):
    jmass = []
    jpt = []

    for pt,eta,phi,m in zip(getattr(thetree,jtype+'_jets_pt'),
                            getattr(thetree,jtype+'_jets_eta'),
                            getattr(thetree,jtype+'_jets_phi'),
                            getattr(thetree,jtype+'_jets_m')):
        jmass.append(m)
        jpt.append(pt)
    jmass = array(jmass)
    jpt = array(jpt)
    return jmass[jpt>200]
    
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

#    if (tree.electrons_n+tree.muons_n)!=lepmulti: continue
    for jt in jtypes:
        jmass = getjetvars(tree,jt)
        jmulti[jt].append(len(jmass[(jmass>150.) & (jmass<200.)]))

from numpy import save
for jt in jtypes:
    save('output/'+samp+'_jmulti_'+jt,jmulti[jt])
