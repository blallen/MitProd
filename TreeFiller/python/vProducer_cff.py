# $Id: vProducer_cff.py,v 1.5 2009/07/20 05:04:20 loizides Exp $

import FWCore.ParameterSet.Config as cms

import MitEdm.Producers.stableParts_cfi

PisStable = MitEdm.Producers.stableParts_cfi.stableParts.clone()

from RecoTracker.TrackProducer.TrackRefitters_cff import *

ProtonPropagator = TrackingTools.MaterialEffects.RungeKuttaTrackerPropagator_cfi.RungeKuttaTrackerPropagator.clone()
ProtonPropagator.ComponentName = cms.string('ProtonPropagator')
ProtonPropagator.Mass          = cms.double(0.93827)

TrackRefitter.Propagator = cms.string('ProtonPropagator')

ProtonsStable = MitEdm.Producers.stableParts_cfi.stableParts.clone()
ProtonsStable.iTracks = cms.untracked.string('TrackRefitter')
ProtonsStable.oPid    = cms.untracked.int32(2212)

import MitEdm.Producers.v2ss_cfi
Ksh2PiPi = MitEdm.Producers.v2ss_cfi.v2ss.clone()

Lambda2ProtPi = MitEdm.Producers.v2ss_cfi.v2ss.clone()
Lambda2ProtPi.iStables2 = cms.untracked.string('ProtonsStable')
Lambda2ProtPi.oPid = cms.untracked.int32(3122)
Lambda2ProtPi.minMass = cms.untracked.double(1.05)
Lambda2ProtPi.maxMass = cms.untracked.double(1.18)

# Sequence to produce the particles
kShProducer = cms.Sequence(PisStable*Ksh2PiPi)
lambdaProducer = cms.Sequence(TrackRefitter*ProtonsStable*Lambda2ProtPi)
vProducer = cms.Sequence(kShProducer*lambdaProducer)

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

    filler.fillers.extend(('ProtonRefitTracks',
                           'ProtonsStable',
                           'Lambda2ProtPi'))

    filler.ProtonRefitTracks = cms.untracked.PSet(
        active       = cms.untracked.bool(True),
        mitName      = cms.untracked.string('ProtonRefitTracks'),
        edmName      = cms.untracked.string('TrackRefitter'),
        simMapName   = cms.untracked.string('SimMap'),
        trackMapName = cms.untracked.string('ProtTracksMapName'),
        fillerType   = cms.untracked.string('FillerTracks')
    )

    filler.ProtonsStable = cms.untracked.PSet(
        active       = cms.untracked.bool(True),
        mitName      = cms.untracked.string('ProtonsStable'),
        edmName      = cms.untracked.string('ProtonsStable'),
        trackMapNames = cms.untracked.vstring('ProtTracksMapName'),
        basePartMap  = cms.untracked.string('ProtonsStableMapName'),
        fillerType   = cms.untracked.string('FillerStableParts')
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
