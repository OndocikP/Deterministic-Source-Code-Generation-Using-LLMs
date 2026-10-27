#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

if __package__ in (None, ''):
    here_root = str(Path(__file__).resolve().parent)
    if here_root not in sys.path:
        sys.path.insert(0, here_root)

try:
    from .data import (
        LANGUAGE_OPTIONS,
        MODEL_OPTIONS,
        average_values,
        build_setup_content,
        create_project_files,
        fmt_metric,
        list_projects,
        load_project_config,
        metric_class,
        project_summary_rows,
        read_reports,
        save_project_config,
    )
    from .report_loud import get_json
except ImportError:
    from data import (
        LANGUAGE_OPTIONS,
        MODEL_OPTIONS,
        average_values,
        build_setup_content,
        create_project_files,
        fmt_metric,
        list_projects,
        load_project_config,
        metric_class,
        project_summary_rows,
        read_reports,
        save_project_config,
    )
    from report_loud import get_json

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
TASKS_DIR = PROJECT_ROOT / 'Code_Generation_Tasks'
HOST = os.environ.get('DASHBOARD_HOST', '0.0.0.0')
PORT = int(os.environ.get('DASHBOARD_PORT', '8000'))


def find_available_port(start_port: int, max_port: int = 9000):
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f'No free port found between {start_port} and {max_port}.')

METRIC_NAMES = (
    ('Code_Identity', 'Code Identity'),
    ('AST_Structure', 'AST Structure'),
    ('Behavioral_Equivalence', 'Behavioral Equivalence'),
)

COMMANDS = {
    'main': 'cls & python -m Experiment_Framework.main',
    'remove_csv': 'cls & python -m Experiment_Framework.remove_csv',
    'report': 'cls & python -m Experiment_Framework.report',
}

RUN_OUTPUTS = {}
RUN_PROCESSES = {}
RUN_LOCK = threading.Lock()


def esc(value):
    return str(value if value is not None else '')


def fmt_row(value):
    return f'<td><span class="score {metric_class(value)}">{esc(fmt_metric(value))}</span></td>'


def build_home_page():
    reports = read_reports()
    projects = sorted({report['project'] for report in reports})
    languages = sorted({report['language'] for report in reports})
    summary_cards = [('Projekty', str(len(projects))), ('Reporty', str(len(reports))), ('Riadky výsledkov', str(sum(len(r['rows']) for r in reports)))]
    avg = average_values(reports)
    for key, label in METRIC_NAMES:
        summary_cards.append((f'Priemer · {label}', fmt_metric(avg.get(key))))

    summary_html = ''.join(f'<div class="stat"><span>{esc(label)}</span><strong>{esc(value)}</strong></div>' for label, value in summary_cards)

    model_rows = []
    for model_name, samples, metric_avg, overall_avg in project_summary_rows(reports):
        cells = ''.join(fmt_row(metric_avg.get(key)) for key, _ in METRIC_NAMES)
        model_rows.append(
            '<tr>'
            f'<td class="model">{esc(model_name)}</td>'
            f'<td>{samples}</td>'
            f'{cells}'
            f'<td><span class="score {metric_class(overall_avg)}">{esc(fmt_metric(overall_avg))}</span></td>'
            '</tr>'
        )

    model_summary_html = '<section class="model-summary"><h2>Priemer pre každý model</h2><div class="notice">Zatiaľ nie sú dáta na výpočet priemerov modelov.</div></section>'
    if model_rows:
        model_summary_html = (
            '<section class="model-summary"><h2>Priemer pre každý model</h2>'
            '<div class="table-wrap"><table><thead><tr><th>Model / súbor</th><th>Vzorky</th><th>Code Identity</th><th>AST Structure</th><th>Behavioral Equivalence</th><th>Celkový priemer</th></tr></thead><tbody>'
            f"{''.join(model_rows)}"
            '</tbody></table></div></section>'
        )

    if not TASKS_DIR.exists():
        empty_message = f'<div class="notice"><strong>Priečinok sa nenašiel.</strong><br>Očakávaná cesta: <code>{esc(TASKS_DIR)}</code><br>Umiestni Code_Generation_Tasks vedľa priečinka Lokal_FrontEnd_Webserver.</div>'
    elif not reports:
        empty_message = '<div class="notice">Nenašli sa žiadne súbory <code>report_*.csv</code>. Očakávaný formát cesty je <code>Code_Generation_Tasks/názov_projektu/jazyk/report_jazyk.csv</code>.</div>'
    else:
        empty_message = ''

    report_cards_html = ''
    for report in reports:
        rows_html = []
        if report.get('error'):
            rows_html.append(f'<tr><td colspan="4" class="error">CSV sa nepodarilo načítať: {esc(report["error"])}</td></tr>')
        elif not report['rows']:
            rows_html.append('<tr><td colspan="4" class="empty">V tomto reporte nie sú žiadne výsledky.</td></tr>')
        else:
            for row in report['rows']:
                cells = ''.join(fmt_row(row['metrics'].get(key)) for key, _ in METRIC_NAMES)
                rows_html.append('<tr>' f'<td class="model">{esc(row["file_name"])}</td>' f'{cells}' '</tr>')
        report_cards_html += (
            '<section class="report-card" data-project="{project_key}" data-language="{language_key}">'
            '<div class="report-head"><div><div class="eyebrow">{language}</div><h3>{project}</h3><div class="filepath">{path}</div></div>'
            '<div class="report-meta"><span class="row-count">{row_count} modelov</span><span class="updated">Upravené: {modified}</span></div></div>'
            '<div class="table-wrap"><table><thead><tr><th>Model / súbor</th><th>Code Identity</th><th>AST Structure</th><th>Behavioral Equivalence</th></tr></thead><tbody>{rows}</tbody></table></div></section>'
        ).format(
            project_key=esc(report['project'].lower()),
            language_key=esc(report['language'].lower()),
            language=esc(report['language']),
            project=esc(report['project']),
            path=esc(report['path']),
            row_count=len(report['rows']),
            modified=esc(report['modified'] or 'neznáme'),
            rows=''.join(rows_html),
        )

    if not report_cards_html:
        report_cards_html = '<div class="notice">Zatiaľ nie sú dostupné žiadne reporty.</div>'

    project_options = ''.join(f'<option value="{esc(p.lower())}">{esc(p)}</option>' for p in projects)
    language_options = ''.join(f'<option value="{esc(lang.lower())}">{esc(lang)}</option>' for lang in languages)

    return (
        Path(HERE / 'templates' / 'home.html').read_text(encoding='utf-8')
        .replace('__SUMMARY_CARDS__', summary_html)
        .replace('__MODEL_SUMMARY__', model_summary_html)
        .replace('__EMPTY_MESSAGE__', empty_message)
        .replace('__PROJECT_OPTIONS__', project_options)
        .replace('__LANGUAGE_OPTIONS__', language_options)
        .replace('__REPORT_COUNT__', f'{len(reports)} reportov')
        .replace('__REPORT_CARDS__', report_cards_html)
    )


def build_reporti_page():
    report_rows = []
    all_project_reports = read_reports()

    for project_name in list_projects():
        config = load_project_config(project_name)
        project_reports = [report for report in all_project_reports if report['project'] == project_name]
        report_count = len(project_reports)
        language_count = len({report['language'] for report in project_reports})
        checked = ' checked' if config.get('include_in_averages', True) else ''

        language_sections = []
        project_dir = TASKS_DIR / project_name
        if project_dir.exists():
            for language_dir in sorted(project_dir.iterdir()):
                if not language_dir.is_dir():
                    continue
                language_name = language_dir.name
                report = next((item for item in project_reports if item['language'] == language_name), None)
                language_rows = []
                language_file_name = f'report_{language_name.lower()}.csv'
                language_path = language_dir / language_file_name
                language_link = f'<a class="file-link" href="{language_path.as_uri()}" target="_blank">{esc(language_name)}</a>' if language_path.exists() else esc(language_name)

                model_dirs = sorted([p for p in language_dir.iterdir() if p.is_dir() and not p.name.startswith('.')], key=lambda p: p.name.lower())

                for model_dir in model_dirs:
                    model_name = model_dir.name
                    model_report = model_dir / 'report.csv'
                    behavior_report = model_dir / 'report_Behavioral_Equivalence.csv'
                    model_metrics = {}
                    if report:
                        model_row = next((row for row in report.get('rows', []) if row.get('file_name') == model_name), None)
                        if model_row:
                            model_metrics = model_row.get('metrics', {})
                    metric_cells = ''.join(
                        f'<span class="metric-pill {metric_class(model_metrics.get(key))}">{esc(fmt_metric(model_metrics.get(key)))}</span>'
                        for key, _label in METRIC_NAMES
                    )
                    model_summary = (
                        '<div class="model-entry">'
                        f'<button type="button" class="model-link-button" data-project="{esc(project_name)}" data-language="{esc(language_name)}" data-model="{esc(model_name)}">'
                        f'{esc(model_name)} {metric_cells}'
                        '</button>'
                        '</div>'
                    )
                    language_rows.append(model_summary)

                if not language_rows:
                    language_rows.append('<div class="empty-row">Pre jazyk <strong>{lang}</strong> nie sú dostupné modely.</div>'.format(lang=esc(language_name)))

                language_sections.append(
                    '<div class="project-language">'
                    f'<div class="language-header"><span>Jazyk</span><strong>{language_link}</strong></div>'
                    f'<div class="model-list">{''.join(language_rows)}</div>'
                    '</div>'
                )

        if not language_sections:
            language_sections.append('<div class="empty-row">Pre projekt <strong>{name}</strong> neboli nájdené žiadne reporty.</div>'.format(name=esc(project_name)))

        report_rows.append(
            '<div class="project-row" data-project-name="{project}">'
            '<div class="project-header">'
            f'<div class="project-main"><div class="project-name">{esc(project_name)}</div><div class="project-meta">{report_count} reportov · {language_count} jazykov</div></div>'
            '<label class="toggle"><input type="checkbox" data-project-toggle="{project}"{checked}><span>Počítať do priemeru</span></label>'
            '</div>'
            f'<div class="project-details">{''.join(language_sections)}</div>'
            '</div>'.format(project=esc(project_name), checked=checked)
        )

    project_rows = ''.join(report_rows) if report_rows else '<div class="notice">Zatiaľ nie sú vytvorené žiadne projekty.</div>'
    model_options = ''.join(f'<option value="{esc(model)}">{esc(model)}</option>' for model in MODEL_OPTIONS)
    language_options = ''.join(f'<option value="{esc(label)}">{esc(label)}</option>' for label in LANGUAGE_OPTIONS)
    return (
        Path(HERE / 'templates' / 'reporti.html').read_text(encoding='utf-8')
        .replace('__PROJECT_ROWS__', project_rows)
        .replace('__MODEL_OPTIONS__', model_options)
        .replace('__LANGUAGE_OPTIONS__', language_options)
    )


def read_request_body(handler):
    length = int(handler.headers.get('Content-Length', '0'))
    raw = handler.rfile.read(length) if length else b''
    if not raw:
        return {}
    ctype = handler.headers.get('Content-Type', '').lower()
    try:
        if ctype.startswith('application/json'):
            return json.loads(raw.decode('utf-8'))
        parsed = parse_qs(raw.decode('utf-8'))
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def start_process(command_name):
    command = COMMANDS.get(command_name)
    if not command:
        raise ValueError(f'Neznámy príkaz: {command_name}')
    with RUN_LOCK:
        RUN_OUTPUTS[command_name] = f'> {command_name}\n'
    process = subprocess.Popen(['cmd', '/c', command], cwd=str(PROJECT_ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    RUN_PROCESSES[command_name] = process

    def stream_output():
        while True:
            if process.stdout is None:
                break
            line = process.stdout.readline()
            if line:
                with RUN_LOCK:
                    RUN_OUTPUTS[command_name] += line
            if not line and process.poll() is not None:
                break
            time.sleep(0.05)
        with RUN_LOCK:
            RUN_OUTPUTS[command_name] += '\n[Skript dokončený]\n'

    threading.Thread(target=stream_output, daemon=True).start()
    return process


def handle_run_post(handler):
    payload = read_request_body(handler)
    command_name = str(payload.get('command', '')).strip()
    if command_name not in COMMANDS:
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': 'Neznámy príkaz.'}).encode('utf-8'))
        return
    try:
        process = start_process(command_name)
    except ValueError as exc:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': str(exc)}).encode('utf-8'))
        return
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps({'ok': True, 'process': {'pid': process.pid}}).encode('utf-8'))


def handle_run_output(handler):
    query = parse_qs(urlparse(handler.path).query)
    command_name = query.get('command', [''])[0]
    output = RUN_OUTPUTS.get(command_name, '')
    if command_name in RUN_PROCESSES and RUN_PROCESSES[command_name].poll() is None:
        time.sleep(0.2)
        output = RUN_OUTPUTS.get(command_name, output)
    handler.send_response(200)
    handler.send_header('Content-Type', 'text/plain; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(output.encode('utf-8'))


def handle_project_toggle(handler):
    payload = read_request_body(handler)
    project_name = str(payload.get('project_name', '')).strip()
    include = bool(payload.get('include_in_averages', True))
    if not project_name:
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': 'Chýba názov projektu.'}).encode('utf-8'))
        return
    save_project_config(project_name, include)
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps({'ok': True, 'include_in_averages': include}).encode('utf-8'))


def handle_project_create(handler):
    payload = read_request_body(handler)
    project_name = str(payload.get('project_name', '')).strip()
    prompt_text = str(payload.get('prompt', '')).strip()
    tests_data_text = str(payload.get('tests_data', '')).strip()
    setup_text = str(payload.get('setup_text', '')).strip()
    language = str(payload.get('language', 'Python')).strip() or 'Python'
    num_generations = payload.get('num_generations', 50)
    setup_extra = str(payload.get('setup_extra', '')).strip()
    models = payload.get('models', MODEL_OPTIONS)

    if not project_name or not prompt_text or not tests_data_text:
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': 'Názov projektu, prompt a test_data sú povinné.'}).encode('utf-8'))
        return
    try:
        value = int(num_generations)
        if value <= 0:
            raise ValueError
    except (TypeError, ValueError):
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': 'num_generations musí byť väčšie ako nula.'}).encode('utf-8'))
        return

    selected = [str(item).strip() for item in models if str(item).strip()] if isinstance(models, list) else MODEL_OPTIONS[:]
    if not selected:
        selected = MODEL_OPTIONS[:]
    extras = [line.strip() for line in setup_extra.splitlines() if line.strip()]
    if setup_text:
        final_setup = setup_text.rstrip()
        if extras:
            final_setup = final_setup.rstrip() + '\n' + '\n'.join(extras) + '\n'
    else:
        final_setup = build_setup_content(selected, language, value, '\n'.join(extras) if extras else '')

    try:
        created = create_project_files(project_name, prompt_text, tests_data_text, final_setup)
    except FileExistsError as exc:
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': str(exc)}).encode('utf-8'))
        return

    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps({'ok': True, 'project': created}).encode('utf-8'))


def handle_model_report(handler):
    query = parse_qs(urlparse(handler.path).query)
    project_name = str(query.get('project', [''])[0]).strip()
    language_name = str(query.get('language', [''])[0]).strip()
    model_name = str(query.get('model', [''])[0]).strip()
    if not all([project_name, language_name, model_name]):
        handler.send_response(400)
        handler.send_header('Content-Type', 'application/json; charset=utf-8')
        handler.end_headers()
        handler.wfile.write(json.dumps({'ok': False, 'error': 'Chýba project, language alebo model.'}).encode('utf-8'))
        return

    report_path = TASKS_DIR / project_name / language_name / model_name / 'report.csv'
    behavior_path = TASKS_DIR / project_name / language_name / model_name / 'report_Behavioral_Equivalence.csv'
    payload = {
        'ok': True,
        'project': project_name,
        'language': language_name,
        'model': model_name,
        'report_path': str(report_path),
        'behavior_path': str(behavior_path),
        'report_exists': report_path.exists(),
        'behavior_exists': behavior_path.exists(),
        'report_rows': [],
        'behavior_rows': [],
    }

    if report_path.exists():
        try:
            with report_path.open('r', encoding='utf-8-sig', newline='') as handle:
                payload['report_rows'] = list(csv.DictReader(handle))
        except (OSError, csv.Error, UnicodeError):
            payload['report_rows'] = []

    if behavior_path.exists():
        try:
            with behavior_path.open('r', encoding='utf-8-sig', newline='') as handle:
                payload['behavior_rows'] = list(csv.DictReader(handle))
        except (OSError, csv.Error, UnicodeError):
            payload['behavior_rows'] = []

    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))


def handle_json_report(handler):
    payload = get_json()
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))


class DashboardHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path in {'/', '/reporti', '/static/styles.css', '/static/app.js', '/run/output', '/api/model-report', '/json'}:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8' if parsed.path in {'/', '/reporti'} else 'text/css; charset=utf-8' if parsed.path == '/static/styles.css' else 'application/javascript; charset=utf-8' if parsed.path == '/static/app.js' else 'application/json; charset=utf-8' if parsed.path in {'/api/model-report', '/json'} else 'text/plain; charset=utf-8')
            self.end_headers()
            return
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/favicon.ico':
            self.send_response(204); self.end_headers(); return
        if parsed.path == '/':
            body = build_home_page().encode('utf-8')
            self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        if parsed.path == '/reporti':
            body = build_reporti_page().encode('utf-8')
            self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        if parsed.path == '/api/model-report':
            handle_model_report(self); return
        if parsed.path == '/json':
            handle_json_report(self); return
        if parsed.path == '/static/styles.css':
            data = (HERE / 'static' / 'styles.css').read_bytes(); self.send_response(200); self.send_header('Content-Type', 'text/css; charset=utf-8'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data); return
        if parsed.path == '/static/app.js':
            data = (HERE / 'static' / 'app.js').read_bytes(); self.send_response(200); self.send_header('Content-Type', 'application/javascript; charset=utf-8'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data); return
        if parsed.path == '/run/output':
            handle_run_output(self); return
        self.send_error(404, 'Not found')

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == '/run':
            handle_run_post(self); return
        if parsed.path == '/projects/average-toggle':
            handle_project_toggle(self); return
        if parsed.path == '/reporti/create':
            handle_project_create(self); return
        self.send_error(404, 'Not found')

    def log_message(self, fmt, *args):
        print(f'[{self.log_date_time_string()}] {fmt % args}')


def main():
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    chosen_port = PORT
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.bind((HOST, chosen_port))
    except OSError:
        chosen_port = find_available_port(PORT)
    server = ThreadingHTTPServer((HOST, chosen_port), DashboardHandler)
    print(f'Dashboard running on: http://{HOST}:{chosen_port}')
    print(f'CSV folder: {TASKS_DIR}')
    print('Stop: Ctrl+C')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping server...')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
