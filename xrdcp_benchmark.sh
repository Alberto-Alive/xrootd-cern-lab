#!/usr/bin/env bash
set -euo pipefail

URL="root://eospublic.cern.ch//eos/opendata/cms/datascience/HiggsToBBNtupleProducerTool/HiggsToBBNTuple_HiggsToBB_QCD_RunII_13TeV_MC/train/ntuple_merged_10.root"
DEST="ntuple_merged_10.root"
LOG="xrdcp_runs.log"

echo "# xrdcp benchmark runs" > "$LOG"

for run in {1..1}; do
  echo "Run $run..."
  start=$(date +%s)
  xrdcp -f "$URL" "$DEST"
  end=$(date +%s)
  duration=$((end - start))
  echo "run=$run start=$start end=$end duration=$duration" | tee -a "$LOG"
done
