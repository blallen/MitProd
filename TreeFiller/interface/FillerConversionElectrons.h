//--------------------------------------------------------------------------------------------------
// $Id: FillerConversionElectrons.h,v 1.4 2008/07/08 12:38:20 loizides Exp $
//
// FillerConversionElectrons
//
// Implementation of a filler creating mithep::Electron objects from the conversion finder tracks.
// This filler differs significantly from the others to deal with the special way in which
// conversions are stored in the edm.
//
// Authors: J.Bendavid
//--------------------------------------------------------------------------------------------------

#ifndef TREEFILLER_FILLERCONVERSIONELECTRONS_H
#define TREEFILLER_FILLERCONVERSIONELECTRONS_H

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "MitAna/DataTree/interface/Collections.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"

namespace mithep 
{
  class FillerConversionElectrons : public BaseFiller
  {  
    public:
      FillerConversionElectrons(const edm::ParameterSet &cfg, bool active=1);
      ~FillerConversionElectrons();

      void                         BookDataBlock(TreeWriter &tws);
      void                         FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
      void                         FillFromTracks(const mithep::TrackCol *tracks, 
                                                  const TrackMap *trackMap);
    private:
      std::string                      mitName_;                //name of Electrons in OAK
      std::string                      convInOutTracksName_;    //name of converted in-out track
      std::string                      convOutInTracksName_;    //name of converted out- track
      std::string                      convInOutTrackMapName_;  //name of imported map wrt in-out
      std::string                      convOutInTrackMapName_;  //name of imported map wrt out-in
      std::string                      convElectronMapName_;    //name of exported map wrt electrons
      const mithep::TrackCol          *convInOutTracks_;        //array of converted in-out tracks
      const mithep::TrackCol          *convOutInTracks_;        //array of converted out-in tracks
      const mithep::TrackMap          *convInOutTrackMap_;      //imported map wrt in-out tracks
      const mithep::TrackMap          *convOutInTrackMap_;      //imported map wrt out-in tracks
      mithep::ElectronArr             *convElectrons_;          //array of conversion electrons
      mithep::ConversionElectronMap   *convElectronMap_;        //exported map wrt electrons
  };
}
#endif