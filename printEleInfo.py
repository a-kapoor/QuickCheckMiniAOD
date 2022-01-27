# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons" 



# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
events = Events("root://xrootd-cms.infn.it///store/data/Run2016C/DoubleEG/MINIAOD/HIPM_UL2016_MiniAODv2-v1/130000/63CA2FE2-BC70-4449-9D74-ED06732DEC7C.root")

for iev,event in enumerate(events):
    print("\nEvent", iev)
    event.getByLabel(electronLabel, electrons)
    #print f'\nEvent {iev}: run {event.eventAuxiliary().run()}, lumi {event.eventAuxiliary().luminosityBlock()}, event {event.eventAuxiliary().event()}'
    print("\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event()))
        # Electrons
    for i,el in enumerate(electrons.product()):
        if el.pt() < 5: continue
        print("elec %2d: pt %4.6f, supercluster eta %+5.3f, sigmaIetaIeta %.3f (%.3f with full5x5 shower shapes), lost hits %d, pass conv veto %d" % (
                    i, el.pt(), el.superCluster().eta(), el.sigmaIetaIeta(), el.full5x5_sigmaIetaIeta(),el.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS), el.passConversionVeto()))

    if iev > 10000: break
