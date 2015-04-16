#include "Reclustering.h"

#include "fastjet/contrib/VariableRPlugin.hh"


Reclustering::Reclustering(double rho_, double min_r_, double max_r_, double ptmin_):
  rho(rho_), min_r(min_r_), max_r(max_r_), ptmin(ptmin_)
{
}

std::vector<TLorentzVector> Reclustering::recluster( 
						    std::vector<TLorentzVector> constituents 
						     ){
  
  std::vector<fastjet::PseudoJet> constit_pseudojets = makePseudoJets(constituents);
  
  fastjet::contrib::VariableRPlugin lvjet_pluginAKT(rho, min_r, max_r, fastjet::contrib::VariableRPlugin::AKTLIKE);
  fastjet::JetDefinition jet_defAKT(&lvjet_pluginAKT);
  fastjet::ClusterSequence clust_seqAKT(constit_pseudojets, jet_defAKT);
  std::vector<fastjet::PseudoJet> inclusive_jetsAKT = clust_seqAKT.inclusive_jets(ptmin);

  return makeTLVs(inclusive_jetsAKT);
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
