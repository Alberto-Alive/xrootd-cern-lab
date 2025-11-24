# xrootd-cern-lab 🧪
Hands-on exercises using the XRootD CLI (`xrdfs`, `xrdcp`) against CERN’s EOS storage via the public `eospublic.cern.ch` endpoint.   Goal: explore, learn and understand how XRootD powers data access at CERN and across the Worldwide LHC Computing Grid.



## Progress Checklist 📊

What I’ve explored so far in this lab.

### XRootD & EOS basics
- [x] Install XRootD client tools (`xrdfs`, `xrdcp`)
- [] Connect to `root://eospublic.cern.ch//`
- [] List directories under `/eos/opendata`
- [] Inspect file metadata with `xrdfs stat`
- [] Copy a ROOT file locally with `xrdcp`

### Data access & analysis
- [] Open a ROOT file via `root://` in ROOT or Python
- [ ] Compare local vs remote read performance
- [ ] Script basic dataset summary (sizes, file counts)

### Monitoring / “CERN job-related” extras
- [ ] Time multiple `xrdcp` runs and log throughput
- [ ] Parse CLI logs into a small CSV/JSON
- [ ] Visualise transfer stats in a simple plot/Grafana panel
- [ ] Note common error codes and failure modes

### Future ideas
- [ ] Explore XCache / caching behaviour (if accessible)
- [ ] Try authenticated access (X.509 or tokens) in a test setup
