//--------------------------------------------------------------------------------------------------
// $Id: FillerPFMet.h,v 1.6 2008/09/16 22:07:16 ksung Exp $
//
// FillerPFMet
//
// Implementation of a filler to fill EDM missing ET objects into our mithep::PFMet data structure.
//
// Authors: C.Loizides
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREEFILLER_FILLERPFMET_H
#define MITPROD_TREEFILLER_FILLERPFMET_H

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"
#include "MitAna/DataTree/interface/Collections.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"

namespace mithep 
{
  class FillerPFMet : public BaseFiller
  {  
    public:
      FillerPFMet(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerPFMet();

      void            BookDataBlock(TreeWriter &tws);
      void            FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
  
    private:
      std::string           edmName_;    //edm name of met collection
      std::string           mitName_;    //name of Mets in OAK
      mithep::PFMetArr     *pfMets_;     //array of Mets
  };
}
#endif
