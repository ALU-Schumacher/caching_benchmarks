#!/usr/bin/env python

import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=str,dest='file_name',default='',help='path to file')
parser.add_argument('-e','--events',type=int,dest='num_events',default=1,help='number of events')

args = parser.parse_args()

ROOT.gROOT.SetBatch(True)

f = ROOT.TFile.Open(args.file_name)
t = f.Get('tree')

hist_mass = ROOT.TH1F('m_inv_ttbar', '', 200, 0, 2500)
hist_eta = ROOT.TH1F('eta', '', 100, -15, 15)

for entry in range(args.num_events):
    t.GetEntry(entry)
    nParticles = t.np
    v = ROOT.Math.PtEtaPhiMVector(0,0,0,0)
    for part in range(0, nParticles):
        hist_eta.Fill(t.eta[part])
        if abs(t.status[part]) == 23:
            v += ROOT.Math.PtEtaPhiMVector(t.pt[part],t.eta[part],t.phi[part],t.m[part])
    print(f"ttbar mass of the event is {v.M()}")
    hist_mass.Fill(v.M())

f.Close()
