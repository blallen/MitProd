# $Id: MitTreeFiller_cfi.py,v 1.27 2009/03/06 14:40:10 bendavid Exp $

import FWCore.ParameterSet.Config as cms

MitTreeFiller = cms.EDAnalyzer("FillMitTree",
    defactive   = cms.untracked.bool(True),

    fillerOrder = cms.untracked.vstring('MetaInfos',
                                        'MCParticles',
                                        'BeamSpot',
                                        'PrimaryVertexes',
                                        'PrimaryVertexesBS',
                                        'CaloTowers',
                                        'BarrelBasicClusters',
                                        'BarrelSuperClusters',
                                        'EndcapBasicClusters',
                                        'EndcapSuperClusters',
                                        'GeneralTracks',
                                        'StandaloneMuonTracks',
                                        'StandaloneMuonTracksWVtxConstraint'
                                        'GlobalMuonTracks',
                                        'ConversionInOutTracks',
                                        'ConversionOutInTracks',
                                        'GsfTracks',
                                        'Muons',
                                        'Electrons',
                                        'ConversionElectrons',
                                        'Conversions',
                                        'Photons',
                                        'IC5GenJets',
                                        'SC5GenJets',
                                        'SC7GenJets',
                                        'KT4GenJets',
                                        'KT6GenJets',
                                        'ItrCone5Jets',
                                        'SisCone5Jets',
                                        'SisCone7Jets',
                                        'Kt4Jets',
                                        'Kt6Jets',
                                        'IC5JetPlusTrack',
                                        'ItrCone5Met',
                                        'SisCone5Met',
                                        'SisCone7Met',
                                        'Kt4Met',
                                        'Kt6Met',
                                        'StableParts',
                                        'DecayParts'),

    MetaInfos = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        hltActive  = cms.untracked.bool(True),
        hltName    = cms.untracked.string('TriggerResults::HLT'),
        fillerType = cms.untracked.string('FillerMetaInfos')
    ),
                   
    MCParticles = cms.untracked.PSet(
        active          = cms.untracked.bool(True),
        genActive       = cms.untracked.bool(True),
        useAodGen       = cms.untracked.bool(True),
        simActive       = cms.untracked.bool(True),
        trackingActive  = cms.untracked.bool(False),
        mitName         = cms.untracked.string('MCParticles'),
        genJetMitName   = cms.untracked.string('GenJets'),
        genEdmName      = cms.untracked.string('genParticles'),
        simEdmName      = cms.untracked.string('g4SimHits'),
        trackingEdmName = cms.untracked.string('mergedtruth:MergedTrackTruth'),
        genMapName      = cms.untracked.string('GenMap'),
        simMapName      = cms.untracked.string('SimMap'),
        trackingMapName = cms.untracked.string('TrackingMap'), 
        fillerType      = cms.untracked.string('FillerMCParticles')
    ),
          
    BeamSpot = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('BeamSpot'),
        edmName    = cms.untracked.string('offlineBeamSpot'),    
        fillerType = cms.untracked.string('FillerBeamSpot')
    ),
                
    PrimaryVertexes = cms.untracked.PSet(
        active        = cms.untracked.bool(True),
        mitName       = cms.untracked.string('PrimaryVertexes'),
        edmName       = cms.untracked.string('offlinePrimaryVertices'),    
        vertexMapName = cms.untracked.string('PrimaryVertexMap'),
        fillerType    = cms.untracked.string('FillerVertexes')
    ),
    
    PrimaryVertexesBS = cms.untracked.PSet(
        active        = cms.untracked.bool(True),
        mitName       = cms.untracked.string('PrimaryVertexesBeamSpot'),
        edmName       = cms.untracked.string('offlinePrimaryVerticesWithBS'),    
        vertexMapName = cms.untracked.string('PrimaryVertexBSMap'),
        fillerType    = cms.untracked.string('FillerVertexes')
    ),

    CaloTowers = cms.untracked.PSet(
        active           = cms.untracked.bool(True),
        mitName          = cms.untracked.string('CaloTowers'),
        edmName          = cms.untracked.string('towerMaker'),    
        caloTowerMapName = cms.untracked.string('CaloTowerMap'),
        fillerType       = cms.untracked.string('FillerCaloTowers')
    ),

    BarrelBasicClusters = cms.untracked.PSet(
        active              = cms.untracked.bool(True),
        mitName             = cms.untracked.string('BarrelBasicClusters'),
        edmName             = cms.untracked.string('hybridSuperClusters:hybridBarrelBasicClusters'),
        basicClusterMapName = cms.untracked.string('barrelBasicClusterMap'),
        fillerType          = cms.untracked.string('FillerBasicClusters')
    ),
                                
    BarrelSuperClusters = cms.untracked.PSet(
        active                = cms.untracked.bool(True),
        mitName               = cms.untracked.string('BarrelSuperClusters'),
        edmName               = cms.untracked.string('correctedHybridSuperClusters'),
        basicClusterMapName   = cms.untracked.string('barrelBasicClusterMap'),
        superClusterMapName   = cms.untracked.string('barrelSuperClusterMap'),
        superClusterIdMapName = cms.untracked.string('barrelSuperClusterIdMap'),
        fillerType            = cms.untracked.string('FillerSuperClusters')
    ),

    EndcapBasicClusters = cms.untracked.PSet(
        active              = cms.untracked.bool(True),
        mitName             = cms.untracked.string('EndcapBasicClusters'),
        edmName             = cms.untracked.string('multi5x5BasicClusters:multi5x5EndcapBasicClusters'),  
        basicClusterMapName = cms.untracked.string('endcapBasicClusterMap'),
        fillerType          = cms.untracked.string('FillerBasicClusters')
    ),

    EndcapSuperClusters = cms.untracked.PSet(
        active                = cms.untracked.bool(True),
        mitName               = cms.untracked.string('EndcapSuperClusters'),                     
        edmName               = cms.untracked.string('correctedMulti5x5SuperClustersWithPreshower'),
        basicClusterMapName   = cms.untracked.string('endcapBasicClusterMap'),
        superClusterMapName   = cms.untracked.string('endcapSuperClusterMap'),
        superClusterIdMapName = cms.untracked.string('endcapSuperClusterIdMap'),
        fillerType            = cms.untracked.string('FillerSuperClusters')
    ),

    GeneralTracks  = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('Tracks'),
        edmName                   = cms.untracked.string('generalTracks'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('TracksMapName'),
        edmSimAssociationName     = cms.untracked.string('trackingParticleRecoTrackAsssociation'),
        fillerType                = cms.untracked.string('FillerTracks')
    ),

    StandaloneMuonTracks = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('StandaloneMuonTracks'),
        edmName                   = cms.untracked.string('standAloneMuons'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('StandaloneMuonTracksMapName'),
        edmSimAssociationName     = cms.untracked.string(''),
        fillerType                = cms.untracked.string('FillerTracks')
    ),

    StandaloneMuonTracksWVtxConstraint = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('StandaloneMuonTracksWVtxConstraint'),
        edmName                   = cms.untracked.string('standAloneMuons:UpdatedAtVtx'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('StandaloneMuonTracksWVtxConstraintMapName'),
        edmSimAssociationName     = cms.untracked.string(''),
        fillerType                = cms.untracked.string('FillerTracks')
    ),
                   
    GlobalMuonTracks = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('GlobalMuonTracks'),
        edmName                   = cms.untracked.string('globalMuons'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('GlobalMuonTracksMapName'),
        edmSimAssociationName     = cms.untracked.string(''),
        fillerType                = cms.untracked.string('FillerTracks')
    ),
                   
    ConversionInOutTracks = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('ConversionInOutTracks'),
        edmName                   = cms.untracked.string('ckfInOutTracksFromConversions'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('ConversionInOutTracksMapName'),
        edmSimAssociationName     = cms.untracked.string('assocInOutConversionTracks'),
        fillerType                = cms.untracked.string('FillerTracks')
    ),

    ConversionOutInTracks = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('ConversionOutInTracks'),
        edmName                   = cms.untracked.string('ckfOutInTracksFromConversions'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('ConversionOutInTracksMapName'),
        edmSimAssociationName     = cms.untracked.string('assocOutInConversionTracks'),
        fillerType                = cms.untracked.string('FillerTracks')
    ),
                   
    GsfTracks = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        ecalAssocActive           = cms.untracked.bool(False),
        mitName                   = cms.untracked.string('GsfTracks'),
        edmName                   = cms.untracked.string('pixelMatchGsfFit'),
        trackingMapName           = cms.untracked.string('TrackingMap'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        trackMapName              = cms.untracked.string('GsfTracksMapName'),
        edmSimAssociationName     = cms.untracked.string('assoc2GsfTracks'),
        fillerType                = cms.untracked.string('FillerTracks')
    ),
  
    Muons = cms.untracked.PSet(
        active              = cms.untracked.bool(True),
        mitName             = cms.untracked.string('Muons'),
        edmName             = cms.untracked.string('muons'),
        globalTrackMapName  = cms.untracked.string('GlobalMuonTracksMapName'),
        staTrackMapName     = cms.untracked.string('StandaloneMuonTracksMapName'),
        staVtxTrackMapName  = cms.untracked.string('StandaloneMuonTracksWVtxConstraintMapName'),
        trackerTrackMapName = cms.untracked.string('TracksMapName'),
        fillerType          = cms.untracked.string('FillerMuons')
    ),
                   
    Electrons = cms.untracked.PSet(
        active                           = cms.untracked.bool(True),
        mitName                          = cms.untracked.string('Electrons'),
        edmName                          = cms.untracked.string('pixelMatchGsfElectrons'),
        gsfTrackMapName                  = cms.untracked.string('GsfTracksMapName'), 
        trackerTrackMapName              = cms.untracked.string('TracksMapName'),
        barrelEcalRecHitName             = cms.untracked.string('reducedEcalRecHitsEB'),
        endcapEcalRecHitName             = cms.untracked.string('reducedEcalRecHitsEE'),
        barrelBasicClusterName           = cms.untracked.string('hybridSuperClusters:hybridBarrelBasicClusters'),
        endcapBasicClusterName           = cms.untracked.string('multi5x5BasicClusters:multi5x5EndcapBasicClusters'),
        barrelSuperClusterName           = cms.untracked.string('correctedHybridSuperClusters'),
        endcapSuperClusterName           = cms.untracked.string('multi5x5SuperClusters:multi5x5EndcapSuperClusters'),
        barrelSuperClusterMapName        = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName        = cms.untracked.string('endcapSuperClusterMap'),
        eIDCutBasedLooseName             = cms.untracked.string('eidLoose'),
        eIDCutBasedTightName             = cms.untracked.string('eidTight'),
        eIDLikelihood                    = cms.untracked.string('eidLikelihoodExt'),
        eIDNeuralNet                     = cms.untracked.string('eidNeuralNet'),
        IsolationTrackCollectionName     = cms.untracked.string('generalTracks'),
        IsolationCaloTowerCollectionName = cms.untracked.string('towerMaker'),
        EcalJurassicIsolationName        = cms.untracked.string('eleIsoFromDepsEcalFromHits'),
        HcalJurassicIsolationName        = cms.untracked.string('eleIsoFromDepsHcalFromHits'),
        TrackerIsolationName             = cms.untracked.string('eleIsoFromDepsTk'),
        gsfTrackAssocName                = cms.untracked.string(''),
        fillerType                       = cms.untracked.string('FillerElectrons')
    ),

    ConversionElectrons = cms.untracked.PSet(
        active                = cms.untracked.bool(True),
        mitName               = cms.untracked.string('ConversionElectrons'),
        convInOutTracksName   = cms.untracked.string('ConversionInOutTracks'),
        convOutInTracksName   = cms.untracked.string('ConversionOutInTracks'),
        convInOutTrackMapName = cms.untracked.string('ConversionInOutTracksMapName'),
        convOutInTrackMapName = cms.untracked.string('ConversionOutInTracksMapName'),
        convElectronMapName   = cms.untracked.string('ConversionElectronsMapName'),
        fillerType            = cms.untracked.string('FillerConversionElectrons')
    ),
                   
    Conversions = cms.untracked.PSet(
        active              = cms.untracked.bool(True),
        mitName             = cms.untracked.string('Conversions'),
        edmName             = cms.untracked.string('conversions'),
        convElectronMapName = cms.untracked.string('ConversionElectronsMapName'),
        conversionMapName   = cms.untracked.string('ConversionsMapName'),
        fillerType          = cms.untracked.string('FillerConversions')
    ),

    Photons = cms.untracked.PSet(
        active                    = cms.untracked.bool(True),
        mitName                   = cms.untracked.string('Photons'),
        edmName                   = cms.untracked.string('photons'),
        photonIDName              = cms.untracked.string('PhotonIDProd:PhotonAssociatedID'),
        conversionMapName         = cms.untracked.string('ConversionsMapName'),
        barrelSuperClusterMapName = cms.untracked.string('barrelSuperClusterMap'),
        endcapSuperClusterMapName = cms.untracked.string('endcapSuperClusterMap'),
        fillerType                = cms.untracked.string('FillerPhotons')
    ),

    IC5GenJets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('IC5GenJets'),
        edmName                       = cms.untracked.string('iterativeCone5GenJets'),
        flavorMatchingByReferenceName = cms.untracked.string('GenIC5byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        fillerType                    = cms.untracked.string('FillerGenJets')
    ),

    SC5GenJets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('SC5GenJets'),
        edmName                       = cms.untracked.string('sisCone5GenJets'),
        flavorMatchingByReferenceName = cms.untracked.string('GenSC5byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        fillerType                    = cms.untracked.string('FillerGenJets')
    ),  
                             
    SC7GenJets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('SC7GenJets'),
        edmName                       = cms.untracked.string('sisCone7GenJets'),
        flavorMatchingByReferenceName = cms.untracked.string('GenSC7byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        fillerType                    = cms.untracked.string('FillerGenJets')
    ),  
    
    KT4GenJets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('KT4GenJets'),
        edmName                       = cms.untracked.string('kt4GenJets'),
        flavorMatchingByReferenceName = cms.untracked.string('GenKT4byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        fillerType                    = cms.untracked.string('FillerGenJets')
    ), 

    KT6GenJets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('KT6GenJets'),
        edmName                       = cms.untracked.string('kt6GenJets'),
        flavorMatchingByReferenceName = cms.untracked.string('GenKT6byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        fillerType                    = cms.untracked.string('FillerGenJets')
    ),     

    ItrCone5Jets = cms.untracked.PSet(
        active                                 = cms.untracked.bool(True),
        flavorMatchingActive                   = cms.untracked.bool(False),
        bTaggingActive                         = cms.untracked.bool(True),
        jetToVertexActive                      = cms.untracked.bool(False),
        jetCorrectionsActive                   = cms.untracked.bool(False),
        mitName                                = cms.untracked.string('ItrCone5Jets'),
        edmName                                = cms.untracked.string('iterativeCone5CaloJets'),
        jetToVertexAlphaName                   = cms.untracked.string('jetVertexAlphaIC5:Var'),
        jetToVertexBetaName                    = cms.untracked.string('jetVertexBetaIC5:Var'),
        L2JetCorrectorName                     = cms.untracked.string('L2RelativeJetCorrectorIC5Calo'),
        L3JetCorrectorName                     = cms.untracked.string('L3AbsoluteJetCorrectorIC5Calo'),
        flavorMatchingByReferenceName          = cms.untracked.string('IC5byRef'),
        flavorMatchingDefinition               = cms.untracked.string('Algorithmic'),
        JetProbabilityBJetTagsName             = cms.untracked.string('jetProbabilityBJetTags'),
        JetBProbabilityBJetTagsName            = cms.untracked.string('jetBProbabilityBJetTags'),
        SimpleSecondaryVertexBJetTagsName      = cms.untracked.string('simpleSecondaryVertexBJetTags'),
        CombinedSecondaryVertexBJetTagsName    = cms.untracked.string('combinedSecondaryVertexBJetTags'),
        CombinedSecondaryVertexMVABJetTagsName = cms.untracked.string('combinedSecondaryVertexMVABJetTags'),
        ImpactParameterMVABJetTagsName         = cms.untracked.string('impactParameterMVABJetTags'),
        TrackCountingHighEffBJetTagsName       = cms.untracked.string('trackCountingHighEffBJetTags'),
        TrackCountingHighPurBJetTagsName       = cms.untracked.string('trackCountingHighPurBJetTags'),
        SoftMuonBJetTagsName                   = cms.untracked.string('softMuonBJetTags'),
        SoftMuonNoIPBJetTagsName               = cms.untracked.string('softMuonNoIPBJetTags'),
        SoftElectronBJetTagsName               = cms.untracked.string('softElectronBJetTags'),        
        caloTowerMapName                       = cms.untracked.string('CaloTowerMap'),
        fillerType                             = cms.untracked.string('FillerCaloJets')
    ),

    SisCone5Jets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        bTaggingActive                = cms.untracked.bool(False),
        jetToVertexActive             = cms.untracked.bool(False),
        jetCorrectionsActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('SisCone5Jets'),
        edmName                       = cms.untracked.string('sisCone5CaloJets'),
        jetToVertexAlphaName          = cms.untracked.string('jetVertexAlphaSC5:Var'),
        jetToVertexBetaName           = cms.untracked.string('jetVertexBetaSC5:Var'),
        L2JetCorrectorName            = cms.untracked.string('L2RelativeJetCorrectorSC5Calo'),
        L3JetCorrectorName            = cms.untracked.string('L3AbsoluteJetCorrectorSC5Calo'),
        flavorMatchingByReferenceName = cms.untracked.string('SC5byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        caloTowerMapName              = cms.untracked.string('CaloTowerMap'),
        fillerType                    = cms.untracked.string('FillerCaloJets')
    ),                          

    SisCone7Jets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        bTaggingActive                = cms.untracked.bool(False),
        jetToVertexActive             = cms.untracked.bool(False),
        jetCorrectionsActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('SisCone7Jets'),
        edmName                       = cms.untracked.string('sisCone7CaloJets'),
        jetToVertexAlphaName          = cms.untracked.string('jetVertexAlphaSC7:Var'),
        jetToVertexBetaName           = cms.untracked.string('jetVertexBetaSC7:Var'),
        L2JetCorrectorName            = cms.untracked.string('L2RelativeJetCorrectorSC7Calo'),
        L3JetCorrectorName            = cms.untracked.string('L3AbsoluteJetCorrectorSC7Calo'),
        flavorMatchingByReferenceName = cms.untracked.string('SC7byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        caloTowerMapName              = cms.untracked.string('CaloTowerMap'),
        fillerType                    = cms.untracked.string('FillerCaloJets')
    ),

    Kt4Jets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        bTaggingActive                = cms.untracked.bool(False),
        jetToVertexActive             = cms.untracked.bool(False),
        jetCorrectionsActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('Kt4Jets'),
        edmName                       = cms.untracked.string('kt4CaloJets'),
        jetToVertexAlphaName          = cms.untracked.string('jetVertexAlphaKT4:Var'),
        jetToVertexBetaName           = cms.untracked.string('jetVertexBetaKT4:Var'),
        L2JetCorrectorName            = cms.untracked.string('L2RelativeJetCorrectorKT4Calo'),
        L3JetCorrectorName            = cms.untracked.string('L3AbsoluteJetCorrectorKT4Calo'),
        flavorMatchingByReferenceName = cms.untracked.string('KT4byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        caloTowerMapName              = cms.untracked.string('CaloTowerMap'),
        fillerType                    = cms.untracked.string('FillerCaloJets')
    ),

    Kt6Jets = cms.untracked.PSet(
        active                        = cms.untracked.bool(True),
        flavorMatchingActive          = cms.untracked.bool(False),
        bTaggingActive                = cms.untracked.bool(False),
        jetToVertexActive             = cms.untracked.bool(False),
        jetCorrectionsActive          = cms.untracked.bool(False),
        mitName                       = cms.untracked.string('Kt6Jets'),
        edmName                       = cms.untracked.string('kt6CaloJets'),
        jetToVertexAlphaName          = cms.untracked.string('jetVertexAlphaKT6:Var'),
        jetToVertexBetaName           = cms.untracked.string('jetVertexBetaKT6:Var'),
        L2JetCorrectorName            = cms.untracked.string('L2RelativeJetCorrectorKT6Calo'),
        L3JetCorrectorName            = cms.untracked.string('L3AbsoluteJetCorrectorKT6Calo'),
        flavorMatchingByReferenceName = cms.untracked.string('KT6byRef'),
        flavorMatchingDefinition      = cms.untracked.string('Algorithmic'),
        caloTowerMapName              = cms.untracked.string('CaloTowerMap'),
        fillerType                    = cms.untracked.string('FillerCaloJets')
    ),

    IC5JetPlusTrack = cms.untracked.PSet(
        active               = cms.untracked.bool(False),
        flavorMatchingActive = cms.untracked.bool(False),
        bTaggingActive       = cms.untracked.bool(False),
        jetToVertexActive    = cms.untracked.bool(False),
        jetCorrectionsActive = cms.untracked.bool(False),
        mitName              = cms.untracked.string('IC5JetPlusTrack'),
        edmName              = cms.untracked.string('JetPlusTrackZSPCorJetIcone5'),
        L2JetCorrectorName   = cms.untracked.string('L2RelativeJetCorrectorIC5JPT'),
        L3JetCorrectorName   = cms.untracked.string('L3AbsoluteJetCorrectorIC5JPT'),
        caloTowerMapName     = cms.untracked.string('CaloTowerMap'),
        fillerType           = cms.untracked.string('FillerCaloJets')
    ),                               
    
    ItrCone5Met = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('ItrCone5Met'),
        edmName    = cms.untracked.string('corMetType1Icone5'),
        fillerType = cms.untracked.string('FillerCaloMet')
    ),
    
    SisCone5Met = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('SisCone5Met'),
        edmName    = cms.untracked.string('corMetType1Scone5'),
        fillerType = cms.untracked.string('FillerCaloMet')
    ),

    SisCone7Met = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('SisCone7Met'),
        edmName    = cms.untracked.string('corMetType1Scone7'), 
        fillerType = cms.untracked.string('FillerCaloMet')
    ),  
    
    Kt4Met = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('Kt4Met'),
        edmName    = cms.untracked.string('corMetType1Kt4'),
        fillerType = cms.untracked.string('FillerCaloMet')
    ),

    Kt6Met = cms.untracked.PSet(
        active     = cms.untracked.bool(True),
        mitName    = cms.untracked.string('Kt6Met'),
        edmName    = cms.untracked.string('corMetType1Kt6'),
        fillerType = cms.untracked.string('FillerCaloMet')
    ),     
                  
    StableParts = cms.untracked.PSet(
        active       = cms.untracked.bool(False),
        mitName      = cms.untracked.string('MuonsStable'),
        edmName      = cms.untracked.string('MuonsStable'),
        trackMapName = cms.untracked.string('TracksMapName'),
        basePartMap  = cms.untracked.string('MuonsStableMapName'),
        fillerType   = cms.untracked.string('FillerStableParts')
    ),

    DecayParts = cms.untracked.PSet(
        active       = cms.untracked.bool(False),
        mitName      = cms.untracked.string('Jpsi2MuMu'),
        edmName      = cms.untracked.string('Jpsi2MuMu'),
        basePartMaps = cms.untracked.vstring('MuonsStableMapName'),
        fillerType   = cms.untracked.string('FillerDecayParts')
    )                                                            
)
   
