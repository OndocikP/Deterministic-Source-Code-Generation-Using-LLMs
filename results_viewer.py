#!/usr/bin/env python3
"""
Lokálny webserver na prehliadanie výsledkov testov determinizmu LLM.

Spustenie:
    python results_viewer.py
    python results_viewer.py "D:\\cesta\\k\\Evaluations\\Results" --port 8000

Štruktúra, ktorú server očakáva (všetko sa načítava dynamicky pri každom
načítaní stránky, takže nový OS alebo test stačí pridať ako priečinok):

    Results/
      Results_report.csv                      <- hlavná tabuľka
      <OS>/
        <OS>_report.csv                       <- súhrn pre OS
        <test>/
          <test>_report.csv                   <- výsledky jedného testu

Bez externých knižníc, stačí Python 3.8+.
"""
import argparse
import csv
import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

DEFAULT_RESULTS = Path(
    r"D:\GitHub\Tuke\Deterministic-Source-Code-Generation-Using-LLMs\Evaluations\Results"
)

RESULTS_DIR = DEFAULT_RESULTS


# ----------------------------------------------------------------- dáta ----
def read_csv(path: Path):
    """Načíta CSV ako {columns, rows}. Číselné hodnoty ostanú ako text,
    prehliadač si ich vyhodnotí sám."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        return {"columns": [], "rows": []}
    return {"columns": rows[0], "rows": rows[1:]}


def pick_report(folder: Path):
    """<folder>_report.csv, inak prvé CSV v priečinku."""
    preferred = folder / f"{folder.name}_report.csv"
    if preferred.is_file():
        return preferred
    found = sorted(folder.glob("*.csv"))
    return found[0] if found else None


def list_subdirs(folder: Path):
    return sorted(
        (p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".")),
        key=lambda p: p.name.lower(),
    )


def list_oses():
    """Každý podpriečinok Results/, ktorý obsahuje CSV alebo priečinky s testami."""
    result = []
    for d in list_subdirs(RESULTS_DIR):
        has_csv = pick_report(d) is not None
        tests = [t for t in list_subdirs(d) if pick_report(t)]
        if has_csv or tests:
            result.append({"name": d.name, "tests": len(tests)})
    return result


def safe_child(parent: Path, name: str):
    """Ochrana proti ../ v názve priečinka."""
    child = (parent / name).resolve()
    if parent.resolve() not in child.parents:
        return None
    return child if child.is_dir() else None


def load_os(name: str):
    os_dir = safe_child(RESULTS_DIR, name)
    if os_dir is None:
        return None
    report = pick_report(os_dir)
    tests = []
    for t in list_subdirs(os_dir):
        rep = pick_report(t)
        if rep:
            tests.append({"name": t.name, **read_csv(rep)})
    return {
        "name": name,
        "summary": read_csv(report) if report else None,
        "tests": tests,
    }


# --------------------------------------------------------------- server ----
class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        try:
            if path == "/":
                self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
            elif path == "/api/main":
                f = RESULTS_DIR / "Results_report.csv"
                self._json(read_csv(f) if f.is_file()
                           else {"error": f"Chýba súbor {f}"})
            elif path == "/api/oses":
                self._json(list_oses())
            elif path.startswith("/api/os/"):
                data = load_os(path[len("/api/os/"):])
                if data is None:
                    self._json({"error": "OS sa nenašiel"}, 404)
                else:
                    self._json(data)
            else:
                self._send(404, b"Not found", "text/plain")
        except Exception as e:  # noqa: BLE001
            self._json({"error": str(e)}, 500)

    def log_message(self, fmt, *args):
        pass  # tichý výstup


# ------------------------------------------------------------ frontend ----
PAGE = r"""<!doctype html>
<html lang="sk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Determinizmus LLM – výsledky</title>
<style>
:root{
  --bg:#f6f7f9; --surface:#fff; --ink:#15191f; --muted:#5d6673; --line:#dfe3e8;
  --accent:#1f5eff; --accent-ink:#fff; --bar:rgba(31,94,255,.17); --bar-low:rgba(214,76,48,.20);
  --font:"Segoe UI Variable Text","Segoe UI",system-ui,-apple-system,Roboto,sans-serif;
  --mono:"Cascadia Mono",Consolas,ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){
  :root{--bg:#101318; --surface:#181c23; --ink:#e8ebf0; --muted:#98a1ae; --line:#2a303a;
    --accent:#6f95ff; --accent-ink:#0b1020; --bar:rgba(111,149,255,.24); --bar-low:rgba(240,110,80,.26);}
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 var(--font)}
main{max-width:1100px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:26px;margin:0 0 4px;letter-spacing:-.01em}
h2{font-size:17px;margin:40px 0 12px}
.sub{color:var(--muted);margin:0 0 24px}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:8px;overflow:auto}
table{border-collapse:collapse;width:100%}
th,td{padding:9px 14px;text-align:left;white-space:nowrap}
th{font-weight:600;font-size:13px;color:var(--muted);border-bottom:1px solid var(--line);
   cursor:pointer;user-select:none;position:sticky;top:0;background:var(--surface)}
th:hover{color:var(--ink)}
th .arr{display:inline-block;width:1em;color:var(--accent)}
td{border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
th.num{text-align:right}
td.name{font-weight:500}
.cell{position:relative}
.cell::before{content:"";position:absolute;inset:3px auto 3px 0;width:var(--w);background:var(--bar);border-radius:0 3px 3px 0}
.cell.low::before{background:var(--bar-low)}
.cell span{position:relative}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);
  border-radius:6px;padding:8px 14px;cursor:pointer}
.chip:hover{border-color:var(--accent)}
.chip[aria-pressed=true]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.chip small{opacity:.7;margin-left:6px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
details{background:var(--surface);border:1px solid var(--line);border-radius:8px;margin:10px 0}
summary{padding:11px 16px;cursor:pointer;font-weight:600;font-family:var(--mono);font-size:14px}
details[open] summary{border-bottom:1px solid var(--line)}
details .panel{border:0;border-radius:0 0 8px 8px}
.bar{display:flex;gap:10px;align-items:center;margin:0 0 12px;flex-wrap:wrap}
.bar button{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;cursor:pointer;padding:2px 4px}
.msg{color:var(--muted);padding:18px}
.err{color:#c8321e}
</style>
</head>
<body>
<main>
  <h1>Determinizmus generovania kódu pomocou LLM</h1>
  <p class="sub" id="path">Výsledky testovania modelov</p>

  <div class="panel" id="main"><p class="msg">Načítavam…</p></div>

  <h2>Operačné systémy</h2>
  <div class="chips" id="oses"></div>

  <section id="os-view"></section>
</main>

<script>
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const isNum = v => v !== '' && !isNaN(Number(v));

async function api(url){
  const r = await fetch(url);
  const j = await r.json();
  if(j.error) throw new Error(j.error);
  return j;
}

/* Tabuľka s radením. Stĺpce, kde sú všetky hodnoty čísla v 0–1, dostanú pruh. */
function renderTable(host, data){
  const cols = data.columns;
  let rows = data.rows.map(r => r.slice());
  const numeric = cols.map((_, i) => rows.length && rows.every(r => isNum(r[i])));
  const ratio = cols.map((_, i) => numeric[i] && rows.every(r => Number(r[i]) >= 0 && Number(r[i]) <= 1));
  let sortCol = -1, dir = 1;

  function draw(){
    const head = cols.map((c, i) =>
      `<th class="${numeric[i]?'num':''}" data-i="${i}">${esc(c.replaceAll('_',' '))}<span class="arr">${sortCol===i?(dir>0?'▲':'▼'):''}</span></th>`).join('');
    const body = rows.map(r => '<tr>' + r.map((v, i) => {
      if(ratio[i]){
        const n = Number(v);
        return `<td class="num cell ${n<0.6?'low':''}" style="--w:${n*100}%"><span>${esc(v)}</span></td>`;
      }
      return `<td class="${numeric[i]?'num':(i===0?'name':'')}">${esc(v)}</td>`;
    }).join('') + '</tr>').join('');
    host.innerHTML = `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
    host.querySelectorAll('th').forEach(th => th.onclick = () => {
      const i = +th.dataset.i;
      dir = sortCol === i ? -dir : 1; sortCol = i;
      rows.sort((a, b) => numeric[i] ? (a[i]-b[i])*dir : a[i].localeCompare(b[i])*dir);
      draw();
    });
  }
  if(!cols.length){ host.innerHTML = '<p class="msg">Súbor je prázdny.</p>'; return; }
  draw();
}

async function loadMain(){
  try { renderTable($('#main'), await api('/api/main')); }
  catch(e){ $('#main').innerHTML = `<p class="msg err">${esc(e.message)}</p>`; }
}

async function loadOses(){
  const list = await api('/api/oses');
  const host = $('#oses');
  if(!list.length){ host.innerHTML = '<p class="msg">Nenašli sa žiadne priečinky s operačnými systémami.</p>'; return; }
  host.innerHTML = list.map(o =>
    `<button class="chip" aria-pressed="false" data-os="${esc(o.name)}">${esc(o.name)}<small>${o.tests} testov</small></button>`).join('');
  host.querySelectorAll('.chip').forEach(b => b.onclick = () => selectOs(b.dataset.os));
  const fromHash = decodeURIComponent(location.hash.slice(1));
  if(fromHash && list.some(o => o.name === fromHash)) selectOs(fromHash);
}

async function selectOs(name){
  document.querySelectorAll('.chip').forEach(b => b.setAttribute('aria-pressed', b.dataset.os === name));
  history.replaceState(null, '', '#' + encodeURIComponent(name));
  const view = $('#os-view');
  view.innerHTML = '<p class="msg">Načítavam…</p>';
  try{
    const d = await api('/api/os/' + encodeURIComponent(name));
    view.innerHTML = `<h2>${esc(d.name)}</h2>`;
    if(d.summary && d.summary.columns.length){
      const p = document.createElement('div'); p.className = 'panel';
      view.appendChild(p); renderTable(p, d.summary);
    }
    if(!d.tests.length){ view.insertAdjacentHTML('beforeend', '<p class="msg">Žiadne testy.</p>'); return; }
    view.insertAdjacentHTML('beforeend',
      `<h2>Testy (${d.tests.length})</h2>
       <div class="bar"><button id="openAll">Rozbaliť všetky</button><button id="closeAll">Zbaliť všetky</button></div>`);
    d.tests.forEach(t => {
      const det = document.createElement('details');
      det.innerHTML = `<summary>${esc(t.name)}</summary><div class="panel"></div>`;
      view.appendChild(det);
      renderTable(det.querySelector('.panel'), t);
    });
    $('#openAll').onclick = () => view.querySelectorAll('details').forEach(x => x.open = true);
    $('#closeAll').onclick = () => view.querySelectorAll('details').forEach(x => x.open = false);
    view.querySelector('details').open = true;
  }catch(e){ view.innerHTML = `<p class="msg err">${esc(e.message)}</p>`; }
}

loadMain(); loadOses();
</script>
</body>
</html>
"""


def main():
    global RESULTS_DIR
    ap = argparse.ArgumentParser(description="Prehliadač výsledkov determinizmu LLM")
    ap.add_argument("results_dir", nargs="?", default=str(DEFAULT_RESULTS),
                    help="cesta k priečinku Evaluations/Results")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    RESULTS_DIR = Path(args.results_dir).expanduser()
    if not RESULTS_DIR.is_dir():
        sys.exit(f"Priečinok neexistuje: {RESULTS_DIR}\n"
                 f"Zadaj cestu ako argument: python results_viewer.py \"cesta\\k\\Results\"")

    url = f"http://127.0.0.1:{args.port}/"
    print(f"Výsledky: {RESULTS_DIR}\nServer beží na {url}  (Ctrl+C ukončí)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nKoniec.")


if __name__ == "__main__":
    main()
