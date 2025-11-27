#!/usr/bin/env python3
import subprocess
import shlex

HOST = "root://eospublic.cern.ch/"
DIR = (
    "/eos/opendata/cms/datascience/HiggsToBBNtupleProducerTool/"
    "HiggsToBBNTuple_HiggsToBB_QCD_RunII_13TeV_MC/train"
)


def run(cmd: str) -> str:
    """Run a shell command and return stdout as text."""
    print(f"$ {cmd}")
    out = subprocess.check_output(shlex.split(cmd), text=True)
    return out


def list_files():
    """List all files in DIR on EOS via xrdfs."""
    output = run(f"xrdfs {HOST} ls {DIR}")
    files = [line.strip() for line in output.splitlines() if line.strip()]
    return files


def stat_size(remote_path: str) -> int:
    """Return file size in bytes using xrdfs stat."""
    output = run(f"xrdfs {HOST} stat {remote_path}")
    size = None
    for line in output.splitlines():
        line = line.strip()
        if line.lower().startswith("size:"):
            # Expect something like: "Size: 123456789"
            parts = line.split()
            size = int(parts[1])
            break
    if size is None:
        raise RuntimeError(f"Could not parse size for {remote_path}")
    return size


def main():
    files = list_files()
    print(f"\nFound {len(files)} files in {DIR}\n")

    total_size = 0
    per_file = []

    for path in files:
        sz = stat_size(path)
        total_size += sz
        per_file.append((path, sz))
        print(f"{path}  {sz/1e6:.2f} MB")

    print("\n=== Summary ===")
    print(f"File count: {len(per_file)}")
    print(f"Total size: {total_size/1e9:.3f} GB")
    if per_file:
        avg = total_size / len(per_file)
        print(f"Average file size: {avg/1e6:.2f} MB")


if __name__ == "__main__":
    main()
