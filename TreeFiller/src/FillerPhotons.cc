// $Id: FillerPhotons.cc,v 1.2 2008/07/03 07:56:14 loizides Exp $

#include "MitProd/TreeFiller/interface/FillerPhotons.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/ConversionFwd.h"
#include "MitAna/DataTree/interface/Names.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerPhotons::FillerPhotons(const edm::ParameterSet &cfg, bool active, 
                             const ConversionMap *conversionMap) : 
  BaseFiller(cfg, "Photons", active),
  edmName_(Conf().getUntrackedParameter<string>("edmName","photons")),
  mitName_(Conf().getUntrackedParameter<string>("mitName",Names::gkPhotonBrn)),
  photons_(new mithep::Array<mithep::Photon>), 
  conversionMap_(conversionMap)
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerPhotons::~FillerPhotons()
{
  // Destructor.

  delete photons_;
}

//--------------------------------------------------------------------------------------------------
void FillerPhotons::BookDataBlock(TreeWriter &tws)
{
  // Add photon branch to tree.

  tws.AddBranch(mitName_.c_str(),&photons_);
}

//--------------------------------------------------------------------------------------------------
void FillerPhotons::FillDataBlock(const edm::Event      &event, 
                                      const edm::EventSetup &setup)
{
  // Fill photon array.

  photons_->Reset();
  
  try {
    event.getByLabel(edm::InputTag(edmName_),photonProduct_);
  } catch (cms::Exception &ex) {
    edm::LogError("FillerPhotons") << "Error! Cannot get collection with label " 
                                   << edmName_ << endl;
    throw edm::Exception(edm::errors::Configuration, "FillerPhotons:FillDataBlock()\n")
      << "Error! Cannot get collection with label " << edmName_ << endl;
  }
  
  const reco::PhotonCollection inPhotons = *(photonProduct_.product());  
  
  for (reco::PhotonCollection::const_iterator iP = inPhotons.begin(); 
       iP != inPhotons.end(); ++iP) {

    mithep::Photon* outPhoton = photons_->Allocate();
    new (outPhoton) mithep::Photon(iP->px(),iP->py(),iP->pz(),iP->energy());
    if (iP->isConverted() && conversionMap_) {
      std::vector<reco::ConversionRef> conversionRefs = iP->conversions();
      for (std::vector<reco::ConversionRef>::const_iterator conversionRef = 
             conversionRefs.begin(); conversionRef != conversionRefs.end(); ++conversionRef) {
        outPhoton->AddConversion(conversionMap_->GetMit(*conversionRef));
      }
    }
  }

  photons_->Trim();
}
