#include "Reclustering.h"

int main(){

  Reclustering rec = Reclustering();

  std::vector<TLorentzVector> constituents;
  constituents.push_back(TLorentzVector(99.0,  0.1,  0, 100.0));
  constituents.push_back(TLorentzVector(25.0,  -0.1,  0, 26.0));
  constituents.push_back(TLorentzVector(-99.0,  0,  0, 99.0));

  std::vector<TLorentzVector> jets = rec.recluster(constituents);  
  
  for(auto jet : jets)
    jet.Print();

  return 0;
}
