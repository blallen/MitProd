# $Id: MitPostRecoGenerator_cff.py,v 1.3 2008/09/28 02:27:52 loizides Exp $

import FWCore.ParameterSet.Config as cms

#track match
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from SimGeneral.TrackingAnalysis.trackingParticles_cfi import *
from SimTracker.TrackAssociation.TrackAssociatorByChi2_cfi import *
from SimTracker.TrackAssociation.TrackAssociatorByHits_cfi import *
TrackAssociatorByHits.Cut_RecoToSim = 0.5
from SimTracker.TrackAssociation.trackMCMatch_cfi import *
#from SimTracker.TrackAssociation.standAloneMuonsMCMatch_cfi import *
#from SimTracker.TrackAssociation.globalMuonsMCMatch_cfi import *
#from SimTracker.TrackAssociation.allTrackMCMatch_cfi import *
from SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cff import *
trackMCMatchSequence = cms.Sequence(trackMCMatch*trackingParticleRecoTrackAsssociation*assoc2GsfTracks*assocOutInConversionTracks*assocInOutConversionTracks)

# define post-reco generator sequence
mit_postreco_generator = cms.Sequence(trackMCMatchSequence)
