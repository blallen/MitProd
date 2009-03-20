//--------------------------------------------------------------------------------------------------
// $Id: FillerPFJets.h,v 1.2 2009/03/15 11:20:40 loizides Exp $
//
// FillerPFJets
//
// Implementation of a filler to fill EDM particle flow jets into our mithep::PFJet data structure.
//
// Authors: C.Loizides
//--------------------------------------------------------------------------------------------------

#ifndef MITPROD_TREEFILLER_FILLERPFJETS_H
#define MITPROD_TREEFILLER_FILLERPFJETS_H

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "MitAna/DataUtil/interface/TreeWriter.h"
#include "MitAna/DataTree/interface/Collections.h"
#include "MitProd/TreeFiller/interface/BaseFiller.h"
#include "MitProd/TreeFiller/interface/AssociationMaps.h"

namespace mithep 
{
  class FillerPFJets : public BaseFiller
  {  
    public:
      FillerPFJets(const edm::ParameterSet &cfg, const char *name, bool active=1);
      ~FillerPFJets();

      void            BookDataBlock(TreeWriter &tws);
      void 	      FillDataBlock(const edm::Event &e, const edm::EventSetup &es);
  
    private:
      bool            flavorMatchingActive_;            //=true if flavor matching is done  
      bool            bTaggingActive_;                  //=true if bTagging info is filled
      bool            jetToVertexActive_;               //=true if jet to vertex info is done
      bool            jetCorrectionsActive_;            //=true if jet corrections are done
      std::string     edmName_;                         //edm name of jets collection
      std::string     mitName_;                         //mit name of jets collection
      std::string     jetToVertexAlphaName_;            //edm name of jet to vertex alpha coll
      std::string     jetToVertexBetaName_;             //edm name of jet to vertex beta coll
      std::string     L2JetCorrectorName_;              //label of the L2JetCorrection service
      std::string     L3JetCorrectorName_;              //label of the L3JetCorrection service
      std::string     flavorMatchingByReferenceName_;   //source of flavor matching
      std::string     flavorMatchingDefinition_;        //type of flavor matching
      std::string     jetProbabilityBJetTagsName_;             //bjet algo discriminant
      std::string     jetBProbabilityBJetTagsName_;            //bjet algo discriminant
      std::string     simpleSecondaryVertexBJetTagsName_;      //bjet algo discriminant
      std::string     combinedSecondaryVertexBJetTagsName_;    //bjet algo discriminant
      std::string     combinedSecondaryVertexMVABJetTagsName_; //bjet algo discriminant
      std::string     impactParameterMVABJetTagsName_;         //bjet algo discriminant
      std::string     trackCountingHighEffBJetTagsName_;       //bjet algo discriminant
      std::string     trackCountingHighPurBJetTagsName_;       //bjet algo discriminant
      std::string     softMuonBJetTagsName_;                   //bjet algo discriminant        
      std::string     softMuonNoIPBJetTagsName_;               //bjet algo discriminant
      std::string     softElectronBJetTagsName_;               //bjet algo discriminant
      std::string     pfCandMapName_;                   //name of imported PFCandidateMap
      std::string     jetMapName_;                      //name of exported PFJetMap
      const mithep::PFCandidateMap       *pfCandMap_;   //map wrt PFCandidates
      mithep::PFJetMap                   *jetMap_;      //export map
      mithep::PFJetArr                   *jets_;        //array of Jets
  };
}
#endif