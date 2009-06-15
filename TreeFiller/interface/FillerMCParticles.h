//--------------------------------------------------------------------------------------------------
// $Id: FillerMCParticles.h,v 1.7 2009/03/22 10:00:45 loizides Exp $
//
// FillerMCParticles
//
// Imlementation of a filler to fill HepMC particles or the AOD GenParticle candidates (gen)
// and SimTracks (sim) with association map to TrackingParticles (for hit-based MC truth matching)
// into mithep::MCParticles. Generated and simulated particle information is thus merged into a 
// single collection.
//
// Authors: C.Loizides, J.Bendavid
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREEFILLER_FILLERMCPARTICLES_H
#define MITPROD_TREEFILLER_FILLERMCPARTICLES_H

#include "MitAna/DataTree/interface/MCParticleFwd.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"

namespace mithep 
{
  class FillerMCParticles : public BaseFiller
  {
    public:
      FillerMCParticles(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerMCParticles();

      void                           BookDataBlock(TreeWriter &tws);
      void                           FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
      void                           ResolveLinks (const edm::Event &e, const edm::EventSetup &es);
  
    private:
      bool                           genActive_;       //=true if generated particles are filled
      bool                           useAodGen_;       //=true if AOD GenParticles to be used
      bool                           simActive_;       //=true if simulated particles are filled
      bool                           trackingActive_;  //=true if TrackingParticles are mapped
      std::string                    genEdmName_;      //edm name of generated particles
      std::string                    simEdmName_;      //edm name of simulated particles
      std::string                    trackingEdmName_; //edm name of simulated TrackingParticles
      std::string                    genMapName_;      //name of exp map wrt generated particles
      std::string                    simMapName_;      //name of exp map wrt simulated particles
      std::string                    trackingMapName_; //name of exp map wrt TrackingParticles
      std::string                    mitName_;         //name of MCParticles branch
      mithep::MCParticleArr         *mcParticles_;     //array of MCParticles
      mithep::GenParticleBarcodeMap *genMap_;          //map wrt generated particles
      mithep::AODGenParticleMap     *aodGenMap_;       //map wrt generated particles
      mithep::SimTrackTidMap        *simMap_;          //map of SimTracks to G4 track ids
      mithep::TrackingParticleMap   *trackingMap_;     //map wrt TrackingParticles
  };
}
#endif
