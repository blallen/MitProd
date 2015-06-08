import FWCore.ParameterSet.Config as cms
from RecoBTag.Configuration.RecoBTag_cff import *

def setupBTag(process, jetCollection, suffix):
    """
    Configure the BTag sequence for the given jet collection.
    EDM module names will be accompanied by the suffix to
    distinguish sequences for multiple collections.
    """

    # tag info
    ipTagInfosName = 'pfImpactParameterTagInfos' + suffix
    svTagInfosName = 'pfSecondaryVertexTagInfos' + suffix
    ivfTagInfosName = 'pfInclusiveSecondaryVertexFinderTagInfos' + suffix
    smTagInfosName = 'softPFMuonsTagInfos' + suffix
    seTagInfosName = 'softPFElectronsTagInfos' + suffix

    newImpactParameterTagInfos = pfImpactParameterTagInfos.clone(
        jets = jetCollection
    )
    newSecondaryVertexTagInfos = pfSecondaryVertexTagInfos.clone(
        trackIPTagInfos = ipTagInfosName
    )
    newInclusiveSecondaryVertexFinderTagInfos = pfInclusiveSecondaryVertexFinderTagInfos.clone(
        trackIPTagInfos = ipTagInfosName
    )
    newSoftPFMuonsTagInfos = softPFMuonsTagInfos.clone(
        jets = jetCollection
    )
    newSoftPFElectronsTagInfos = softPFElectronsTagInfos.clone(
        jets = jetCollection
    )

    # impact parameter b-tags
    newTrackCountingHighEffBJetTags = pfTrackCountingHighEffBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(ipTagInfosName))
    )
    newTrackCountingHighPurBJetTags = pfTrackCountingHighPurBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(ipTagInfosName))
    )

    # jet probability b-tags
    newJetProbabilityBJetTags = pfJetProbabilityBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(ipTagInfosName))
    )
    newJetBProbabilityBJetTags = pfJetBProbabilityBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(ipTagInfosName))
    )

    # secondary vertex b-tags
    newSimpleSecondaryVertexHighEffBJetTags = pfSimpleSecondaryVertexHighEffBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(svTagInfosName))
    )
    newSimpleSecondaryVertexHighPurBJetTags = pfSimpleSecondaryVertexHighPurBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(svTagInfosName))
    )

    # combined secondary vertex b-tags
    newCombinedSecondaryVertexBJetTags = pfCombinedSecondaryVertexBJetTags.clone(
        tagInfos = cms.VInputTag(
            cms.InputTag(ipTagInfosName),
            cms.InputTag(svTagInfosName)
        )
    )
    newCombinedSecondaryVertexV2BJetTags = pfCombinedSecondaryVertexV2BJetTags.clone(
        tagInfos = cms.VInputTag(
            cms.InputTag(ipTagInfosName),
            cms.InputTag(svTagInfosName)
        )
    )

    # inclusive combined secondary vertex b-tags
    newCombinedInclusiveSecondaryVertexV2BJetTags = pfCombinedInclusiveSecondaryVertexV2BJetTags.clone(
        tagInfos = cms.VInputTag(
            cms.InputTag(ipTagInfosName),
            cms.InputTag(ivfTagInfosName)
        )
    )

    # soft lepton b-tags
    newSoftPFMuonBJetTags = softPFMuonBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(smTagInfosName))
    )
    newSoftPFElectronBJetTags = softPFElectronBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag(seTagInfosName))
    )

    # super-combined b-tags
    newCombinedMVABJetTags = pfCombinedMVABJetTags.clone(
        tagInfos = cms.VInputTag(
            cms.InputTag(ipTagInfosName),
            cms.InputTag(ivfTagInfosName),
            cms.InputTag(smTagInfosName),
            cms.InputTag(seTagInfosName)
        )
    )
    newCombinedSecondaryVertexSoftLeptonBJetTags = pfCombinedSecondaryVertexSoftLeptonBJetTags.clone(
        tagInfos = cms.VInputTag(
            cms.InputTag(ipTagInfosName),
            cms.InputTag(ivfTagInfosName),
            cms.InputTag(smTagInfosName),
            cms.InputTag(seTagInfosName)
        )
    )

    # sequence
    sequence = cms.Sequence(
        (
            newImpactParameterTagInfos *
            (
                newTrackCountingHighEffBJetTags +
                newTrackCountingHighPurBJetTags +
                newJetProbabilityBJetTags +
                newJetBProbabilityBJetTags +
                newSecondaryVertexTagInfos *
                (
                    newSimpleSecondaryVertexHighEffBJetTags +
                    newSimpleSecondaryVertexHighPurBJetTags +
                    newCombinedSecondaryVertexBJetTags +
                    newCombinedSecondaryVertexV2BJetTags
                ) +
                inclusiveCandidateVertexing *
                newInclusiveSecondaryVertexFinderTagInfos *
                newCombinedInclusiveSecondaryVertexV2BJetTags
            ) +
            newSoftPFMuonsTagInfos *
#            newSoftPFMuonBJetTags +
            newSoftPFElectronsTagInfos #*
#            newSoftPFElectronBJetTags
        ) *
        (
            newCombinedMVABJetTags +
            newCombinedSecondaryVertexSoftLeptonBJetTags
        )
    )

    # configure process
    # add candidate vertexing (might be a repeat but no problem)
    process.load('RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff')

    # add tag info calculators
    setattr(process, ipTagInfosName, newImpactParameterTagInfos)
    setattr(process, svTagInfosName, newSecondaryVertexTagInfos)
    setattr(process, ivfTagInfosName, newInclusiveSecondaryVertexFinderTagInfos)
    setattr(process, smTagInfosName, newSoftPFMuonsTagInfos)
    setattr(process, seTagInfosName, newSoftPFElectronsTagInfos)

    # add btag calculators
    setattr(process, 'trackCountingHighEffBJetTags' + suffix, newTrackCountingHighEffBJetTags)
    setattr(process, 'trackCountingHighPurBJetTags' + suffix, newTrackCountingHighPurBJetTags)
    setattr(process, 'jetProbabilityBJetTags' + suffix, newJetProbabilityBJetTags)
    setattr(process, 'jetBProbabilityBJetTags' + suffix, newJetBProbabilityBJetTags)
    setattr(process, 'simpleSecondaryVertexHighEffBJetTags' + suffix, newSimpleSecondaryVertexHighEffBJetTags)
    setattr(process, 'simpleSecondaryVertexHighPurBJetTags' + suffix, newSimpleSecondaryVertexHighPurBJetTags)
    setattr(process, 'combinedSecondaryVertexBJetTags' + suffix, newCombinedSecondaryVertexBJetTags)
    setattr(process, 'combinedSecondaryVertexV2BJetTags' + suffix, newCombinedSecondaryVertexV2BJetTags)
    setattr(process, 'combinedInclusiveSecondaryVertexV2BJetTags' + suffix, newCombinedInclusiveSecondaryVertexV2BJetTags)
    setattr(process, 'softPFMuonBJetTags' + suffix, newSoftPFMuonBJetTags)
    setattr(process, 'softPFElectronBJetTags' + suffix, newSoftPFElectronBJetTags)
    setattr(process, 'combinedMVABJetTags' + suffix, newCombinedMVABJetTags)
    setattr(process, 'combinedSecondaryVertexSoftLeptonBJetTags' + suffix, newCombinedSecondaryVertexSoftLeptonBJetTags)

    # finally add sequence
    setattr(process, 'pfBTagging' + suffix, sequence)
    
    return sequence
