#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "MitProd/TreeFiller/interface/FillerElectrons.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaReco/interface/ClusterShape.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "AnalysisDataFormats/Egamma/interface/ElectronID.h"
#include "AnalysisDataFormats/Egamma/interface/ElectronIDAssociation.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/ElectronTkIsolation.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaEcalIsolation.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaTowerIsolation.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/TransientTrack/plugins/TransientTrackBuilderESProducer.h"
#include "RecoVertex/GaussianSumVertexFit/interface/GsfVertexTrackCompatibilityEstimator.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MitAna/DataTree/interface/ElectronCol.h"
#include "MitAna/DataTree/interface/Names.h"
#include "MitAna/DataTree/interface/Track.h"
#include "MitEdm/DataFormats/interface/RefToBaseToPtr.h"
#include "MitProd/ObjectService/interface/ObjectService.h"
#include "MitEdm/DataFormats/interface/DecayPart.h"
#include "MitEdm/ConversionRejection/interface/ConversionMatcher.h"
#include "RecoVertex/VertexTools/interface/LinearizedTrackStateFactory.h"
#include "RecoVertex/VertexTools/interface/VertexTrackFactory.h"
#include "RecoVertex/VertexPrimitives/interface/VertexTrack.h"
#include "RecoVertex/VertexPrimitives/interface/CachingVertex.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexUpdator.h"
#include "MitEdm/Tools/interface/VertexReProducer.h"

using namespace std;
using namespace edm;
using namespace mithep;

//--------------------------------------------------------------------------------------------------
FillerElectrons::FillerElectrons(const edm::ParameterSet &cfg, const char *name, bool active) :
  BaseFiller(cfg,name,active),
  edmName_(Conf().getUntrackedParameter<string>("edmName","pixelMatchGsfElectrons")),
  expectedHitsName_(Conf().getUntrackedParameter<string>("expectedHitsName","")),  
  mitName_(Conf().getUntrackedParameter<string>("mitName",Names::gkElectronBrn)),
  gsfTrackMapName_(Conf().getUntrackedParameter<string>("gsfTrackMapName","")),
  trackerTrackMapName_(Conf().getUntrackedParameter<string>("trackerTrackMapName","")),
  barrelSuperClusterMapName_(Conf().getUntrackedParameter<string>("barrelSuperClusterMapName","")),
  endcapSuperClusterMapName_(Conf().getUntrackedParameter<string>("endcapSuperClusterMapName","")),
  checkClusterActive_(Conf().getUntrackedParameter<bool>("requireClusterAndGsfMap",true)),
  pfSuperClusterMapName_(Conf().getUntrackedParameter<string>("pfSuperClusterMapName","")),
  electronMapName_(Conf().getUntrackedParameter<string>("electronMapName","")),
  eIDCutBasedTightName_(Conf().getUntrackedParameter<string>("eIDCutBasedTightName","eidTight")),
  eIDCutBasedLooseName_(Conf().getUntrackedParameter<string>("eIDCutBasedLooseName","eidLoose")),
  eIDLikelihoodName_(Conf().getUntrackedParameter<string>("eIDLikelihoodName","")),
  pvEdmName_(Conf().getUntrackedParameter<string>("pvEdmName","offlinePrimaryVertices")),
  pvBSEdmName_(Conf().getUntrackedParameter<string>("pvBSEdmName","offlinePrimaryVerticesWithBS")),  
  recomputeConversionInfo_(Conf().getUntrackedParameter<bool>("recomputeConversionInfo",false)),  
  fitUnbiasedVertex_(Conf().getUntrackedParameter<bool>("fitUnbiasedVertex",true)),
  electronMap_(new mithep::ElectronMap),
  electrons_(new mithep::ElectronArr(16)),
  gsfTrackMap_(0),
  trackerTrackMap_(0),
  barrelSuperClusterMap_(0),
  endcapSuperClusterMap_(0)
{
  // Constructor.
}

//--------------------------------------------------------------------------------------------------
FillerElectrons::~FillerElectrons()
{
  // Destructor.

  delete electrons_;
  delete electronMap_;
}

//--------------------------------------------------------------------------------------------------
void FillerElectrons::BookDataBlock(TreeWriter &tws)
{
  // Add electron branch to our tree and get our maps.

  tws.AddBranch(mitName_,&electrons_);
  OS()->add<mithep::ElectronArr>(electrons_,mitName_);
  if (!gsfTrackMapName_.empty()) {
    gsfTrackMap_ = OS()->get<TrackMap>(gsfTrackMapName_);
    if (gsfTrackMap_)
      AddBranchDep(mitName_,gsfTrackMap_->GetBrName());
  }
  if (!trackerTrackMapName_.empty()) {
    trackerTrackMap_ = OS()->get<TrackMap>(trackerTrackMapName_);
    if (trackerTrackMap_)
      AddBranchDep(mitName_,trackerTrackMap_->GetBrName());
  }
  if (!barrelSuperClusterMapName_.empty()) {
    barrelSuperClusterMap_ = OS()->get<SuperClusterMap>(barrelSuperClusterMapName_);
    if (barrelSuperClusterMap_)
      AddBranchDep(mitName_,barrelSuperClusterMap_->GetBrName());
  }
  if (!endcapSuperClusterMapName_.empty()) {
    endcapSuperClusterMap_ = OS()->get<SuperClusterMap>(endcapSuperClusterMapName_);
    if (endcapSuperClusterMap_)
      AddBranchDep(mitName_,endcapSuperClusterMap_->GetBrName());
  }
  if (!pfSuperClusterMapName_.empty()) {
    pfSuperClusterMap_ = OS()->get<SuperClusterMap>(pfSuperClusterMapName_);
    if (pfSuperClusterMap_)
      AddBranchDep(mitName_,pfSuperClusterMap_->GetBrName());
  }
  if (!electronMapName_.empty()) {
    electronMap_->SetBrName(mitName_);
    OS()->add<ElectronMap>(electronMap_,electronMapName_);
  }
}

//--------------------------------------------------------------------------------------------------
void FillerElectrons::FillDataBlock(const edm::Event &event, const edm::EventSetup &setup)	 
{
  // Fill electrons from edm collection into our collection.

  electrons_  ->Delete();
  electronMap_->Reset();

  Handle<reco::GsfElectronCollection> hElectronProduct;
  GetProduct(edmName_, hElectronProduct, event);
  
  // handles to get the electron ID information
  Handle<edm::ValueMap<float> > eidLooseMap;
  GetProduct(eIDCutBasedLooseName_, eidLooseMap, event);
  Handle<edm::ValueMap<float> > eidTightMap;
  GetProduct(eIDCutBasedTightName_, eidTightMap, event);
  edm::Handle<edm::ValueMap<float> > eidLikelihoodMap;
  if (!eIDLikelihoodName_.empty()) {
    GetProduct(eIDLikelihoodName_, eidLikelihoodMap, event);  
  }
  
  edm::Handle<reco::VertexCollection> hVertex;
  event.getByLabel(pvEdmName_, hVertex);
  const reco::VertexCollection *pvCol = hVertex.product();
  edm::Handle<reco::VertexCollection> hVertexBS;
  event.getByLabel(pvBSEdmName_, hVertexBS);
  const reco::VertexCollection *pvBSCol = hVertexBS.product();
  edm::Handle<reco::TrackCollection> hGeneralTracks;
  event.getByLabel("generalTracks", hGeneralTracks);
  //const reco::VertexCollection *trackCol = hGeneralTracks.product();
  
  edm::Handle<reco::GsfTrackCollection> hGsfTracks;
  event.getByLabel("electronGsfTracks", hGsfTracks);

  edm::Handle<std::vector<mitedm::DecayPart> > hConversions;
  event.getByLabel("mvfConversionRemoval", hConversions);
  
  mitedm::ConversionMatcher convMatcher;
     
  edm::ESHandle<TransientTrackBuilder> hTransientTrackBuilder;
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder",hTransientTrackBuilder);
  const TransientTrackBuilder *transientTrackBuilder = hTransientTrackBuilder.product();
  
  GsfVertexTrackCompatibilityEstimator gsfEstimator;

  LinearizedTrackStateFactory lTrackFactory;
  VertexTrackFactory<5> vTrackFactory;
  KalmanVertexUpdator<5> updator;

   //Get Magnetic Field from event setup, taking value at (0,0,0)
  edm::ESHandle<MagneticField> magneticField;
  setup.get<IdealMagneticFieldRecord>().get(magneticField);
  const double bfield = magneticField->inTesla(GlobalPoint(0.,0.,0.)).z();

  const reco::GsfElectronCollection inElectrons = *(hElectronProduct.product());
  // loop over electrons
  for (reco::GsfElectronCollection::const_iterator iM = inElectrons.begin(); 
       iM != inElectrons.end(); ++iM) {

    // the index and Ref are needed for the eID association Map
    unsigned int iElectron = iM - inElectrons.begin();
    reco::GsfElectronRef eRef(hElectronProduct, iElectron);

    mithep::Electron *outElectron = electrons_->AddNew();
    
    outElectron->SetPtEtaPhi(iM->pt(),iM->eta(),iM->phi());
         
    outElectron->SetCharge(iM->charge());
    outElectron->SetScPixCharge(iM->scPixCharge());
    outElectron->SetESuperClusterOverP(iM->eSuperClusterOverP());
    outElectron->SetESeedClusterOverPout(iM->eSeedClusterOverPout());
    outElectron->SetEEleClusterOverPout(iM->eEleClusterOverPout());
    outElectron->SetPIn(iM->trackMomentumAtVtx().R());
    outElectron->SetPOut(iM->trackMomentumOut().R());
    outElectron->SetDeltaEtaSuperClusterTrackAtVtx(iM->deltaEtaSuperClusterTrackAtVtx());
    outElectron->SetDeltaEtaSeedClusterTrackAtCalo(iM->deltaEtaSeedClusterTrackAtCalo());
    outElectron->SetDeltaPhiSuperClusterTrackAtVtx(iM->deltaPhiSuperClusterTrackAtVtx());
    outElectron->SetDeltaPhiSeedClusterTrackAtCalo(iM->deltaPhiSeedClusterTrackAtCalo());
    outElectron->SetIsEnergyScaleCorrected(iM->isEnergyScaleCorrected());
    //outElectron->SetIsMomentumCorrected(iM->isMomentumCorrected());
    outElectron->SetNumberOfClusters(iM->basicClustersSize());
    outElectron->SetClassification(iM->classification());
    outElectron->SetFBrem(iM->fbrem());
    
    // pflow electron stuff
    outElectron->SetIsEcalDriven(iM->ecalDrivenSeed());
    outElectron->SetIsTrackerDriven(iM->trackerDrivenSeed());
    outElectron->SetMva(iM->mva());
    
    // shower shape variables   
    outElectron->SetE15(iM->e1x5());
    outElectron->SetE25Max(iM->e2x5Max());
    outElectron->SetE55(iM->e5x5());
    outElectron->SetCovEtaEta(iM->sigmaEtaEta());
    outElectron->SetCoviEtaiEta(iM->sigmaIetaIeta());
    outElectron->SetHadronicOverEm(iM->hcalOverEcal());
    outElectron->SetHcalDepth1OverEcal(iM->hcalDepth1OverEcal());
    outElectron->SetHcalDepth2OverEcal(iM->hcalDepth2OverEcal());
   
    // fill isolation variables for both cone sizes
    outElectron->SetEcalRecHitIsoDr04(iM->dr04EcalRecHitSumEt());
    outElectron->SetHcalDepth1TowerSumEtDr04(iM->dr04HcalDepth1TowerSumEt());
    outElectron->SetHcalDepth2TowerSumEtDr04(iM->dr04HcalDepth2TowerSumEt());
    outElectron->SetTrackIsolationDr04(iM->dr04TkSumPt());
    outElectron->SetEcalRecHitIsoDr03(iM->dr03EcalRecHitSumEt());
    outElectron->SetHcalTowerSumEtDr03(iM->dr03HcalTowerSumEt());
    outElectron->SetHcalDepth1TowerSumEtDr03(iM->dr03HcalDepth1TowerSumEt());
    outElectron->SetHcalDepth2TowerSumEtDr03(iM->dr03HcalDepth2TowerSumEt());
    outElectron->SetTrackIsolationDr03(iM->dr03TkSumPt());
     
    //pflow isolation
    outElectron->SetPFChargedHadronIso(iM->pfIsolationVariables().chargedHadronIso);
    outElectron->SetPFChargedHadronIso(iM->pfIsolationVariables().neutralHadronIso);
    outElectron->SetPFChargedHadronIso(iM->pfIsolationVariables().photonIso);
    
    // fiducial flags
    outElectron->SetIsEB(iM->isEB());
    outElectron->SetIsEE(iM->isEE());
    outElectron->SetIsEBEEGap(iM->isEBEEGap());
    outElectron->SetIsEBEtaGap(iM->isEBEtaGap());
    outElectron->SetIsEBPhiGap(iM->isEBPhiGap());
    outElectron->SetIsEEDeeGap(iM->isEEDeeGap());
    outElectron->SetIsEERingGap(iM->isEERingGap());
    
    // gsf-tracker match quality
    outElectron->SetFracSharedHits(iM->shFracInnerHits());

    // make proper links to Tracks and Super Clusters
    if (gsfTrackMap_ && iM->gsfTrack().isNonnull()) {
      try{outElectron->SetGsfTrk(gsfTrackMap_->GetMit(refToPtr(iM->gsfTrack())));}
      catch(...) { 
	if(checkClusterActive_)  throw edm::Exception(edm::errors::Configuration, "FillerElectrons:FillDataBlock()\n")
	  << "Error! GSF track unmapped collection " << edmName_ << endl;
      }
    }
    // make links to ambigous gsf tracks
    if (gsfTrackMap_) {
      for (reco::GsfTrackRefVector::const_iterator agsfi = iM->ambiguousGsfTracksBegin(); agsfi != iM->ambiguousGsfTracksEnd(); ++agsfi) {
        try{outElectron->AddAmbiguousGsfTrack(gsfTrackMap_->GetMit(refToPtr(*agsfi)));}
	catch(...) { 
	  if(checkClusterActive_)  throw edm::Exception(edm::errors::Configuration, "FillerElectrons:FillDataBlock()\n")
	    << "Error! GSF track unmapped collection " << edmName_ << endl;
	}
      }
    }
    
    // make tracker track links,
    if (trackerTrackMap_ && iM->closestCtfTrackRef().isNonnull()) {
        outElectron->SetTrackerTrk(trackerTrackMap_->GetMit(refToPtr(iM->closestCtfTrackRef())));
    }
   
    if (barrelSuperClusterMap_ && endcapSuperClusterMap_ && 
        pfSuperClusterMap_ && iM->superCluster().isNonnull()) {
      if(barrelSuperClusterMap_->HasMit(iM->superCluster())) {
        outElectron->SetSuperCluster(barrelSuperClusterMap_->GetMit(iM->superCluster()));        
      }
      else if (endcapSuperClusterMap_->HasMit(iM->superCluster())) {
        outElectron->SetSuperCluster(endcapSuperClusterMap_->GetMit(iM->superCluster()));
      }
      else if (pfSuperClusterMap_->HasMit(iM->superCluster())) {
        outElectron->SetSuperCluster(pfSuperClusterMap_->GetMit(iM->superCluster()));  
      }
      else if(checkClusterActive_) {
	throw edm::Exception(edm::errors::Configuration, "FillerElectrons:FillDataBlock()\n")
             << "Error! SuperCluster reference in unmapped collection " << edmName_ << endl;
      }
    }
  
    //compute NLayersWithMeasurement for associated ctf track
    if (iM->closestCtfTrackRef().isNonnull()) {
      outElectron->SetCTFTrkNLayersWithMeasurement(iM->closestCtfTrackRef()->hitPattern().trackerLayersWithMeasurement());
    } else {
      outElectron->SetCTFTrkNLayersWithMeasurement(-1);
    }

    //compute impact parameter with respect to PV
    if (iM->gsfTrack().isNonnull()) {
      const reco::TransientTrack &tt = transientTrackBuilder->build(iM->gsfTrack()); 

      reco::TransientTrack ttckf;

      reco::Vertex thevtx = pvCol->at(0);
      reco::Vertex thevtxbs = pvBSCol->at(0);

      reco::Vertex thevtxub = pvCol->at(0);
      reco::Vertex thevtxubbs = pvBSCol->at(0);
     
      //check if closest ctf track is included in PV and if so, remove it before computing impact parameters and uncertainties
      if (iM->closestCtfTrackRef().isNonnull()) {
        ttckf = transientTrackBuilder->build(iM->closestCtfTrackRef());
	
        //check if closest ctf track is included in PV and if so, remove it from the collection of 
        //tracks associated with the PV and perform a refit before computing impact parameters and uncertainties
        reco::TrackCollection newTkCollection;
        bool foundMatch = false;
        for(reco::Vertex::trackRef_iterator itk = thevtx.tracks_begin(); itk!=thevtx.tracks_end(); itk++) {
          if(iM->closestCtfTrack().ctfTrack.isNonnull()) {
            bool refMatching = (itk->get() == &*(iM->closestCtfTrack().ctfTrack));
            float shFraction = iM->closestCtfTrack().shFracInnerHits;
            if(refMatching && shFraction > 0.5) {
              foundMatch = true; 
	      continue;
            }
          }       
          newTkCollection.push_back(*itk->get());
        }

        if(foundMatch && fitUnbiasedVertex_) {
          edm::Handle<reco::BeamSpot> bs;
          event.getByLabel(edm::InputTag("offlineBeamSpot"),bs);
	  
	  VertexReProducer revertex(hVertex,event); //Needs to be fixed

	  edm::Handle<reco::BeamSpot> pvbeamspot;
          event.getByLabel(revertex.inputBeamSpot(),pvbeamspot);
	  vector<TransientVertex> pvs = revertex.makeVertices(newTkCollection,*pvbeamspot,setup);
	  if(pvs.size()>0) {
            thevtxub = pvs.front();      // take the first in the list
          }
          VertexReProducer revertexbs(hVertexBS,event);
          edm::Handle<reco::BeamSpot> pvbsbeamspot;
          event.getByLabel(revertexbs.inputBeamSpot(),pvbsbeamspot);
          vector<TransientVertex> pvbss = revertexbs.makeVertices(newTkCollection,*pvbsbeamspot,setup);
	  if(pvbss.size()>0) {
            thevtxubbs = pvbss.front();  // take the first in the list
          }
        }
      }
      //preserve sign of transverse impact parameter (cross-product definition from track, not lifetime-signing)
      const double gsfsign   = ( (-iM->gsfTrack()->dxy(thevtx.position()))   >=0 ) ? 1. : -1.;
      const double gsfsignbs = ( (-iM->gsfTrack()->dxy(thevtxbs.position())) >=0 ) ? 1. : -1.;
      const std::pair<bool,Measurement1D> &d0pv =  IPTools::absoluteTransverseImpactParameter(tt,thevtx);
      if (d0pv.first) {
        outElectron->SetD0PV(gsfsign*d0pv.second.value());
        outElectron->SetD0PVErr(d0pv.second.error());
      }
      else {
        outElectron->SetD0PV(-999.0);
      }

      const std::pair<bool,Measurement1D> &ip3dpv =  IPTools::absoluteImpactParameter3D(tt,thevtx);
      if (ip3dpv.first) {
        outElectron->SetIp3dPV(gsfsign*ip3dpv.second.value());
        outElectron->SetIp3dPVErr(ip3dpv.second.error());
      }
      else {
        outElectron->SetIp3dPV(-999.0);
      }

      const std::pair<bool,Measurement1D> &d0pvbs =  IPTools::absoluteTransverseImpactParameter(tt,thevtxbs);
      if (d0pvbs.first) {
        outElectron->SetD0PVBS(gsfsignbs*d0pvbs.second.value());
        outElectron->SetD0PVBSErr(d0pvbs.second.error());
      }
      else {
        outElectron->SetD0PVBS(-999.0);
      }

      const std::pair<bool,Measurement1D> &ip3dpvbs =  IPTools::absoluteImpactParameter3D(tt,thevtxbs);
      if (ip3dpvbs.first) {
        outElectron->SetIp3dPVBS(gsfsignbs*ip3dpvbs.second.value());
        outElectron->SetIp3dPVBSErr(ip3dpvbs.second.error());
      }
      else {
        outElectron->SetIp3dPVBS(-999.0);
      }

      const std::pair<bool,Measurement1D> &d0pvub =  IPTools::absoluteTransverseImpactParameter(tt,thevtxub);
      if (d0pvub.first) {
        outElectron->SetD0PVUB(gsfsign*d0pvub.second.value());
        outElectron->SetD0PVUBErr(d0pvub.second.error());
      }
      else {
        outElectron->SetD0PVUB(-999.0);
      }


      const std::pair<bool,Measurement1D> &ip3dpvub =  IPTools::absoluteImpactParameter3D(tt,thevtxub);
      if (ip3dpvub.first) {
        outElectron->SetIp3dPVUB(gsfsign*ip3dpvub.second.value());
        outElectron->SetIp3dPVUBErr(ip3dpvub.second.error());
      }
      else {
        outElectron->SetIp3dPVUB(-999.0);
      }

      const std::pair<bool,Measurement1D> &d0pvubbs =  IPTools::absoluteTransverseImpactParameter(tt,thevtxubbs);
      if (d0pvubbs.first) {
        outElectron->SetD0PVUBBS(gsfsignbs*d0pvubbs.second.value());
        outElectron->SetD0PVUBBSErr(d0pvubbs.second.error());
      }
      else {
        outElectron->SetD0PVUBBS(-999.0);
      }

      const std::pair<bool,Measurement1D> &ip3dpvubbs =  IPTools::absoluteImpactParameter3D(tt,thevtxubbs);
      if (ip3dpvubbs.first) {
        outElectron->SetIp3dPVUBBS(gsfsignbs*ip3dpvubbs.second.value());
        outElectron->SetIp3dPVUBBSErr(ip3dpvubbs.second.error());
      }
      else {
        outElectron->SetIp3dPVUBBS(-999.0);
      }

      if (iM->closestCtfTrackRef().isNonnull()) {

        const double ckfsign   = ( (-iM->closestCtfTrackRef()->dxy(thevtx.position()))   >=0 ) ? 1. : -1.;
        const double ckfsignbs = ( (-iM->closestCtfTrackRef()->dxy(thevtxbs.position())) >=0 ) ? 1. : -1.;

        const std::pair<bool,Measurement1D> &d0pvckf =  IPTools::absoluteTransverseImpactParameter(ttckf,thevtx);
        if (d0pvckf.first) {
          outElectron->SetD0PVCkf(ckfsign*d0pvckf.second.value());
          outElectron->SetD0PVCkfErr(d0pvckf.second.error());
        }
        else {
          outElectron->SetD0PVCkf(-999.0);
        }
  
  
        const std::pair<bool,Measurement1D> &ip3dpvckf =  IPTools::absoluteImpactParameter3D(ttckf,thevtx);
        if (ip3dpvckf.first) {
          outElectron->SetIp3dPVCkf(ckfsign*ip3dpvckf.second.value());
          outElectron->SetIp3dPVCkfErr(ip3dpvckf.second.error());
        }
        else {
          outElectron->SetIp3dPVCkf(-999.0);
        }
  
        const std::pair<bool,Measurement1D> &d0pvbsckf =  IPTools::absoluteTransverseImpactParameter(ttckf,thevtxbs);
        if (d0pvbsckf.first) {
          outElectron->SetD0PVBSCkf(ckfsignbs*d0pvbsckf.second.value());
          outElectron->SetD0PVBSCkfErr(d0pvbsckf.second.error());
        }
        else {
          outElectron->SetD0PVBSCkf(-999.0);
        }
  
        const std::pair<bool,Measurement1D> &ip3dpvbsckf =  IPTools::absoluteImpactParameter3D(ttckf,thevtxbs);
        if (ip3dpvbsckf.first) {
          outElectron->SetIp3dPVBSCkf(ckfsignbs*ip3dpvbsckf.second.value());
          outElectron->SetIp3dPVBSCkfErr(ip3dpvbsckf.second.error());
        }
        else {
          outElectron->SetIp3dPVBSCkf(-999.0);
        }
//////////////

        const std::pair<bool,Measurement1D> &d0pvubckf =  IPTools::absoluteTransverseImpactParameter(ttckf,thevtxub);
        if (d0pvubckf.first) {
          outElectron->SetD0PVUBCkf(ckfsign*d0pvubckf.second.value());
          outElectron->SetD0PVUBCkfErr(d0pvubckf.second.error());
        }
        else {
          outElectron->SetD0PVUBCkf(-999.0);
        }
  
  
        const std::pair<bool,Measurement1D> &ip3dpvubckf =  IPTools::absoluteImpactParameter3D(ttckf,thevtxub);
        if (ip3dpvubckf.first) {
          outElectron->SetIp3dPVUBCkf(ckfsign*ip3dpvubckf.second.value());
          outElectron->SetIp3dPVUBCkfErr(ip3dpvubckf.second.error());
        }
        else {
          outElectron->SetIp3dPVUBCkf(-999.0);
        }
  
        const std::pair<bool,Measurement1D> &d0pvubbsckf =  IPTools::absoluteTransverseImpactParameter(ttckf,thevtxubbs);
        if (d0pvubbsckf.first) {
          outElectron->SetD0PVUBBSCkf(ckfsignbs*d0pvubbsckf.second.value());
          outElectron->SetD0PVUBBSCkfErr(d0pvubbsckf.second.error());
        }
        else {
          outElectron->SetD0PVUBBSCkf(-999.0);
        }
  
        const std::pair<bool,Measurement1D> &ip3dpvubbsckf =  IPTools::absoluteImpactParameter3D(ttckf,thevtxubbs);
        if (ip3dpvubbsckf.first) {
          outElectron->SetIp3dPVUBBSCkf(ckfsignbs*ip3dpvubbsckf.second.value());
          outElectron->SetIp3dPVUBBSCkfErr(ip3dpvubbsckf.second.error());
        }
        else {
          outElectron->SetIp3dPVUBBSCkf(-999.0);
        }

      }
      else {
        outElectron->SetD0PVCkf(-999.0);
        outElectron->SetIp3dPVCkf(-999.0);
        outElectron->SetD0PVBSCkf(-999.0);
        outElectron->SetIp3dPVBSCkf(-999.0);

        outElectron->SetD0PVUBCkf(-999.0);
        outElectron->SetIp3dPVUBCkf(-999.0);
        outElectron->SetD0PVUBBSCkf(-999.0);
        outElectron->SetIp3dPVUBBSCkf(-999.0);
      }

      if (verbose_>1) {
        printf("gsf track      pt = %5f\n",iM->gsfTrack()->pt());
        printf("gsf track mode pt = %5f\n",iM->gsfTrack()->ptMode());
        printf("ttrack         pt = %5f\n",tt.initialFreeState().momentum().perp());
        //printf("ttrackgsf      pt = %5f\n",ttgsf.innermostMeasurementState().globalMomentum().perp());
        printf("ip3dpv reduced chisquared = %5f, probability = %5f\n", ip3dpv.second.value()/ip3dpv.second.error(), TMath::Prob(ip3dpv.second.value()/ip3dpv.second.error(),1));
        //printf("gsf    reduced chisquared = %5f, probability = %5f\n", pvGsfCompat.second/2, TMath::Prob(pvGsfCompat.second,2));
      }
    }
    

    //fill conversion partner track info
    if (recomputeConversionInfo_) {
      ConversionFinder convFinder;         outElectron->SetConvPartnerDCotTheta(iM->convDcot());
      ConversionInfo convInfo = convFinder.getConversionInfo(*iM, hGeneralTracks, hGsfTracks, bfield);
  
      outElectron->SetConvFlag(convInfo.flag());
      outElectron->SetConvPartnerDCotTheta(convInfo.dcot());
      outElectron->SetConvPartnerDist(convInfo.dist());
      outElectron->SetConvPartnerRadius(convInfo.radiusOfConversion());
      reco::TrackRef ckfconvTrackRef = convInfo.conversionPartnerCtfTk();
      reco::GsfTrackRef gsfconvTrackRef = convInfo.conversionPartnerGsfTk();
  
  
      if ( gsfconvTrackRef.isNonnull() && gsfTrackMap_  ) {
        try {outElectron->SetConvPartnerTrk(gsfTrackMap_->GetMit(edm::refToPtr(gsfconvTrackRef)));}
	  catch(...) { 
	    if(checkClusterActive_)  throw edm::Exception(edm::errors::Configuration, "FillerElectrons:FillDataBlock()\n")
	      << "Error! GSF track unmapped collection " << edmName_ << endl;
	  }
	
      }
      else if (ckfconvTrackRef.isNonnull() && trackerTrackMap_) {
        outElectron->SetConvPartnerTrk(trackerTrackMap_->GetMit(edm::refToPtr(ckfconvTrackRef)));
      }
    }
    else {
      outElectron->SetConvFlag(iM->convFlags());
      outElectron->SetConvPartnerDCotTheta(iM->convDcot());
      outElectron->SetConvPartnerDist(iM->convDist());
      outElectron->SetConvPartnerRadius(iM->convRadius());
      reco::TrackBaseRef convTrackRef = iM->convPartner();
      if (convTrackRef.isNonnull()) {
        if ( dynamic_cast<const reco::GsfTrack*>(convTrackRef.get()) && gsfTrackMap_  ) {
          try{outElectron->SetConvPartnerTrk(gsfTrackMap_->GetMit(mitedm::refToBaseToPtr(convTrackRef)));}
	  catch(...) { 
	    if(checkClusterActive_)  throw edm::Exception(edm::errors::Configuration, "FillerElectrons:FillDataBlock()\n")
	      << "Error! GSF track unmapped collection " << edmName_ << endl;
	  }
        }
        else if (trackerTrackMap_) {
          outElectron->SetConvPartnerTrk(trackerTrackMap_->GetMit(mitedm::refToBaseToPtr(convTrackRef)));
        }
      }
    }
    


    // fill Electron ID information
    outElectron->SetPassLooseID((*eidLooseMap)[eRef]);
    outElectron->SetPassTightID((*eidTightMap)[eRef]);
    if (!eIDLikelihoodName_.empty()) {
      outElectron->SetIDLikelihood((*eidLikelihoodMap)[eRef]);
    }
    // fill corrected expected inner hits
    if(iM->gsfTrack().isNonnull()) {
      outElectron->SetCorrectedNExpectedHitsInner(iM->gsfTrack()->trackerExpectedHitsInner().numberOfHits());
    }
    //fill additional conversion flag
    outElectron->SetMatchesVertexConversion(convMatcher.matchesGoodConversion(*iM,hConversions));
    
    // add electron to map
    edm::Ptr<reco::GsfElectron> thePtr(hElectronProduct, iM - inElectrons.begin());
    electronMap_->Add(thePtr, outElectron);
 
    if (verbose_>1) {
      double recomass = sqrt(iM->energy()*iM->energy() - iM->p()*iM->p());
      printf(" mithep::Electron,    pt=%5f, eta=%5f, phi=%5f, energy=%5f, p=%5f, mass=%5f\n",
             outElectron->Pt(), outElectron->Eta(), outElectron->Phi(), 
             outElectron->E(), outElectron->P(), outElectron->Mass());
      printf("reco::GsfElectron   , pt=%5f, eta=%5f, phi=%5f, energy=%5f, p=%5f, mass=%5f\n",
             iM->pt(), iM->eta(), iM->phi(), iM->energy(), iM->p(), recomass);  
    }
  } 
  electrons_->Trim();
}
