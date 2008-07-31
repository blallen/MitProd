//--------------------------------------------------------------------------------------------------
// $Id: FillerConversions.h,v 1.4 2008/07/08 12:38:20 loizides Exp $
//
// FillerConversions
//
// Implementation of a filler creating mithep::Conversion objects from the reconstructed
// conversion electrons.
//
// Authors: J.Bendavid
//--------------------------------------------------------------------------------------------------

#ifndef TREEFILLER_FILLERCONVERSIONS_H
#define TREEFILLER_FILLERCONVERSIONS_H

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "MitAna/DataTree/interface/Collections.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"

namespace mithep 
{
  class FillerConversions : public BaseFiller
  {  
    public:
      FillerConversions(const edm::ParameterSet &cfg, bool active=1);
      ~FillerConversions();

      void                 BookDataBlock(TreeWriter &tws);
      void                 FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
  
    private:
      std::string                            edmName_;             //name of edm conversions
      std::string                            mitName_;             //name of Conversions in OAK
      std::string                            convElectronMapName_; //name of imported electrons map
      std::string                            conversionMapName_;   //name of exported conv map
      const mithep::ConversionElectronMap   *convElectronMap_;     //imported map wrt conv electrons
      mithep::ConversionArr                 *conversions_;         //array of Conversions
      mithep::ConversionMap                 *conversionMap_;       //exported map wrt Conversions
  };
}
#endif