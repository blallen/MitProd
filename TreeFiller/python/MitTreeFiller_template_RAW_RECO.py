#---------------------------------------------------------------------------------------------------
# This template config file is intended to be a reference for the "HEAD" OAK tree version.
# This config file will be used by the mitprod account to do production on CRAB. It must
# be ensured that this config file is always working with the production CMSSW release
#---------------------------------------------------------------------------------------------------
# List of paramters to be properly replaced
#
#  - XX-MITDATASET-XX - MIT type dataset name (ex. csa08-1ipb-jpsi)
#
#---------------------------------------------------------------------------------------------------

import FWCore.ParameterSet.Config as cms
process = cms.Process("FILLER")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)
#process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring(
   #'file:/server/02a/bendavid/RECO/0079F3C0-AF75-DD11-8EF5-003048772390.root'
                             #),
                            #secondaryFileNames = cms.untracked.vstring(
   #'file:/server/02a/bendavid/RAW/10A05094-446F-DD11-B8F3-00304865C360.root'
                             #),
#)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
   'file:/server/02a/sixie/RECO/001EA63A-DF60-DD11-9D5A-001A92810AA6.root'
                             ),
                            secondaryFileNames = cms.untracked.vstring()
)

# compute ECAL shower shape variables
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load("Configuration.StandardSequences.Geometry_cff")

process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/Digi_cff')
process.load('Configuration/StandardSequences/MixingNoPileUp_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

process.GlobalTag.globaltag = 'IDEAL_V6::All'


process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.load( "RecoEgamma.ElectronIdentification.electronIdCutBased_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdCutBasedClasses_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdLikelihood_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdNeuralNet_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdCutBasedExt_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdCutBasedClassesExt_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdLikelihoodExt_cfi")
process.load( "RecoEgamma.ElectronIdentification.electronIdNeuralNetExt_cfi")

# process.load("SimGeneral.TrackingAnalysis.trackingParticles_cfi")




process.eIdSequence = cms.Sequence( process.eidCutBased +
                                    process.eidCutBasedExt +
                                    process.eidCutBasedClasses +
                                    process.eidCutBasedClassesExt +
                                    process.eidLikelihood +
                                    process.eidLikelihoodExt + 
                                    process.eidNeuralNet +
                                    process.eidNeuralNetExt)

process.load("MitProd.TreeFiller.JetsMCFlavourMatching_cfi")

process.TreeService = cms.Service("TreeService",
    fileNames = cms.untracked.vstring('mit-match')
)

process.add_(cms.Service("ObjectService"))

process.load("MitProd.TreeFiller.MitPostRecoGenerator_cff")
process.load("MitProd.TreeFiller.MitTreeFiller_RAW_RECO_cfi")

process.p1 = cms.Path(process.pdigi * process.mit_postreco_generator * (process.caloJetMCFlavour + process.eIdSequence) * process.MitTreeFiller)
# process.p1 = cms.Path((process.caloJetMCFlavour + process.eIdSequence)*process.MitTreeFiller)