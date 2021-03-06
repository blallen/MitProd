# $Id: vProducerNoRefit_cff.py,v 1.3 2009/07/20 05:04:20 loizides Exp $

import FWCore.ParameterSet.Config as cms

import MitEdm.Producers.stableParts_cfi

PisStable = MitEdm.Producers.stableParts_cfi.stableParts.clone()

ProtonsStable = MitEdm.Producers.stableParts_cfi.stableParts.clone()
ProtonsStable.oPid = cms.untracked.int32(2212)

import MitEdm.Producers.v2ss_cfi
Ksh2PiPi = MitEdm.Producers.v2ss_cfi.v2ss.clone()
Ksh2PiPi.useHitDropper = cms.untracked.bool(False)

Lambda2ProtPi = MitEdm.Producers.v2ss_cfi.v2ss.clone()
Lambda2ProtPi.iStables2 = cms.untracked.string('ProtonsStable')
Lambda2ProtPi.oPid = cms.untracked.int32(3122)
Lambda2ProtPi.minMass = cms.untracked.double(1.0)
Lambda2ProtPi.maxMass = cms.untracked.double(1.3)
Lambda2ProtPi.useHitDropper = cms.untracked.bool(False)

vProducer = cms.Sequence(PisStable*ProtonsStable*Ksh2PiPi*Lambda2ProtPi)

def addKshFiller(filler):

    filler.fillers.extend(('PisStable',
                           'Ksh2PiPi'))

    filler.PisStable = cms.untracked.PSet(
        active       = cms.untracked.bool(True),
        mitName      = cms.untracked.string('PisStable'),
        edmName      = cms.untracked.string('PisStable'),
        trackMapNames = cms.untracked.vstring('TracksMapName'),
        basePartMap  = cms.untracked.string('PisStableMapName'),
        fillerType   = cms.untracked.string('FillerStableParts')
    )

    filler.Ksh2PiPi = cms.untracked.PSet(
        active       = cms.untracked.bool(True),
        mitName      = cms.untracked.string('Ksh2PiPi'),
        edmName      = cms.untracked.string('Ksh2PiPi'),
        basePartMaps = cms.untracked.vstring('PisStableMapName'),
        fillerType   = cms.untracked.string('FillerDecayParts')
    )

def addLambdaFiller(filler):

    filler.fillers.extend(('ProtonsStable',
                           'Lambda2ProtPi'))

    filler.ProtonsStable = cms.untracked.PSet(
        active        = cms.untracked.bool(True),
        mitName       = cms.untracked.string('ProtonsStable'),
        edmName       = cms.untracked.string('ProtonsStable'),
        trackMapNames = cms.untracked.vstring('TracksMapName'),
        basePartMap   = cms.untracked.string('ProtonsStableMapName'),
        fillerType    = cms.untracked.string('FillerStableParts')
    )

    filler.Lambda2ProtPi = cms.untracked.PSet(
        active       = cms.untracked.bool(True),
        mitName      = cms.untracked.string('Lambda2ProtPi'),
        edmName      = cms.untracked.string('Lambda2ProtPi'),
        basePartMaps = cms.untracked.vstring('PisStableMapName','ProtonsStableMapName'),
        fillerType   = cms.untracked.string('FillerDecayParts')
    )

def addVFiller(filler):
    addKshFiller(filler)
    addLambdaFiller(filler)
