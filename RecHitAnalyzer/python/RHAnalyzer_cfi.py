import FWCore.ParameterSet.Config as cms 

fevt = cms.EDAnalyzer('RecHitAnalyzer'
    #, tracks = cms.untracked.InputTag('ctfWithMaterialTracks')
    #, EBRecHitCollection = cms.InputTag('ecalRecHit:EcalRecHitsEB')
    , reducedEBRecHitCollection = cms.InputTag('reducedEcalRecHitsEB')
    #, EERecHitCollection = cms.InputTag('ecalRecHit:EcalRecHitsEE')
    , reducedEERecHitCollection = cms.InputTag('reducedEcalRecHitsEE')
    #, EBDigiCollection = cms.InputTag('simEcalDigis:ebDigis')
    #, selectedEBDigiCollection = cms.InputTag('selectDigi:selectedEcalEBDigiCollection')
    , reducedHBHERecHitCollection = cms.InputTag('reducedHcalRecHits:hbhereco')
    , genParticleCollection = cms.InputTag('genParticles')
    , gedPhotonCollection = cms.InputTag('gedPhotons')
    , ak4PFJetCollection = cms.InputTag('ak4PFJets')
    , genJetCollection = cms.InputTag('ak4GenJets')
    , trackRecHitCollection = cms.InputTag('generalTracks')
    , siPixelRecHitCollection = cms.InputTag('siPixelRecHits')
    , siStripRecHitCollection =  cms.VInputTag(
    cms.InputTag('siStripMatchedRecHits:rphiRecHit'),
    cms.InputTag('siStripMatchedRecHits:stereoRecHit'),
    cms.InputTag('siStripMatchedRecHits:rphiRecHitUnmatched'),
    cms.InputTag('siStripMatchedRecHits:stereoRecHitUnmatched')
    )
    , trackCollection = cms.InputTag("generalTracks")
    , pfCollection = cms.InputTag("particleFlow")
    , mode = cms.string("JetLevel")

    # Jet level cfg
    , nJets = cms.int32(2)
    , minJetPt = cms.double(20.)
    , maxJetEta = cms.double(2.4)

    , granularityMultiPhi = cms.int32(1)
    , granularityMultiEta = cms.int32(1)
    )
