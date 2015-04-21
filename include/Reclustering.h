#ifndef  Reclustering_H
#define  Reclustering_H

#include <vector>
#include "TLorentzVector.h"
#include "fastjet/PseudoJet.hh"

class Reclustering{
 private:

  double radius;
  double rho;
  double min_r;
  double max_r;
  double ptmin;

 public:

  Reclustering(double radius_, double rho_=1., double min_r_=0.4, double max_r_=1.5, double ptmin_=20.);
  std::vector<fastjet::PseudoJet> trim( std::vector<fastjet::PseudoJet> jets );
  std::vector<TLorentzVector> recluster( std::vector<TLorentzVector> constituents );
  std::vector<fastjet::PseudoJet> makePseudoJets( std::vector<TLorentzVector> tlvs );
  std::vector<TLorentzVector> makeTLVs( 
				       std::vector<fastjet::PseudoJet> pseudojets 
					);

};

#endif
