import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.register('skipEvents', 
    default=0, 
    mult=VarParsing.VarParsing.multiplicity.singleton,
    mytype=VarParsing.VarParsing.varType.int,
    info = "skipEvents")
options.parseArguments()

process = cms.Process("FEVTAnalyzer")

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("DQM.Integration.config.FrontierCondition_GT_Offline_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
#process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
#process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi");
#process.load("Geometry.CaloEventSetup.CaloGeometry_cfi");
#process.load("Geometry.CaloEventSetup.CaloTopology_cfi");
process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet( 
    #input = cms.untracked.int32(1) 
    input = cms.untracked.int32(options.maxEvents) 
    )

print " >> Loaded",len(options.inputFiles),"input files from list."
process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
      #'file:myfile.root'
      #'file:pickevents.root'
      #'file:pickeventsRECO.root'
      #'file:step3.root'
      #'file:SinglePhotonPt50_FEVTDEBUG.root'
      #'file:SingleElectronPt50_FEVTDEBUG.root'
      #'file:/eos/uscms/store/user/mba2012/FEVTDEBUG/H125GGgluonfusion_13TeV_TuneCUETP8M1_FEVTDEBUG/*/*/step_full_*.root'
      options.inputFiles
      )
    , skipEvents = cms.untracked.uint32(options.skipEvents)
    )

process.GlobalTag.globaltag = cms.string('80X_dataRun2_HLT_v12')
process.es_prefer_GlobalTag = cms.ESPrefer('PoolDBESSource','GlobalTag')

process.fevt = cms.EDAnalyzer('SCAnalyzer'
    #, EBRecHitCollection = cms.InputTag('ecalRecHit:EcalRecHitsEB')
    , gsfElectronCollection = cms.InputTag('gedGsfElectrons')
    , gedPhotonCollection = cms.InputTag('gedPhotons')
    , reducedEBRecHitCollection = cms.InputTag('reducedEcalRecHitsEB')
    , genParticleCollection = cms.InputTag('genParticles')
    , genJetCollection = cms.InputTag('ak4GenJets')
    )

process.TFileService = cms.Service("TFileService",
    #fileName = cms.string('histo.root')
    fileName = cms.string(options.outputFile)
    )

process.p = cms.Path(process.fevt)
