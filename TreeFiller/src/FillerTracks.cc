// $Id: FillerTracks.cc,v 1.21 2008/10/13 10:41:36 bendavid Exp $

#include "MitProd/TreeFiller/interface/FillerTracks.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticleFwd.h"
#include "DataFormats/RecoCandidate/interface/TrackAssociation.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerTracks::FillerTracks(const ParameterSet &cfg, const char *name, bool active,
                           const char *edmName, const char *mitName) :
  BaseFiller(cfg,name,active),
  edmName_(Conf().getUntrackedParameter<string>("edmName",edmName)),
  mitName_(Conf().getUntrackedParameter<string>("mitName",mitName)),
  edmSimAssocName_(Conf().getUntrackedParameter<string>("edmSimAssociationName","")),
  trackingMapName_(Conf().getUntrackedParameter<string>("trackingMapName","TrackingMap")),
  trackMapName_(Conf().getUntrackedParameter<string>("trackMapName",
                                                     Form("%sMapName",mitName_.c_str()))),
  trackingMap_(0),
  tracks_(new mithep::TrackArr(250)), 
  trackMap_(new mithep::TrackMap)
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerTracks::~FillerTracks()
{
  // Destructor.

  delete tracks_;
  delete trackMap_;
}

//--------------------------------------------------------------------------------------------------
void FillerTracks::BookDataBlock(TreeWriter &tws)
{
  // Add tracks branch to tree, publish and get our objects.

  tws.AddBranch(mitName_.c_str(),&tracks_);

  trackingMap_ = OS()->get<TrackingParticleMap>(trackingMapName_.c_str());
  OS()->add<TrackMap>(trackMap_,trackMapName_.c_str());
  OS()->add<TrackArr>(tracks_,mitName_.c_str());
}

//--------------------------------------------------------------------------------------------------
void FillerTracks::FillDataBlock(const edm::Event      &event, 
                                 const edm::EventSetup &setup)
{
  // Fill tracks from edm collection into our collection.

  tracks_  ->Reset();
  trackMap_->Reset();

  Handle<reco::TrackCollection> hTrackProduct;
  GetProduct(edmName_, hTrackProduct, event);  
	
  trackMap_->SetEdmProductId(hTrackProduct.id().id());
  const reco::TrackCollection inTracks = *(hTrackProduct.product());  
  
  // for MC SimParticle association (reco->sim mappings)
  reco::RecoToSimCollection simAssociation;
  if (trackingMap_ && !edmSimAssocName_.empty()) {
    Handle<reco::RecoToSimCollection> simAssociationProduct;
    GetProduct(edmSimAssocName_, simAssociationProduct, event);  
    simAssociation = *(simAssociationProduct.product());
    //printf("SimAssociation Map Size = %i\n",simAssociation.size());
  }
  
  // loop through all tracks and fill the information
  for (reco::TrackCollection::const_iterator it = inTracks.begin(); 
       it != inTracks.end(); ++it) {
    mithep::Track *outTrack = tracks_->Allocate();
    // create track and set the core parameters
    new (outTrack) mithep::Track(it->qoverp(),it->lambda(),
                                 it->phi(),it->dxy(),it->dsz());
    outTrack->SetErrors(it->qoverpError(),it->lambdaError(),
                        it->phiError(),it->dxyError(),it->dszError());
	
    // fill track quality information
    outTrack->SetChi2(it->chi2());
    outTrack->SetNdof(static_cast<Int_t>(it->ndof()));
    
    //fill hit layer map
    const reco::HitPattern &hits = it->hitPattern();
    for (Int_t i=0; i<hits.numberOfHits(); i++) {
      uint32_t hit = hits.getHitPattern(i);
      if (hits.validHitFilter(hit))
        if (hits.trackerHitFilter(hit))
          outTrack->SetHit(hitReader_.Layer(hit));
                
      if (0) {
        if (hits.muonDTHitFilter(hit))
          printf("Muon DT Layer = %i\n", hits.getLayer(hit));
        if (hits.muonCSCHitFilter(hit))
          printf("Muon CSC Layer = %i\n", hits.getLayer(hit));        
        if (hits.muonRPCHitFilter(hit))
          printf("Muon RPC Layer = %i\n", hits.getLayer(hit));
      }
    }
    
    // add reference between mithep and edm object
    reco::TrackRef theRef(hTrackProduct, it - inTracks.begin());
    trackMap_->Add(theRef, outTrack);
	
    if (trackingMap_ && !edmSimAssocName_.empty()) {
      //printf("Trying Track-Sim association\n");
      reco::TrackBaseRef theBaseRef(theRef);
      vector<pair<TrackingParticleRef, double> > simRefs;
      Bool_t noSimParticle = 0;
      try {
        simRefs = simAssociation[theBaseRef]; //try to get the sim references if existing
      }
      catch (edm::Exception &ex) {
        noSimParticle = 1;
      }

      if (!noSimParticle) { //loop through sim match candidates
        //printf("Applying track-sim association\n");
        for (vector<pair<TrackingParticleRef, double> >::const_iterator simRefPair=simRefs.begin(); 
             simRefPair != simRefs.end(); ++simRefPair) 

          if (simRefPair->second > 0.5) // require more than 50% shared hits between reco and sim
            outTrack->SetMCPart(trackingMap_->GetMit(simRefPair->first)); //add reco->sim reference
      }
    }
  }
  tracks_->Trim();
}

