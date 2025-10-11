
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const filenameEl = document.getElementById('filename');
const browseBtn = document.getElementById('browse-btn');
const form = document.getElementById('convert-form');

const progressArea = document.getElementById('progress-area');
const bar = document.getElementById('bar');
const barPct = document.getElementById('bar-pct');
const logsEl = document.getElementById('logs');
const downloadLink = document.getElementById('download-link');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropzone.addEventListener(eventName, (e) => {
    e.preventDefault();
    e.stopPropagation();
  }, false);
});

['dragenter', 'dragover'].forEach(eventName => {
  dropzone.addEventListener(eventName, () => dropzone.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropzone.addEventListener(eventName, () => dropzone.classList.remove('highlight'), false);
});

dropzone.addEventListener('drop', (e) => {
  const files = e.dataTransfer.files;
  if (files && files[0]) {
    fileInput.files = files;
    filenameEl.textContent = files[0].name;
    resetProgress(); // Limpiar log y progreso al arrastrar nuevo archivo
  }
});

browseBtn.addEventListener('click', () => fileInput.click());

function resetProgress() {
  logsEl.textContent = '';
  setProgress(0);
  progressArea.classList.add('hidden');
  downloadLink.classList.add('hidden');
}

fileInput.addEventListener('change', () => {
  if (fileInput.files && fileInput.files[0]) {
    filenameEl.textContent = fileInput.files[0].name;
    resetProgress(); // Limpiar log y progreso al seleccionar nuevo archivo
  }
});

function setProgress(pct) {
  const v = Math.max(0, Math.min(100, Number(pct) || 0));
  bar.style.width = v + '%';
  barPct.textContent = v.toFixed(1) + '%';
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  resetProgress(); // Usar la función resetProgress()
  progressArea.classList.remove('hidden');

  const data = new FormData(form);
  const resp = await fetch('/convert', { method: 'POST', body: data });
  if (!resp.ok) {
    const txt = await resp.text();
    logsEl.textContent = 'Error al iniciar conversión: ' + txt;
    return;
  }
  const { job_id, download_url } = await resp.json();

  const es = new EventSource(`/progress/${job_id}`);
  es.addEventListener('log', (ev) => {
    logsEl.textContent += ev.data + '\n';
    logsEl.scrollTop = logsEl.scrollHeight;
  });
  es.addEventListener('progress', (ev) => {
    setProgress(parseFloat(ev.data));
  });
  es.addEventListener('status', (ev) => {
    const data = JSON.parse(ev.data);
    if (data.status === 'done') {
      setProgress(100);
      downloadLink.href = `/download/${job_id}`;
      downloadLink.classList.remove('hidden');
      es.close();
    } else if (data.status === 'error') {
      logsEl.textContent += '\nERROR: ' + (data.error || 'fallo desconocido');
      es.close();
    }
  });
});
