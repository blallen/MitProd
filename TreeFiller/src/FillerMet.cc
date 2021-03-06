#include "MitProd/TreeFiller/interface/FillerMet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "MitAna/DataTree/interface/Names.h"
#include "MitAna/DataTree/interface/MetCol.h"
#include "MitProd/ObjectService/interface/ObjectService.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerMet::FillerMet(const ParameterSet &cfg, edm::ConsumesCollector& collector, ObjectService* os, const char *name, bool active) : 
  BaseFiller(cfg,os,name,active),
  edmToken_(GetToken<reco::METCollection>(collector, cfg, "edmName")), //met
  mitName_(cfg.getUntrackedParameter<string>("mitName",Names::gkCaloMetBrn)),
  mets_(new mithep::MetArr)
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerMet::~FillerMet()
{
  // Destructor.

  delete mets_;
}

//--------------------------------------------------------------------------------------------------
void FillerMet::BookDataBlock(TreeWriter &tws)
{
  // Add mets branch to tree.

  tws.AddBranch(mitName_,&mets_);
  OS()->add<mithep::MetArr>(mets_,mitName_);
}

//--------------------------------------------------------------------------------------------------
void FillerMet::FillDataBlock(const edm::Event      &event, 
                              const edm::EventSetup &setup)
{
  // Fill missing energy from edm collection into our collection.

  mets_->Delete();

  Handle<reco::METCollection> hMetProduct;
  GetProduct(edmToken_, hMetProduct, event);

  reco::METCollection const& inMets = *hMetProduct;

  // loop through all mets
  for (reco::METCollection::const_iterator inMet = inMets.begin(); 
       inMet != inMets.end(); ++inMet) {
    
    mithep::Met *met = mets_->Allocate();
    new (met) mithep::Met(inMet->px(), inMet->py());
    
    // fill met base class data 
    met->SetSumEt(inMet->sumEt());
    met->SetElongitudinal(inMet->e_longitudinal());
    for(unsigned i=0; i<inMet->mEtCorr().size(); i++) {
      met->PushCorrectionX(inMet->mEtCorr()[i].mex);
      met->PushCorrectionY(inMet->mEtCorr()[i].mey);
      met->PushCorrectionSumEt(inMet->mEtCorr()[i].sumet);
    }

  }
  mets_->Trim();
}

DEFINE_MITHEP_TREEFILLER(FillerMet);
