#include "Reclustering.h"

#include "fastjet/contrib/VariableRPlugin.hh"
#include <fastjet/tools/Filter.hh>

Reclustering::Reclustering(double radius_, double rho_, double min_r_, double max_r_, double ptmin_):
  radius(radius_), rho(rho_), min_r(min_r_), max_r(max_r_), ptmin(ptmin_)
{
}
std::vector<TLorentzVector> Reclustering::recluster( 
						    std::vector<TLorentzVector> constituents 
						     ){
  
  std::vector<fastjet::PseudoJet> constit_pseudojets = makePseudoJets(constituents);

  //variable r  
  fastjet::contrib::VariableRPlugin lvjet_pluginAKT(rho, min_r, max_r, fastjet::contrib::VariableRPlugin::AKTLIKE);
  fastjet::JetDefinition jet_def_vr(&lvjet_pluginAKT);

  //fixed r
  fastjet::JetDefinition jet_def_fixr(fastjet::antikt_algorithm, radius);

  fastjet::JetDefinition jet_defAKT;
  if(radius<0.)
    jet_defAKT = jet_def_vr;
  else
    jet_defAKT = jet_def_fixr;

  fastjet::ClusterSequence clust_seqAKT(constit_pseudojets, jet_defAKT);
  std::vector<fastjet::PseudoJet> inclusive_jetsAKT = clust_seqAKT.inclusive_jets(ptmin);

  std::vector<fastjet::PseudoJet> trimmed_jetsAKT = trim(inclusive_jetsAKT);

  return makeTLVs(trimmed_jetsAKT);
}

std::vector<fastjet::PseudoJet> Reclustering::makePseudoJets( std::vector<TLorentzVector> tlvs ){
  
  std::vector<fastjet::PseudoJet> pseudojets; pseudojets.clear();
  for( std::vector<TLorentzVector>::iterator tvit = tlvs.begin(); 
       tvit != tlvs.end(); ++tvit )
    pseudojets.push_back( fastjet::PseudoJet(tvit->Px(), tvit->Py(), 
					     tvit->Pz(), tvit->E()) );

  return pseudojets;
}

std::vector<TLorentzVector> Reclustering::makeTLVs( std::vector<fastjet::PseudoJet> pseudojets ){
  
  std::vector<TLorentzVector> tlvs; tlvs.clear();
  for( std::vector<fastjet::PseudoJet>::iterator pjit = pseudojets.begin(); 
       pjit != pseudojets.end(); ++pjit )
    tlvs.push_back( TLorentzVector(pjit->px(), pjit->py(), pjit->pz(), pjit->E()) );

  return tlvs;
}

std::vector<fastjet::PseudoJet> Reclustering::trim( std::vector<fastjet::PseudoJet> jets){

  std::vector<fastjet::PseudoJet> trimmed_jetsAKT; trimmed_jetsAKT.clear();
  fastjet::Filter trimmer(fastjet::JetDefinition(fastjet::antikt_algorithm, 0.4),
			  fastjet::SelectorPtFractionMin(0.05));
  for( auto jet : jets )
    trimmed_jetsAKT.push_back(trimmer(jet));

  return trimmed_jetsAKT;
}
