import ROOT as r
from sys import stdout,argv
from math import fabs,hypot

lepmulti = 0
samp = 'signal'
whichjet = 0
topmatch = True if int(argv[1])==1 else False

fnamedict = {'signal':'data/mc14_13TeV.204534.Herwigpp_UEEE4_CTEQ6L1_Gtt_G1300_T5000_L100.root',
             'bckg':'data/mc14_13TeV.110401.PowhegPythia_P2012_ttbar_nonallhad.root',
             }

filename = fnamedict[samp]
ff = r.TFile(filename)
tree = ff.Get('tree')
nentries = tree.GetEntries()

jtypes = ['rc','vr','ak10']
                                                                         
jmasses = {k:[] for k in jtypes}
jpts = {k:[] for k in jtypes}
jsplit12 = {k:[] for k in jtypes}
jsplit23 = {k:[] for k in jtypes}
jtau21 = {k:[] for k in jtypes}
jtau32 = {k:[] for k in jtypes}
jnconst = {k:[] for k in jtypes}

def matching(thetree,jeta,jphi):
    match = 2
    for pid,pt,eta,phi in zip(
        thetree.mc_pdgId,
        thetree.mc_pt,
        thetree.mc_eta,
        thetree.mc_phi
        ):
        if fabs(pid)!=6: continue
        if pt<350: continue
        dist = hypot(jeta-eta,jphi-phi)
        if dist<0.75: 
            match = 1
            break
        if dist < 1.5:
            match = 0
    return match
    
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    if (tree.electrons_n+tree.muons_n)!=lepmulti: continue
    for jt in jtypes:
        njets = getattr(tree,jt+'_jets_n')
        if njets<whichjet+1: continue
        jpt = getattr(tree,jt+'_jets_pt')[whichjet]
#        if jpt<300: continue
        jeta = getattr(tree,jt+'_jets_eta')[whichjet]
        jphi = getattr(tree,jt+'_jets_phi')[whichjet]
        match = matching(tree,jeta,jphi)
        if topmatch:
            if match!=1: continue
        else:
            if match!=2: continue
        
        jmasses[jt].append(getattr(tree,jt+'_jets_m')[whichjet])
        jpts[jt].append(jpt)
        jsplit12[jt].append(getattr(tree,jt+'_jets_SPLIT12')[whichjet]) 
        jsplit23[jt].append(getattr(tree,jt+'_jets_SPLIT23')[whichjet]) 
        jtau21[jt].append(getattr(tree,jt+'_jets_tau21')[whichjet]) 
        jtau32[jt].append(getattr(tree,jt+'_jets_tau32')[whichjet])
        if 'ak10' not in jt:
            jnconst[jt].append(getattr(tree,jt+'_jets_nconst')[whichjet])

matched = '_true' if topmatch else '_fake'
suffix = matched + '_jet%d'%whichjet
from numpy import save
for jt in jtypes:
    save('output/'+samp+'_jmass_'+jt+suffix,jmasses[jt])
    save('output/'+samp+'_jpt_'+jt+suffix,jpts[jt])
    save('output/'+samp+'_jsplit12_'+jt+suffix,jsplit12[jt])
    save('output/'+samp+'_jsplit23_'+jt+suffix,jsplit23[jt])
    save('output/'+samp+'_jtau21_'+jt+suffix,jtau21[jt])
    save('output/'+samp+'_jtau32_'+jt+suffix,jtau32[jt])
    save('output/'+samp+'_jnconst_'+jt+suffix,jnconst[jt])
