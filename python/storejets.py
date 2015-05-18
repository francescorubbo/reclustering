import ROOT as r
from sys import stdout,argv

lepmulti = 0
samp = 'signal'

fnamedict = {'signal':'output_signal.root',
             'bckg':'output_bckg_1M.root',
             }

filename = fnamedict[samp]
ff = r.TFile(filename)
tree = ff.Get('outtree')
nentries = tree.GetEntries()

jtypes = ['rcTop','vrTop','ak10']
                                                                         
jmasses = {k:[] for k in jtypes}
jpts = {k:[] for k in jtypes}
jistops = {k:[] for k in jtypes}
jtoppts = {k:[] for k in jtypes}

def getjetvars(thetree,jtype):
    jmass = []
    jpt = []
    jistop = []
    jtoppt = []

#    for pt,m,istop,toppt in zip(
    for pt,m in zip(
        getattr(thetree,jtype+'_jets_pt'),
        getattr(thetree,jtype+'_jets_m'),
#        getattr(thetree,jtype+'_jets_isTop'),
#        getattr(thetree,jtype+'_jets_toppt')
        ):
        jmass.append(m)
        jpt.append(pt)
#        jistop.append(istop)
#        jtoppt.append(toppt)
    return jmass,jpt,jistop,jtoppt
    
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    if tree.lep_n!=lepmulti: continue
    for jt in jtypes:
        jmass,jpt,jistop,jtoppt = getjetvars(tree,jt)
        jmasses[jt] += jmass
        jpts[jt] += jpt
        jistops[jt] += jistop
        jtoppts[jt] += jtoppt

from numpy import save
for jt in jtypes:
    save('output/'+samp+'_jmass_'+jt,jmasses[jt])
    save('output/'+samp+'_jpt_'+jt,jpts[jt])
    save('output/'+samp+'_jistop_'+jt,jistops[jt])
    save('output/'+samp+'_jtoppt_'+jt,jtoppts[jt])
