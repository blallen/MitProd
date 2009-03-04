//--------------------------------------------------------------------------------------------------
// $Id: TreeService.h,v 1.12 2009/03/03 18:06:09 bendavid Exp $
//
// TreeService 
//
// This service can be used in the config files to provide access to the TreeWriter,
// for example:
//
//   service = TreeService { 
//     untracked vstring treeNames   = { "MitTree" }
//     untracked vstring fileNames   = { "mittreefile" }
//     untracked vstring pathNames   = { "." }
//     untracked vuint32 maxSizes    = { 1024 }
//     untracked vuint32 compLevels  = { 9 }
//     untracked vuint32 splitLevels = { 99 }
//     untracked vuint32 brSizes     = { 32000 }
//   }
//
// Authors: C.Loizides
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREESERVICE_TREESERVICE_H
#define MITPROD_TREESERVICE_TREESERVICE_H

#include "DataFormats/Provenance/interface/EventID.h"
#include "DataFormats/Provenance/interface/Timestamp.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include <TObjArray.h>

namespace edm 
{
  class ActivityRegistry;
  class ParameterSet;
  class ModuleDescription;
}

namespace mithep 
{
  class TreeWriter;

  class TreeService  {
    public:
      TreeService(const edm::ParameterSet &cfg, edm::ActivityRegistry &ar);
      ~TreeService();

      TreeWriter *get(const char *name=0);

    private:
      void preEventProcessing(const edm::EventID &id, const edm::Timestamp &t);
      void postEventProcessing(const edm::Event &e, const edm::EventSetup &es);
      void postBeginJob();
      void postEndJob();

      TObjArray tws_; //array holding the tree writers

      // parameters for service
      std::vector<std::string> treeNames_;    //tree names
      std::vector<std::string> fileNames_;    //file names 
      std::vector<std::string> pathNames_;    //path names
      std::vector<unsigned>    maxSizes_;     //max file sizes [MB]
      std::vector<unsigned>    compLevels_;   //compression levels
      std::vector<unsigned>    splitLevels_;  //default split levels
      std::vector<unsigned>    brSizes_;      //default branch sizes [Byte]
      unsigned                 zipMode_;      //compression mode used by OptIO
      double                   bZipThres_;    //bzip threshold
      double                   gZipThres_;    //gzip threshold
      double                   lzoThres_;     //lzo threshold
      double                   lzmaThres_;    //lzma threshold
      unsigned                 optIOVerbose_; //OptIO verbose 
      bool                     fDoReset_;     //reset object counter (def=1)
  };
}
#endif
