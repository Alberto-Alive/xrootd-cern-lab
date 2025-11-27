// time_read.C
#include "TFile.h"
#include "TTree.h"
#include "TStopwatch.h"
#include "TString.h"
#include <iostream>

void time_read(const char* label,
               const char* filename,
               const char* treepath,
               Long64_t nEntriesToRead = 100000)
{
    std::cout << "\n=== " << label << " ===" << std::endl;
    std::cout << "File: " << filename << std::endl;
    std::cout << "Tree: " << treepath << std::endl;

    TStopwatch sw;

    // Open file
    sw.Start();
    TFile *f = TFile::Open(filename);
    sw.Stop();
    if (!f || f->IsZombie()) {
        std::cerr << "ERROR: Failed to open file\n";
        return;
    }
    std::cout << "Open time: " << sw.RealTime() << " s (real)" << std::endl;

    // Get tree
    TTree *t = nullptr;
    f->GetObject(treepath, t);
    if (!t) {
        std::cerr << "ERROR: Could not find TTree at path " << treepath << "\n";
        f->Close();
        return;
    }

    Long64_t nEntries = t->GetEntries();
    if (nEntriesToRead > nEntries) nEntriesToRead = nEntries;

    std::cout << "Total entries in tree: " << nEntries << std::endl;
    std::cout << "Reading first " << nEntriesToRead << " entries..." << std::endl;

    // Time reading entries
    sw.Reset();
    sw.Start();
    for (Long64_t i = 0; i < nEntriesToRead; ++i) {
        t->GetEntry(i);
    }
    sw.Stop();

    std::cout << "Read time: " << sw.RealTime() << " s (real), "
              << sw.CpuTime() << " s (CPU)" << std::endl;

    f->Close();
}
