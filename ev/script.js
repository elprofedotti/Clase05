let endpointData = {};

window.onload = function() {
    setupEndpointListeners();
    document.getElementById("obtenerDetalle").addEventListener("click", obtenerDetalle);
}

function setupEndpointListeners() {
    const selectEndpoint = document.getElementById('endpoints');
    selectEndpoint.addEventListener('change', (event) => {
        const endpoint = selectEndpoint.value;
        fetchTotalRegistros(endpoint);
    });
}

function fetchTotalRegistros(endpoint) {
    const url = `http://localhost:8080/${endpoint}`;
    console.log(url);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            //cargo el endpointData
            endpointData[endpoint] = data;
            const totalRegistros = data.length;
            const p_totalRegistros = document.getElementById('totalRegistros');
            p_totalRegistros.textContent = `Total de registros para ${endpoint}: ${totalRegistros}`;
            document.getElementById('resultado').innerHTML = 
                '<form>' +
                '   <label for="id">Ingresa el ID</label>' +
                `   <input type="number" id="id" name="id" min="1" max="${totalRegistros}">` +
                '   <button id="obtenerDetalle">Obtener Detalle</button>' +
                '</form><p id="mje"></p>';
            document.getElementById('resultado').style.display = 'block';
            document.getElementById("obtenerDetalle").addEventListener("click", obtenerDetalle);
            document.getElementById('detalle').style.display = 'none';
            document.getElementById('detalleUsuario').style.display = 'none';
        })
        .catch(error => console.error('Error:', error));
}

function obtenerDetalle(event) {

    event.preventDefault();
    var id = document.getElementById("id").value;
    
    // Obtener el valor seleccionado del elemento "endpoints"
    const endpoint = document.getElementById("endpoints").value; 
    
    const registros = endpointData[endpoint];
    const detalleRegistro = registros.find(registro => registro.id == id);
    
    if (detalleRegistro) {
        if(endpoint==="users"){
            obtenerDetalleUsuario(id);
                
        }
        else{
            const detalleHTML = generarDetalleHTML(detalleRegistro);
            document.getElementById('detalle').innerHTML = detalleHTML;
            document.getElementById('detalle').style.display = 'block';
        }
        document.getElementById('mje').innerHTML ='';
        
    } else {
        console.error('No se encontró el registro con el ID especificado');
        document.getElementById('mje').innerHTML ='Solo ponga valores entre 1 y el total de registros';
        document.getElementById('mje').style="Color: red";
    }
    
    
}

function generarDetalleHTML(registro) {
    let detalleHTML = '<ul>';
    for (let key in registro) {
        if(key=="id")continue;
        detalleHTML += `<li>${key}: ${registro[key]}</li>`;
        
        
    }
    
    // Mostrar botón para obtener detalle del usuario si existe el campo userId
    if ('userId' in registro){
        detalleHTML += `<br><button onclick="obtenerDetalleUsuario(${registro.userId})">Detalle del Usuario</button>`;
    }
    else{
        if ('albumId' in registro){
            detalleHTML +=`<br><img src="${registro.thumbnailUrl}">`
            detalleHTML += `<button onclick="mostrarFoto('${registro.url}')" style="margin-left:10px;">Ver Foto</button>`;
        }
        
    }
    detalleHTML += '</ul>';
    return detalleHTML;
}

function obtenerDetalleUsuario(userId) {
    const url = `http://localhost:8080/users?userId=${userId}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const detalleUsuarioHTML = generarDetalleUsuarioHTML(data);
            document.getElementById('detalleUsuario').innerHTML = detalleUsuarioHTML;
            document.getElementById('detalleModalLabel').innerHTML="Detalle de Usuario";
            document.getElementById('detalleUsuario').style.display = 'block';
            $('#detalleModal').modal('show'); // Abre el modal
        })
        .catch(error => console.error('Error:', error));
}


function generarDetalleUsuarioHTML(usuario) {
    let detalleUsuarioHTML = '<ul>';
    
    for (let key in usuario) {
        if (typeof usuario[key] === 'object') {
            detalleUsuarioHTML += `<li><button id='boton${key}' onclick="mostrarDetalle('${key}')">Mostrar ${key}</button></li>`;
            detalleUsuarioHTML += `<li id="${key}" style="display: none;">`;
            detalleUsuarioHTML += `<ul>`;
            
            for (let subKey in usuario[key]) {
                
                if (typeof usuario[key][subKey] === 'object') {
                    detalleUsuarioHTML += `<li>${subKey}:</li>`;
                    
                    detalleUsuarioHTML += `<ul>`;
                    for (let subSubKey in usuario[key][subKey]) {
                        detalleUsuarioHTML += `<li>${subSubKey}: ${usuario[key][subKey][subSubKey]}</li>`;
                    }
                    detalleUsuarioHTML += `</ul>`;
                    
                } else {
                    detalleUsuarioHTML += `<li>${subKey}: ${usuario[key][subKey]}</li>`;
                }
            }
            detalleUsuarioHTML += `</ul>`;
            detalleUsuarioHTML += `</li>`;
        } else {
            if(key==="id")continue;
            detalleUsuarioHTML += `<li>${key}: ${usuario[key]}</li>`;
        }
    }

    detalleUsuarioHTML += '</ul>';

    return detalleUsuarioHTML;
}

function mostrarDetalle(key) {
    const elemento = document.getElementById(key);
    const boton = document.getElementById(`boton${key}`); // Asegúrate de reemplazar "boton" con el id de tu botón

    if (elemento.style.display === 'block') {
        elemento.style.display = 'none';
        boton.innerText = `Mostrar ${key}`;
    } else {
        elemento.style.display = 'block';
        boton.innerText = `Ocultar ${key}`;
    }
}

function mostrarFoto(url) {
    document.getElementById('detalleModalLabel').innerHTML="Foto";
    document.getElementById('detalleUsuario').innerHTML =`<img src="${url}" width="450px" height="450px">`;
    document.getElementById('detalleUsuario').style.display = 'block';
    $('#detalleModal').modal('show'); // Abre el modal
}