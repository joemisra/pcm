const midiPortsSelect = document.getElementById('midi-ports');
const openPortButton = document.getElementById('open-port');
const closePortButton = document.getElementById('close-port');
const patchDataPre = document.getElementById('patch-data');
const patchTypeSelect = document.getElementById('patch-type');

function getMidiPorts() {
  fetch('http://127.0.0.1:5000/api/midi/ports')
    .then(response => response.json())
    .then(ports => {
      midiPortsSelect.innerHTML = '';
      ports.forEach(port => {
        const option = document.createElement('option');
        option.value = port;
        option.textContent = port;
        midiPortsSelect.appendChild(option);
      });
    });
}

function openPort() {
  const selectedPort = midiPortsSelect.value;
  fetch('http://127.0.0.1:5000/api/midi/ports/open', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ port_name: selectedPort })
  });
}

function closePort() {
  fetch('http://127.0.0.1:5000/api/midi/ports/close', {
    method: 'POST'
  });
}

function getPatch() {
  fetch('http://127.0.0.1:5000/api/patch')
    .then(response => response.json())
    .then(patch => {
      patchDataPre.textContent = JSON.stringify(patch, null, 2);
    });
}

function selectPatch() {
  const selectedPatch = patchTypeSelect.value;
  fetch('http://127.0.0.1:5000/api/patch/select', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ patch_name: selectedPatch })
  }).then(() => {
    getPatch();
  });
}

openPortButton.addEventListener('click', openPort);
closePortButton.addEventListener('click', closePort);
patchTypeSelect.addEventListener('change', selectPatch);

getMidiPorts();
getPatch();
