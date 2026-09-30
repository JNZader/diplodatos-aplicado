#!/usr/bin/env python3
"""Stream-compare official 8.7k sample vs full SAIJ JSONL (no pandas of 874k)."""
from __future__ import annotations

import gzip
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/javier/programacion/Educacion/DiploDatos/Mentoria Jurisprudencia")
SAMPLE = ROOT / "datos/dataset_sample.jsonl.gz"
FULL = ROOT / "datos/full-dataset/dataset.jsonl"
OUT = ROOT / "practicos/P1/validacion-muestra.json"

DUMMY = "Término elegido para describir"
FUERO = ["CIVIL", "COMERCIAL", "PENAL", "LABORAL", "ADMINISTRATIVO", "CONSTITUCIONAL"]


def iter_jsonl(path: Path):
    if str(path).endswith(".gz"):
        f = gzip.open(path, "rt", encoding="utf-8")
    else:
        f = open(path, "rt", encoding="utf-8")
    with f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def nonempty(v) -> bool:
    return v not in (None, "", {}, [])


def prefix_of(row) -> str:
    i = row.get("id-infojus")
    if not nonempty(i) or not isinstance(i, str) or len(i) < 2:
        return "<NA>"
    return i[:2]


def is_dummy(row) -> bool:
    d = row.get("descriptores")
    if isinstance(d, (dict, list)) and DUMMY in json.dumps(d, ensure_ascii=False):
        return True
    return not nonempty(row.get("id-infojus"))


def clean_text(t) -> str:
    if not isinstance(t, str):
        return ""
    t = re.sub(r"\[\[.*?\]\]", " ", t)
    return t


def fecha_year(row):
    f = row.get("fecha")
    if not nonempty(f):
        return None
    s = str(f).split("|")[0][:4]
    try:
        y = int(s)
    except ValueError:
        return None
    if 1800 <= y <= 2030:
        return y
    return None


def materia_fuero_bucket(m) -> str:
    if not isinstance(m, str) or not m:
        return "<sin materia>"
    parts = set(re.split(r"[^A-Za-zÁÉÍÓÚáéíóúÑñ]+", m.upper()))
    civ, com = "CIVIL" in parts, "COMERCIAL" in parts
    if civ and com:
        return "CIVIL∩COMERCIAL"
    if civ:
        return "CIVIL_only"
    if com:
        return "COMERCIAL_only"
    hits = [t for t in FUERO if t in parts]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        return "multi_otro"
    return "<otro>"


class Acc:
    def __init__(self):
        self.n = 0
        self.dummy = 0
        self.no_id = 0
        self.prefix = Counter()
        self.prov = Counter()
        self.year = Counter()
        self.fuero_b = Counter()
        self.pipe_fecha = 0
        self.su_sumario_chars = []  # only store if small stream; for full use bins
        self.len_s_bins = Counter()
        self.len_t_bins = Counter()
        self.su = 0
        self.su_both_text = 0
        self.su_equal = 0
        self.materia_nunique = set()
        self.materia_n = 0
        self.ts_pos = 0

    def len_bin(self, n: int) -> str:
        if n < 40:
            return "0-39"
        if n < 80:
            return "40-79"
        if n < 160:
            return "80-159"
        if n < 320:
            return "160-319"
        if n < 640:
            return "320-639"
        if n < 1280:
            return "640-1279"
        return "1280+"

    def add(self, row: dict, store_materia_set: bool = True):
        self.n += 1
        if is_dummy(row):
            self.dummy += 1
        if not nonempty(row.get("id-infojus")):
            self.no_id += 1
        pref = prefix_of(row)
        self.prefix[pref] += 1
        if nonempty(row.get("provincia")):
            self.prov[str(row["provincia"])] += 1
        y = fecha_year(row)
        if y is not None:
            self.year[y] += 1
        if isinstance(row.get("fecha"), str) and "|" in row["fecha"]:
            self.pipe_fecha += 1
        ts = row.get("timestamp")
        if isinstance(ts, (int, float)) and ts > 0:
            self.ts_pos += 1
        m = row.get("materia")
        if nonempty(m) and isinstance(m, str):
            self.materia_n += 1
            self.fuero_b[materia_fuero_bucket(m)] += 1
            if store_materia_set and len(self.materia_nunique) < 50000:
                self.materia_nunique.add(m)
        if pref == "SU":
            self.su += 1
            s = clean_text(row.get("sumario"))
            t = clean_text(row.get("texto"))
            self.len_s_bins[self.len_bin(len(s))] += 1
            self.len_t_bins[self.len_bin(len(t))] += 1
            if s and t:
                self.su_both_text += 1
                if row.get("sumario") == row.get("texto"):
                    self.su_equal += 1

    def snapshot(self) -> dict:
        def rates(c: Counter, den: int):
            den = max(den, 1)
            return {k: round(v / den, 6) for k, v in c.most_common(20)}

        return {
            "n": self.n,
            "dummy": self.dummy,
            "dummy_rate": round(self.dummy / max(self.n, 1), 6),
            "no_id": self.no_id,
            "no_id_rate": round(self.no_id / max(self.n, 1), 6),
            "prefix": dict(self.prefix),
            "prefix_rate": rates(self.prefix, self.n),
            "pipe_fecha": self.pipe_fecha,
            "pipe_rate": round(self.pipe_fecha / max(self.n, 1), 6),
            "ts_pos_rate": round(self.ts_pos / max(self.n, 1), 6),
            "materia_n": self.materia_n,
            "materia_nunique": len(self.materia_nunique),
            "fuero_bucket": dict(self.fuero_b.most_common()),
            "prov_top": dict(self.prov.most_common(8)),
            "prov_top_rate": rates(self.prov, self.n),
            "year_minmax": [min(self.year) if self.year else None, max(self.year) if self.year else None],
            "year_top": dict(self.year.most_common(8)),
            "su": self.su,
            "su_equal_rate": round(self.su_equal / max(self.su_both_text, 1), 6),
            "len_sumario_bins": dict(self.len_s_bins),
            "len_texto_bins": dict(self.len_t_bins),
        }


def tvd(p: dict, q: dict) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0)) for k in keys)


def fill_acc(path: Path, store_set: bool = True) -> Acc:
    a = Acc()
    for row in iter_jsonl(path):
        a.add(row, store_materia_set=store_set)
    return a


def reservoir_srs(path: Path, k: int, seed: int = 42) -> Acc:
    rng = random.Random(seed)
    buf = []
    n = 0
    for row in iter_jsonl(path):
        n += 1
        if len(buf) < k:
            buf.append(row)
        else:
            j = rng.randrange(n)
            if j < k:
                buf[j] = row
    a = Acc()
    for row in buf:
        a.add(row)
    return a


def stratified(path: Path, k: int, prefix_full: Counter, seed: int = 42) -> Acc:
    """Approximate proportional allocation by id prefix, second pass reservoirs."""
    rng = random.Random(seed)
    total = sum(prefix_full.values()) or 1
    alloc = {}
    leftover = k
    items = list(prefix_full.items())
    for i, (pref, c) in enumerate(items):
        if i == len(items) - 1:
            alloc[pref] = leftover
        else:
            n = max(1, round(k * c / total)) if c else 0
            n = min(n, leftover - (len(items) - 1 - i))
            alloc[pref] = max(0, n)
            leftover -= alloc[pref]
    buf = {pref: [] for pref in alloc}
    seen = Counter()
    for row in iter_jsonl(path):
        pref = prefix_of(row)
        seen[pref] += 1
        kk = alloc.get(pref, 0)
        if kk <= 0:
            continue
        b = buf[pref]
        if len(b) < kk:
            b.append(row)
        else:
            j = rng.randrange(seen[pref])
            if j < kk:
                b[j] = row
    a = Acc()
    for rows in buf.values():
        for row in rows:
            a.add(row)
    return a


def main():
    print("pass sample…")
    sample = fill_acc(SAMPLE)
    print("  n", sample.n)
    print("pass full…")
    full = fill_acc(FULL, store_set=True)
    print("  n", full.n)
    print("pass SRS…")
    srs = reservoir_srs(FULL, sample.n, seed=42)
    print("  n", srs.n)
    print("pass stratified…")
    strat = stratified(FULL, sample.n, full.prefix, seed=42)
    print("  n", strat.n)

    snaps = {
        "sample_oficial": sample.snapshot(),
        "full": full.snapshot(),
        "srs_8k7": srs.snapshot(),
        "strat_prefix_8k7": strat.snapshot(),
    }
    snaps["tvd_prefix_sample_vs_full"] = tvd(
        sample.snapshot()["prefix_rate"], full.snapshot()["prefix_rate"]
    )
    snaps["tvd_prefix_srs_vs_full"] = tvd(
        srs.snapshot()["prefix_rate"], full.snapshot()["prefix_rate"]
    )
    snaps["tvd_prefix_strat_vs_full"] = tvd(
        strat.snapshot()["prefix_rate"], full.snapshot()["prefix_rate"]
    )
    snaps["tvd_prov_sample_vs_full"] = tvd(
        sample.snapshot()["prov_top_rate"], full.snapshot()["prov_top_rate"]
    )
    snaps["tvd_prov_srs_vs_full"] = tvd(
        srs.snapshot()["prov_top_rate"], full.snapshot()["prov_top_rate"]
    )
    OUT.write_text(json.dumps(snaps, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
