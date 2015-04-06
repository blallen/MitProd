import FWCore.ParameterSet.Config as cms

from RecoJets.Configuration.GenJetParticles_cff import *
from RecoJets.Configuration.RecoGenJets_cff import *

antiktGenJets = cms.Sequence(
  genJetParticles*
  ak4GenJets*
  ak8GenJets
)
