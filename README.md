# xrootd-cern-lab 🧪
Hands-on exercises using the XRootD CLI (`xrdfs`, `xrdcp`) against CERN’s EOS storage via the public `eospublic.cern.ch` endpoint.   Goal: explore, learn and understand how XRootD powers data access at CERN and across the Worldwide LHC Computing Grid.



## Progress Checklist 📊

What I’ve explored so far in this lab.

### XRootD & EOS basics
- [x] Install XRootD client tools (`xrdfs`, `xrdcp`)
- [x] Connect to `root://eospublic.cern.ch//`
- [x] List directories under `/eos/opendata`
- [x] Inspect file metadata with `xrdfs stat`
- [x] Copy a ROOT file locally with `xrdcp`

### Data access & analysis
- [x] Open a ROOT file via `root://` in ROOT
- [] Compare local vs remote read performance
- [] Script basic dataset summary (sizes, file counts)

### Monitoring / “CERN job-related” extras
- [] Time multiple `xrdcp` runs and log throughput
- [] Parse CLI logs into a small CSV/JSON
- [] Visualise transfer stats in a simple plot/Grafana panel
- [] Note common error codes and failure modes

### Future ideas
- [] Explore XCache / caching behaviour (if accessible)
- [] Try authenticated access (X.509 or tokens) in a test setup


## Environment

- OS: <your distro here> (e.g. Ubuntu 22.04)
- XRootD client: `xrootd-client` from system packages
- Verify install:
- Abbrev: xrdfs = XRootD Remote Distributed File System (DFS) client
```bash
xrdfs --help | head
xrdcp --help | head
```



## EOS directory listing

Using the XRootD client from WSL (Ubuntu):

```bash
# List top-level on the EOS public instance
xrdfs root://eospublic.cern.ch/ ls /

# List the EOS namespace
xrdfs root://eospublic.cern.ch/ ls /eos

# List CERN Open Data area
xrdfs root://eospublic.cern.ch/ ls /eos/opendata
```

### Comparing local vs remote read performance in ROOT

Using the same TTree (`deepntuplizer/tree`), I timed opening the file and reading
the first 100k entries with a simple `GetEntry(i)` loop and `TStopwatch`.

`time_read.C` results (WSL, home network, cold cache):

| Access mode         | Open time (s) | Read time real (s) | Read time CPU (s) | Entries read |
|---------------------|--------------:|--------------------:|-------------------:|-------------:|
| Local file (`file://`)  |     0.005    |        6.93         |        3.49        |     100k     |
| Remote XRootD (`root://`)|     1.17     |      526.77         |        4.07        |     100k     |

Observations:

- Opening over XRootD takes ~1.2 s vs ~5 ms locally (network + handshake).
- CPU time to process 100k entries is similar for local and remote (~3.5–4 s),
  but the **real** time over XRootD is ~500 s because the process spends most of
  the time waiting on remote I/O.
- This illustrates how naive event-by-event reading over WAN is very slow
  without caching/batching, and why XRootD caching (XCache) and optimised
  read patterns are important in WLCG production.

