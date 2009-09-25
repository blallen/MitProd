//--------------------------------------------------------------------------------------------------
// $Id: FillerConversions.h,v 1.12 2009/07/20 03:19:24 loizides Exp $
//
// FillerConversions
//
// Implementation of a filler creating mithep::Conversion objects from the reconstructed
// conversion electrons.
//
// Authors: J.Bendavid
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREEFILLER_FILLERCONVERSIONS_H
#define MITPROD_TREEFILLER_FILLERCONVERSIONS_H

#include "MitAna/DataTree/interface/ConversionFwd.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"

namespace mithep 
{
  class FillerConversions : public BaseFiller
  {  
    public:
      FillerConversions(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerConversions();

      void                                     BookDataBlock(TreeWriter &tws, 
                                                             const edm::EventSetup &es);
      void                                     FillDataBlock(const edm::Event &e, 
                                                             const edm::EventSetup &es);
  
    private:
      mithep::Particle                        *GetMitParticle(edm::Ptr<reco::Track> ptr) const;
    
      std::string                              edmName_;             //name of edm conversions
      std::string                              mitName_;             //mit name of Conversions
      std::string                              convElectronMapName_; //name of imported electrons map
      std::vector<std::string>                 stablePartMapNames_;  //name imp maps wrt stable parts
      std::string                              conversionMapName_;   //name of exported conv map
      std::vector<const mithep::TrackPartMap*> stablePartMaps_;      //maps wrt stable parts
      mithep::ConversionArr                   *conversions_;         //array of Conversions
      mithep::ConversionMap                   *conversionMap_;       //exported map wrt Conversions
  };
}
#endif
