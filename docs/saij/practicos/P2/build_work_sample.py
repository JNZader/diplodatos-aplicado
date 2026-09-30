#!/usr/bin/env python3
"""Stratified SU+FA work sample from full JSONL (not the group's 50%)."""
from __future__ import annotations

import gzip
import json
import random
from pathlib import Path

FULL = Path("/home/javier/programacion/Educacion/DiploDatos/Mentoria Jurisprudencia/datos/full-dataset/dataset.jsonl")
OUT = Path("/home/javier/programacion/Educacion/DiploDatos/Mentoria Jurisprudencia/datos/work-sample-su-fa-50k.jsonl.gz")

# Among SU+FA in the census: SU 483305, FA 286283 → 0.628 / 0.372
N = 50_000
N_SU = 31_400
N_FA = N - N_SU
SEED = 42


def prefix(row) -> str:
    i = row.get("id-infojus")
    if not isinstance(i, str) or len(i) < 2:
        return "<NA>"
    return i[:2]


def main():
    rng = random.Random(SEED)
    buf = {"SU": [], "FA": []}
    seen = {"SU": 0, "FA": 0}
    want = {"SU": N_SU, "FA": N_FA}
    with open(FULL, "rt", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            p = prefix(row)
            if p not in want:
                continue
            seen[p] += 1
            b = buf[p]
            k = want[p]
            if len(b) < k:
                b.append(line if line.endswith("\n") else line + "\n")
            else:
                j = rng.randrange(seen[p])
                if j < k:
                    b[j] = line if line.endswith("\n") else line + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with gzip.open(OUT, "wt", encoding="utf-8") as g:
        for p in ("SU", "FA"):
            for line in buf[p]:
                g.write(line)
                n += 1
    print("wrote", OUT, "n", n, "seen", dict(seen))


if __name__ == "__main__":
    main()
