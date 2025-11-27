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
- [x] Compare local vs remote read performance
- [x] Script basic dataset summary (sizes, file counts)

### Monitoring / “CERN job-related” extras
- [x] Time multiple `xrdcp` runs and log throughput
- [x] Parse CLI logs into a small CSV/JSON
- [x] Visualise transfer stats in a simple plot/Grafana panel
- [x] Note common error codes and failure modes

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



### Dataset Summary

```text
=== Summary ===
File count: 165
Total size: 220.457 GB
Average file size: 1336.10 MB
```


### xrdcp timing and throughput

I ran `xrdcp` three times on the ~1.128 GB file and logged start/end times
to `xrdcp_runs.log`. Parsed with `xrdcp_parse_logs.py`, the effective
throughput was:

- Run 1: ~0.57 MB/s  (~33 min)
- Run 2: ~0.65 MB/s  (~29 min)
- Run 3: ~20.5 MB/s  (~55 s)

The large jump on the third run shows how much variability there can be in
end-to-end data transfer (WAN path, caches, load, etc.). A real monitoring
system would track these distributions over time and per site, not just
single averages.


### Common `xrdcp` / XRootD failure modes

As part of this lab I deliberately triggered a few failures and noted the
messages + exit codes.

#### 1. Missing file (wrong EOS path)

```bash
xrdcp root://eospublic.cern.ch//eos/opendata/cms/this/does/not/exist.root ./bad.root
echo "exit code: $?"
```