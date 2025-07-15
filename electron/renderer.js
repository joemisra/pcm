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

const modulationMatrix = document.getElementById('modulation-matrix').getElementsByTagName('tbody')[0];
const addModulationButton = document.getElementById('add-modulation');

function renderModulationMatrix(modulations) {
    modulationMatrix.innerHTML = '';
    modulations.forEach((mod, index) => {
        const row = modulationMatrix.insertRow();
        row.innerHTML = `
            <td><input type="number" value="${mod.source}" data-index="${index}" data-field="source"></td>
            <td><input type="number" value="${mod.destination}" data-index="${index}" data-field="destination"></td>
            <td><input type="number" step="0.01" value="${mod.amount}" data-index="${index}" data-field="amount"></td>
            <td><button class="remove-modulation" data-index="${index}">Remove</button></td>
        `;
    });
}

addModulationButton.addEventListener('click', () => {
    const source = parseInt(prompt('Enter source address:'));
    const destination = parseInt(prompt('Enter destination address:'));
    const amount = parseFloat(prompt('Enter amount:'));

    if (!isNaN(source) && !isNaN(destination) && !isNaN(amount)) {
        fetch('http://127.0.0.1:5000/api/patch/modulation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source, destination, amount })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    alert(`Error: ${err.message}`);
                });
            }
            getPatch();
        });
    }
});

modulationMatrix.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-modulation')) {
        const index = event.target.dataset.index;
        fetch(`http://127.0.0.1:5000/api/patch/modulation/${index}`, {
            method: 'DELETE'
        })
        .then(() => {
            getPatch();
        });
    }
});

const macros = document.getElementById('macros').getElementsByTagName('tbody')[0];
const addMacroButton = document.getElementById('add-macro');

function getPatch() {
  fetch('http://127.0.0.1:5000/api/patch')
    .then(response => response.json())
    .then(patch => {
      patchDataPre.textContent = JSON.stringify(patch, null, 2);
      if (patch.modulation_matrix) {
        renderModulationMatrix(patch.modulation_matrix.modulations);
      }
      if (patch.macros) {
        renderMacros(patch.macros);
      }
    });
}

function renderMacros(macrosData) {
    macros.innerHTML = '';
    for (const address in macrosData) {
        const macro = macrosData[address];
        const row = macros.insertRow();
        row.innerHTML = `
            <td>${macro.name}</td>
            <td>${macro.parameters.join(', ')}</td>
            <td>${macro.min_value}</td>
            <td>${macro.max_value}</td>
            <td><button class="remove-macro" data-address="${address}">Remove</button></td>
        `;
    }
}

addMacroButton.addEventListener('click', () => {
    const name = prompt('Enter macro name:');
    const parametersStr = prompt('Enter comma-separated parameter addresses:');
    const parameters = parametersStr.split(',').map(p => parseInt(p.trim()));
    const minValue = parseInt(prompt('Enter min value:', 0));
    const maxValue = parseInt(prompt('Enter max value:', 127));

    if (name && parameters.length > 0) {
        fetch('http://127.0.0.1:5000/api/patch/macro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, parameters, min_value: minValue, max_value: maxValue })
        })
        .then(() => {
            getPatch();
        });
    }
});

macros.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-macro')) {
        const address = event.target.dataset.address;
        fetch(`http://127.0.0.1:5000/api/patch/macro/${address}`, {
            method: 'DELETE'
        })
        .then(() => {
            getPatch();
        });
    }
});

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
