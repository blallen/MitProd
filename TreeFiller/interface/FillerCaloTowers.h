//--------------------------------------------------------------------------------------------------
// $Id:  $
//
// FillerBasicClusters
//
// Imlementation of a filler to fill EDM CaloTower's into our mithep::CaloTower data structure.
//
// Authors: Si Xie
//--------------------------------------------------------------------------------------------------

#ifndef TREEFILLER_FILLERCALOTOWERS_H
#define TREEFILLER_FILLERCALOTOWERS_H

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"
#include "MitAna/DataTree/interface/Collections.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"

namespace mithep 
{
  class FillerCaloTowers : public BaseFiller
  {  
    public:
      FillerCaloTowers(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerCaloTowers();

      void                         BookDataBlock(TreeWriter &tws);
      void 	                   FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
  
    private:
      std::string                           edmName_;
      std::string                           mitName_;
      mithep::CaloTowerArr                 *caloTowers_;        //array of basic clusters
      
  };
}
#endif