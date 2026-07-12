#!/usr/bin/env python3
"""Generate reports/targetgate_explorer.html — a self-contained, no-backend page
that lets a reviewer search the 924-perturbation authoritative reversal table by
gene, filter by evidence depth / decision, sort by any column, and read the primary
non-advancement reason. All data is embedded inline; the page needs no server and no
private data.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FROZEN = REPO / "results" / "frozen"


def main() -> None:
    ap = pd.read_csv(FROZEN / "all_perturbations_authoritative_reversal.tsv", sep="\t")
    pc = pd.read_csv(FROZEN / "primary_comparison.tsv", sep="\t")
    cols = ["gene_symbol", "perturbation_id", "reversal_score", "global_rank", "global_percentile",
            "screen_level_status", "evidence_depth", "deep_validation_status",
            "final_evidence_class", "primary_rejection_or_nonadvance_reason"]
    records = ap[cols].fillna("").to_dict(orient="records")
    for r in records:
        r["reversal_score"] = round(float(r["reversal_score"]), 4)
        r["global_percentile"] = round(float(r["global_percentile"]), 1)
    deep = {row["target"]: dict(label=row["final_public_label"], reversal=row["primary_reversal"],
                                decision=row["final_decision"]) for _, row in pc.iterrows()}
    data_json = json.dumps(records)
    deep_json = json.dumps(deep)
    n = len(records)

    page = _TEMPLATE.replace("__DATA__", data_json).replace("__DEEP__", deep_json).replace("__N__", str(n))
    out = REPO / "reports" / "targetgate_explorer.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)} ({out.stat().st_size/1024:.0f} KB, {n} perturbations)")


_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>TargetGate Explorer</title>
<style>
:root {
  --bg:#ffffff; --fg:#1a1d21; --muted:#5b6570; --card:#f6f8fa; --line:#e3e8ee;
  --accent:#0072B2; --green:#0a7d5a; --amber:#9a6a00; --red:#b23b1e; --grey:#6b7280;
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#0f1216; --fg:#e6eaef; --muted:#9aa4af; --card:#171b21; --line:#262c34;
          --accent:#56B4E9; --green:#3ecfa0; --amber:#e0a53a; --red:#f0785a; --grey:#9aa4af; }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
.wrap { max-width:1180px; margin:0 auto; padding:28px 20px 60px; }
h1 { font-size:1.7rem; margin:0 0 2px; letter-spacing:-.01em; }
.sub { color:var(--muted); margin:0 0 4px; }
.msg { color:var(--fg); background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent);
  padding:10px 14px; border-radius:8px; margin:16px 0; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:18px 0; }
.card { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }
.card .k { font-size:1.5rem; font-weight:700; }
.card .l { color:var(--muted); font-size:.85rem; }
.controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:14px 0; }
input,select { background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:8px;
  padding:8px 10px; font-size:14px; }
input#q { flex:1 1 240px; min-width:200px; }
.tablewrap { overflow-x:auto; border:1px solid var(--line); border-radius:10px; }
table { border-collapse:collapse; width:100%; font-size:13.5px; }
th,td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--line); white-space:nowrap; }
th { position:sticky; top:0; background:var(--card); cursor:pointer; user-select:none; }
th:hover { color:var(--accent); }
td.reason { white-space:normal; min-width:260px; color:var(--muted); font-size:12.5px; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:11.5px; font-weight:600;
  border:1px solid currentColor; }
.b-ret { color:var(--green); } .b-rej { color:var(--red); } .b-cmp { color:var(--accent); }
.b-safe { color:var(--amber); } .b-none { color:var(--grey); }
.deep { font-weight:700; }
.foot { color:var(--muted); font-size:12.5px; margin-top:18px; }
a { color:var(--accent); }
.count { color:var(--muted); font-size:13px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>TargetGate Explorer</h1>
  <p class="sub">Evidence-gated screen of __N__ CD4 T-cell perturbations — search, filter, and read why each was or was not advanced.</p>
  <div class="msg"><strong>Ranking is not validation.</strong> A high reversal score is necessary but not
  sufficient for target nomination. Reversal here is the screen-substrate score; the authoritative deep
  RICTOR reversal is +0.161 (responder-resolved). Deep decisions come from the bounded validation branches.</div>

  <div class="cards" id="cards"></div>

  <div class="controls">
    <input id="q" type="search" placeholder="Search gene symbol (e.g. RICTOR, PAK2, STAT3)…" autocomplete="off"/>
    <select id="depth"><option value="">all evidence depths</option></select>
    <select id="cls"><option value="">all decisions</option></select>
    <span class="count" id="count"></span>
  </div>

  <div class="tablewrap">
    <table id="tbl">
      <thead><tr>
        <th data-k="gene_symbol">gene</th>
        <th data-k="reversal_score">reversal</th>
        <th data-k="global_rank">rank</th>
        <th data-k="global_percentile">pctile</th>
        <th data-k="screen_level_status">screen status</th>
        <th data-k="evidence_depth">depth</th>
        <th data-k="deep_validation_status">deep status</th>
        <th data-k="final_evidence_class">final decision</th>
        <th data-k="primary_rejection_or_nonadvance_reason">reason</th>
      </tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </div>

  <p class="foot">Source: <code>results/frozen/all_perturbations_authoritative_reversal.tsv</code> +
  <code>primary_comparison.tsv</code>. Screen substrate = corrected activated-memory raw-count JIA
  synovium-vs-blood disease vector (924 perturbations). Not all perturbations underwent deep validation;
  see <code>results/frozen/candidate_funnel.tsv</code> and <code>rejection_ledger.tsv</code>. This page is
  self-contained and uses no private data.</p>
</div>

<script>
const DATA = __DATA__;
const DEEP = __DEEP__;
const badge = (c) => {
  const map = {RETAINED_MECHANISM_HYPOTHESIS:['b-ret','RETAINED'],
    REJECTED_AFTER_DEEP_VALIDATION:['b-rej','REJECTED'], COMPARATOR_ONLY:['b-cmp','COMPARATOR'],
    SAFETY_CONSTRAINED:['b-safe','SAFETY-CONSTRAINED'], EXPLORATORY_SINGLE_STATE_HIT:['b-none','EXPLORATORY'],
    NONSPECIFIC_BROAD_REVERSER:['b-none','BROAD-REVERSER'], NOT_ADVANCED_FROM_SCREEN:['b-none','NOT ADVANCED']};
  const [cl,txt] = map[c] || ['b-none', c||'—'];
  return `<span class="badge ${cl}">${txt}</span>`;
};
let sortK='global_rank', sortAsc=true;

function summary(){
  const total = DATA.length;
  const conv = DATA.filter(d=>d.screen_level_status==='CONVERGENT_FDR<0.10').length;
  const deep = DATA.filter(d=>d.evidence_depth==='DEEP').length;
  const c = document.getElementById('cards');
  c.innerHTML = [
    ['__N__','perturbations screened'],
    [conv,'convergent + FDR<0.10'],
    [deep,'deep-validated targets'],
    ['1','retained mechanism node (RICTOR)'],
    ['1','rejected after validation (PAK2)'],
  ].map(([k,l])=>`<div class="card"><div class="k">${k}</div><div class="l">${l}</div></div>`).join('');
}
function fillSelects(){
  const depths=[...new Set(DATA.map(d=>d.evidence_depth))].sort();
  const cls=[...new Set(DATA.map(d=>d.final_evidence_class))].sort();
  depths.forEach(v=>document.getElementById('depth').insertAdjacentHTML('beforeend',`<option>${v}</option>`));
  cls.forEach(v=>document.getElementById('cls').insertAdjacentHTML('beforeend',`<option>${v}</option>`));
}
function render(){
  const q=document.getElementById('q').value.trim().toUpperCase();
  const dp=document.getElementById('depth').value, cl=document.getElementById('cls').value;
  let rows=DATA.filter(d=>
    (!q||String(d.gene_symbol).toUpperCase().includes(q)) &&
    (!dp||d.evidence_depth===dp) && (!cl||d.final_evidence_class===cl));
  rows.sort((a,b)=>{ let x=a[sortK],y=b[sortK];
    if(typeof x==='number'&&typeof y==='number'){} else {x=String(x);y=String(y);}
    return (x<y?-1:x>y?1:0)*(sortAsc?1:-1); });
  document.getElementById('count').textContent = rows.length+' / __N__ shown';
  document.getElementById('rows').innerHTML = rows.slice(0,600).map(d=>{
    const deepMark = d.evidence_depth==='DEEP' ? ' class="deep"' : '';
    return `<tr><td${deepMark}>${d.gene_symbol}</td><td>${d.reversal_score>=0?'+':''}${d.reversal_score.toFixed(3)}</td>`+
      `<td>${d.global_rank}</td><td>${d.global_percentile}</td><td>${d.screen_level_status}</td>`+
      `<td>${d.evidence_depth}</td><td>${d.deep_validation_status||'—'}</td>`+
      `<td>${badge(d.final_evidence_class)}</td><td class="reason">${d.primary_rejection_or_nonadvance_reason||'—'}</td></tr>`;
  }).join('') + (rows.length>600?`<tr><td colspan="9" class="count">…showing first 600 of ${rows.length}; refine your search.</td></tr>`:'');
}
document.querySelectorAll('th').forEach(th=>th.addEventListener('click',()=>{
  const k=th.dataset.k; if(sortK===k) sortAsc=!sortAsc; else {sortK=k; sortAsc=true;} render();
}));
['q','depth','cls'].forEach(id=>document.getElementById(id).addEventListener('input',render));
summary(); fillSelects(); render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
