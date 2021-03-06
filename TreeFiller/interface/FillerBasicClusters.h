//--------------------------------------------------------------------------------------------------
// FillerBasicClusters
//
// Implementation of a filler to fill EDM basic clusters into the mithep::BasicCluster data
// structure.
//
// Authors: C.Paus, J.Bendavid, S.Xie
//--------------------------------------------------------------------------------------------------
#ifndef MITPROD_TREEFILLER_FILLERBASICCLUSTERS_H
#define MITPROD_TREEFILLER_FILLERBASICCLUSTERS_H

#include "MitAna/DataTree/interface/BasicClusterFwd.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"

#include "DataFormats/CaloRecHit/interface/CaloClusterFwd.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"

namespace mithep 
{
  class FillerBasicClusters : public BaseFiller
  {  
    public:
      FillerBasicClusters(const edm::ParameterSet &cfg, edm::ConsumesCollector&, ObjectService*, const char *name, bool active=1);
      ~FillerBasicClusters();

      void                     BookDataBlock(TreeWriter &tws);
      void 	               FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
  
    private:
      edm::EDGetTokenT<reco::CaloClusterCollection> edmToken_;       // edm token for clusters
      edm::EDGetTokenT<EcalRecHitCollection> barrelEcalRecHitToken_; // token for barrel ecal rechits 
      edm::EDGetTokenT<EcalRecHitCollection> endcapEcalRecHitToken_; // token for endcap ecal rechits
      std::string              mitName_;              // mit name of clusters
      std::string              basicClusterMapName_;  // name of export map
      bool                     pfClusters_;           // for alternate shape computations
      mithep::BasicClusterArr *basicClusters_;        // array of basic clusters
      mithep::BasicClusterMap *basicClusterMap_;      // map wrt basic Clusters
  };
}
#endif
