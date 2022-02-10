#include "TTree.h"
#include "TFile.h"
#include <vector>
#include <chrono>

void pythia8(Int_t nev  = 100)
{

  auto start = std::chrono::high_resolution_clock::now();

  // Load libraries
  //gSystem->Load("pythia/lib/libpythia8.so");
  //gSystem->Load("pythia/examples/main92.so");
  //gSystem->Load("libEG");
  //gSystem->Load("libEGPythia8");

  // Create pythia8 object
  Pythia8::Pythia *pythia8 = new Pythia8::Pythia();

  // File
  TFile* file = TFile::Open("pytree.root","recreate");

  // Prepare Tree

  Int_t np;
  std::vector<Int_t> id;
  std::vector<Int_t> status;
  std::vector<Float_t> e;
  std::vector<Float_t> m;
  std::vector<Float_t> pt;
  std::vector<Float_t> phi;
  std::vector<Float_t> eta;
  
  TTree* tree = new TTree("tree","tree");
  auto np_branch = tree->Branch("np",&np);
  auto id_branch = tree->Branch("id",&id);
  auto status_branch = tree->Branch("status",&status);
  auto e_branch = tree->Branch("e",&e);
  auto m_branch = tree->Branch("m",&m);
  auto pt_branch = tree->Branch("pt",&pt);
  auto phi_branch = tree->Branch("phi",&phi);
  auto eta_branch = tree->Branch("eta",&eta);

  // Configure
  //pythia8->readString("HardQCD:all = on");
  //pythia8->readString("HiggsSM:gg2H = on");
  // pythia8->readString("25:onMode = off");
  // pythia8->readString("25:onIfAll= 11 -11");
  // pythia8->readString("Random:setSeed = on");
  // use a reproducible seed: always the same results for the tutorial.
  // pythia8->readString("Random:seed = 42");

  pythia8->readString("Beams:eCM = 13000.");
  pythia8->readString("Top:gg2ttbar = on");
  pythia8->readString("Top:qqbar2ttbar = on");
  // pythia8->readString("PartonLevel:FSR = off");
  // pythia8->readString("PartonLevel:ISR = off");
  // pythia8->readString("PartonLevel:MPI = off");
  // pythia8->readString("HadronLevel:all = off");
  // pythia8->readString("PartonLevel:all = off");

  // Initialize

  //pythia8->init(2212 /* p */, 2212 /* p */, 14000. /* TeV */);
  pythia8->init();

  // Event loop
  for (Int_t iev = 0; iev < nev; iev++) {

    status.clear();
    id.clear();
    e.clear();
    m.clear();
    pt.clear();
    phi.clear();
    eta.clear();

    pythia8->next();

    np = pythia8->event.size();

    //    std::cout << "Event Nr.: " << iev << std::endl;
    //    std::cout << "Nr. of Particles: " << np << std::endl;

    //Particle loop
    for (Int_t ip = 0; ip < np; ip++) {
      status.push_back(pythia8->event[ip].status());
      id.push_back(pythia8->event[ip].id());
      e.push_back(pythia8->event[ip].e());
      m.push_back(pythia8->event[ip].m());
      pt.push_back(pythia8->event[ip].pT());
      phi.push_back(pythia8->event[ip].phi());
      eta.push_back(pythia8->event[ip].eta());
    }

    tree->Fill();

  }

  pythia8->stat();

  tree->Print();
  tree->Write();
  delete file;

  auto stop = std::chrono::high_resolution_clock::now();
  auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);
  std::cout << duration.count() << std::endl;

}
