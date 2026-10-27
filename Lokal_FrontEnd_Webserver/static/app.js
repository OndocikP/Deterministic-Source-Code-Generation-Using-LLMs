const runButtons = document.querySelectorAll('[data-run]');
const dialog = document.getElementById('run-dialog');
const closeDialogButtons = document.querySelectorAll('.close-dialog, #close-run-dialog');
const runOutput = document.getElementById('run-output');
const searchInput = document.getElementById('search');
const projectFilter = document.getElementById('project-filter');
const languageFilter = document.getElementById('language-filter');
const reportSearch = document.getElementById('report-search');
const projectDialog = document.getElementById('project-dialog');
const modelDetailDialog = document.getElementById('model-detail-dialog');
const modelDetailTitle = document.getElementById('model-detail-title');
const modelDetailContent = document.getElementById('model-detail-content');
const newProjectButton = document.getElementById('new-project-button');
const resetButton = document.getElementById('reset');
const projectCards = document.querySelectorAll('.report-card');
const projectRows = document.querySelectorAll('.project-row');
const closeModelDetailButton = document.getElementById('close-model-detail');

function openRunDialog() {
  dialog.classList.remove('hidden');
  dialog.setAttribute('aria-hidden', 'false');
}

function closeRunDialog() {
  dialog.classList.add('hidden');
  dialog.setAttribute('aria-hidden', 'true');
}

function closeModelDetail() {
  modelDetailDialog?.classList.add('hidden');
  modelDetailDialog?.setAttribute('aria-hidden', 'true');
}

function appendOutput(text) {
  runOutput.textContent += `${text}\n`;
  runOutput.scrollTop = runOutput.scrollHeight;
}

async function runCommand(commandName) {
  openRunDialog();
  runOutput.textContent = '';
  appendOutput(`> ${commandName}`);

  const response = await fetch('/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ command: commandName }),
  });

  const payload = await response.json();
  if (!payload.ok) {
    appendOutput(payload.error || 'Chyba pri spúšťaní skriptu.');
    return;
  }

  const process = payload.process || null;
  if (process) {
    appendOutput(`PID: ${process.pid}`);
  }

  const streamResponse = await fetch(`/run/output?command=${encodeURIComponent(commandName)}`);
  const streamText = await streamResponse.text();
  appendOutput(streamText || 'Skript dokončený.');

  const closeButton = document.getElementById('close-run-dialog');
  if (closeButton) {
    closeButton.disabled = false;
  }
}

for (const button of runButtons) {
  button.addEventListener('click', () => {
    const scriptName = button.dataset.run;
    runCommand(scriptName);
  });
}

for (const closeButton of closeDialogButtons) {
  closeButton.addEventListener('click', () => {
    if (closeButton.id === 'close-run-dialog' || closeButton === document.getElementById('close-run-dialog')) {
      closeRunDialog();
      return;
    }
    closeModelDetail();
    projectDialog?.classList.add('hidden');
    projectDialog?.setAttribute('aria-hidden', 'true');
  });
}

async function openModelDetail(project, language, model) {
  if (!modelDetailDialog || !modelDetailTitle || !modelDetailContent) {
    return;
  }
  modelDetailTitle.textContent = `${model} · ${language}`;
  modelDetailContent.innerHTML = '<div class="notice">Načítavam report…</div>';
  modelDetailDialog.classList.remove('hidden');
  modelDetailDialog.setAttribute('aria-hidden', 'false');

  try {
    const response = await fetch(`/api/model-report?project=${encodeURIComponent(project)}&language=${encodeURIComponent(language)}&model=${encodeURIComponent(model)}`);
    const payload = await response.json();
    if (!payload.ok) {
      modelDetailContent.innerHTML = `<div class="notice">${payload.error || 'Report sa nepodarilo načítať.'}</div>`;
      return;
    }

    const reportRows = Array.isArray(payload.report_rows) ? payload.report_rows : [];
    const behaviorRows = Array.isArray(payload.behavior_rows) ? payload.behavior_rows : [];
    const metricNames = ['Code_Identity', 'AST_Structure', 'Behavioral_Equivalence'];
    const fileLink = (filePath, label) => {
      const safePath = String(filePath || '').replace(/\\/g, '/');
      const href = safePath.startsWith('file:') ? safePath : `file://${safePath}`;
      return `<a class="file-link" href="${href}" target="_blank" rel="noreferrer">${label}</a>`;
    };

    const rowsHtml = reportRows.length ? reportRows.map((row) => {
      const fileName = row.File_name || row.file_name || row['File_name'] || 'Unknown';
      const metrics = metricNames.map((key) => {
        const value = row[key];
        const numeric = Number(value);
        const score = Number.isFinite(numeric) ? numeric.toFixed(2) : '—';
        return `<span class="metric-pill ${value === '' || !Number.isFinite(numeric) ? 'missing' : (numeric >= 0.8 ? 'high' : numeric >= 0.5 ? 'medium' : 'low')}">${score}</span>`;
      }).join('');
      return `<tr><td>${fileName}</td><td>${metrics}</td></tr>`;
    }).join('') : '<tr><td colspan="2">Žiadne riadky v report.csv.</td></tr>';

    const behaviorHtml = behaviorRows.length ? behaviorRows.map((row) => {
      const fileName = row.File_name || row.file_name || row['File_name'] || 'Unknown';
      const metrics = metricNames.map((key) => {
        const value = row[key];
        const numeric = Number(value);
        const score = Number.isFinite(numeric) ? numeric.toFixed(2) : '—';
        return `<span class="metric-pill ${value === '' || !Number.isFinite(numeric) ? 'missing' : (numeric >= 0.8 ? 'high' : numeric >= 0.5 ? 'medium' : 'low')}">${score}</span>`;
      }).join('');
      return `<tr><td>${fileName}</td><td>${metrics}</td></tr>`;
    }).join('') : '<tr><td colspan="2">Žiadne riadky v report_Behavioral_Equivalence.csv.</td></tr>';

    modelDetailContent.innerHTML = `
      <div class="detail-links">
        ${payload.report_exists ? fileLink(payload.report_path, 'report.csv') : '<span class="muted">report.csv chýba</span>'}
        ${payload.behavior_exists ? fileLink(payload.behavior_path, 'report_Behavioral_Equivalence.csv') : '<span class="muted">report_Behavioral_Equivalence.csv chýba</span>'}
      </div>
      <div class="detail-table-wrap">
        <table class="detail-table">
          <thead><tr><th>Model / súbor</th><th>Code Identity · AST Structure · Behavioral Equivalence</th></tr></thead>
          <tbody>${rowsHtml}</tbody>
        </table>
      </div>
      <div class="detail-tags">
        <span class="detail-chip">Projekt: ${project}</span>
        <span class="detail-chip">Jazyk: ${language}</span>
      </div>
      <div class="detail-table-wrap">
        <table class="detail-table">
          <thead><tr><th>Behavioral file</th><th>Hodnoty</th></tr></thead>
          <tbody>${behaviorHtml}</tbody>
        </table>
      </div>
    `;
  } catch (error) {
    modelDetailContent.innerHTML = `<div class="notice">Nepodarilo sa načítať detail modelu: ${error.message || error}</div>`;
  }
}

function filterReports() {
  const q = (searchInput?.value || '').trim().toLowerCase();
  const project = projectFilter?.value || '';
  const language = languageFilter?.value || '';
  let visible = 0;

  for (const card of projectCards) {
    const matches = (!project || card.dataset.project === project)
      && (!language || card.dataset.language === language)
      && (!q || card.textContent.toLowerCase().includes(q));
    card.hidden = !matches;
    if (matches) visible++;
  }

  const visibleCount = document.getElementById('visible-count');
  if (visibleCount) {
    visibleCount.textContent = `${visible} z ${projectCards.length} reportov`;
  }
}

if (searchInput) {
  searchInput.addEventListener('input', filterReports);
}
if (projectFilter) {
  projectFilter.addEventListener('change', filterReports);
}
if (languageFilter) {
  languageFilter.addEventListener('change', filterReports);
}
if (resetButton) {
  resetButton.addEventListener('click', () => {
    searchInput.value = '';
    projectFilter.value = '';
    languageFilter.value = '';
    filterReports();
  });
}

if (reportSearch) {
  reportSearch.addEventListener('input', () => {
    const query = reportSearch.value.trim().toLowerCase();
    for (const row of projectRows) {
      const text = row.textContent.toLowerCase();
      row.hidden = !!query && !text.includes(query);
    }
  });
}

if (newProjectButton) {
  newProjectButton.addEventListener('click', () => {
    projectDialog.classList.remove('hidden');
    projectDialog.setAttribute('aria-hidden', 'false');
  });
}

for (const closeButton of document.querySelectorAll('.close-dialog')) {
  closeButton.addEventListener('click', () => {
    if (closeButton.id === 'close-model-detail' || closeButton.closest('#model-detail-dialog')) {
      closeModelDetail();
      return;
    }
    projectDialog?.classList.add('hidden');
    projectDialog?.setAttribute('aria-hidden', 'true');
  });
}

if (closeModelDetailButton) {
  closeModelDetailButton.addEventListener('click', closeModelDetail);
}

for (const modelButton of document.querySelectorAll('.model-link-button')) {
  modelButton.addEventListener('click', () => {
    openModelDetail(
      modelButton.dataset.project,
      modelButton.dataset.language,
      modelButton.dataset.model,
    );
  });
}

const toggleInputs = document.querySelectorAll('[data-project-toggle]');
for (const toggle of toggleInputs) {
  toggle.addEventListener('change', async () => {
    const projectName = toggle.dataset.projectToggle;
    const includeInAverages = toggle.checked;
    await fetch('/projects/average-toggle', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ project_name: projectName, include_in_averages: includeInAverages }),
    });
  });
}

if (document.getElementById('project-form')) {
  document.getElementById('project-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload.models = formData.getAll('models');
    payload.setup_extra = payload.setup_extra || '';

    const response = await fetch('/reporti/create', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });
    const result = await response.json();

    if (result.ok) {
      window.location.href = '/reporti';
    } else {
      alert(result.error || 'Nepodarilo sa vytvoriť projekt.');
    }
  });
}
