//--------------------------------------------------------------------------------------------------
// $Id: FillerElectrons.h,v 1.19 2009/07/07 08:32:26 bendavid Exp $
//
// FillerElectrons
//
// Implementation of a filler to fill EDM electrons into our mithep::Electron data structure.
//
// Authors: J.Bendavid, S.Xie
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREEFILLER_FILLERELECTRONS_H
#define MITPROD_TREEFILLER_FILLERELECTRONS_H

#include "MitAna/DataTree/interface/ElectronFwd.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"

namespace mithep 
{
  class FillerElectrons : public BaseFiller
  {  
    public:
      FillerElectrons(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerElectrons();

      void                           BookDataBlock(TreeWriter &tws, 
                                                   const edm::EventSetup &es);
      void                           FillDataBlock(const edm::Event &e, 
                                                   const edm::EventSetup &es);
  
    private:
      std::string                    edmName_;                   //edm name of electrons collection
      std::string                    mitName_;                   //mit name of Electrons collection
      std::string                    gsfTrackMapName_;           //name of imported map wrt gsf trks
      std::string                    trackerTrackMapName_;       //name of imported map wrt trk trks
      std::string                    barrelSuperClusterMapName_; //name of imp. map wrt barrel sclus
      std::string                    endcapSuperClusterMapName_; //name of imp. map wrt endcap sclus
      std::string                    pfSuperClusterMapName_;     //name of imp. map wrt pflow sclus
      std::string                    eIDCutBasedTightName_;      //name of tight cut eID algo
      std::string                    eIDCutBasedLooseName_;      //name of loose cut eID algo
      mithep::ElectronArr           *electrons_;                 //array of Electrons
      const mithep::TrackMap        *gsfTrackMap_;               //map wrt gsf tracks
      const mithep::TrackMap        *trackerTrackMap_;           //map wrt tracker tracks
      const mithep::SuperClusterMap *barrelSuperClusterMap_;     //map wrt barrel super clusters
      const mithep::SuperClusterMap *endcapSuperClusterMap_;     //map wrt endcap super clusters
      const mithep::SuperClusterMap *pfSuperClusterMap_;         //map wrt pflow super clusters 
  };
}
#endif
