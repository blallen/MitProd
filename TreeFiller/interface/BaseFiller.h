//--------------------------------------------------------------------------------------------------
// $Id: BaseFiller.h,v 1.6 2008/07/01 14:38:33 loizides Exp $
//
// BaseFiller
//
// Base class to define the interface for a filler.
//
// Authors: C.Paus
//--------------------------------------------------------------------------------------------------

#ifndef TREEFILLER_BASEFILLER_H
#define TREEFILLER_BASEFILLER_H

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"

namespace mithep 
{
  class BaseFiller
  {
    public:
      BaseFiller(const edm::ParameterSet &cfg, const char *name, bool active=true);
      virtual ~BaseFiller() {}

      bool                     Active() const { return active_; }
      virtual void             BookDataBlock(TreeWriter &tws)                                = 0;
      virtual void             FillDataBlock(const edm::Event &e, const edm::EventSetup &es) = 0;
      const std::string       &Name()   const { return name_; }
      virtual void             ResolveLinks(const edm::Event &e, const edm::EventSetup &es)    {}

    protected:
      const edm::ParameterSet &Conf()   const { return config_; }

      const std::string        name_;    //name of this filler
      const edm::ParameterSet  config_;  //parameter set for this filler
      const bool               active_;  //=1 if active
  };
}
#endif
