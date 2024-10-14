document.addEventListener("DOMContentLoaded", function () {
    localStorage.setItem('token', '');
    const token = localStorage.getItem('token'); // Recuperar el token aquí

    // Función para listar personas
    function listarPersonas() {
        fetch('/personas', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const tbody = document.querySelector('tbody');
                tbody.innerHTML = ''; // Limpiar la tabla antes de llenarla

                data.forEach(d => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${d.id_personas}</td>
                        <td>${d.nombre}</td>
                        <td>${d.apellido}</td>
                        <td>${d.email}</td>
                        <td><button class="btn btn-primary btn-sm" id="btn-edit${d.id_personas}" data-bs-toggle="modal" data-bs-target="#modal${d.id_personas}">Editar</button></td>
                        <td><button class="btn btn-danger btn-sm" id="btn-delete${d.id_personas}">Eliminar</button></td>
                    `;
                    tbody.appendChild(row);

                    // Modal con IDs únicos en los inputs
                    const modal = document.createElement('div');
                    modal.classList.add('modal', 'fade');
                    modal.id = `modal${d.id_personas}`;
                    modal.tabIndex = -1;
                    modal.ariaLabelledby = "exampleModalLabel";
                    modal.ariaHidden = "true";
                    modal.innerHTML = `
                        <div class="modal-dialog">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h1 class="modal-title fs-5" id="exampleModalLabel">${d.nombre}</h1>
                              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="form-update${d.id_personas}">
                                    <label>Nombre</label>
                                    <input type="text" class="form-control mb-3" id="nombre${d.id_personas}" name="nombre" value="${d.nombre}">
                                    <label>Apellido</label>
                                    <input type="text" class="form-control mb-3" id="apellido${d.id_personas}" name="apellido" value="${d.apellido}">
                                    <label>Email</label>
                                    <input type="email" class="form-control mb-3" id="email${d.id_personas}" name="email" value="${d.email}">
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-primary" id="btn-save${d.id_personas}">Guardar cambios</button>
                            </div>
                                </form>
                          </div>
                        </div>
                    `;
                    document.body.appendChild(modal);

                    // Agregar evento para guardar los cambios (actualizar persona)
                    document.getElementById(`btn-save${d.id_personas}`).addEventListener('click', () => {
                        const formData = {
                            nombre: document.getElementById(`nombre${d.id_personas}`).value,
                            apellido: document.getElementById(`apellido${d.id_personas}`).value,
                            email: document.getElementById(`email${d.id_personas}`).value
                        };

                        fetch(`/personas/${d.id_personas}`, {
                            method: 'PATCH',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`
                            },
                            body: JSON.stringify(formData)  // Convertir a JSON
                        })
                        .then(response => {
                           if (!response.ok) {
                               return response.json().then(data => {
                                   // Si el servidor devuelve un error relacionado con el email
                                   if (data.error && data.error === 'El email ya está registrado') {
                                       alert(data.error);  // Mostrar alerta con el mensaje de error
                                   } else {
                                       throw new Error('Error al actualizar la persona');
                                   }
                               });
                           }
                            return response.json();
                        })
                        .then(data => {
                            console.log(data.message); // Mensaje de éxito
                            listarPersonas(); // Actualiza la lista de personas

                            // Cerrar el modal después de actualizar
                            const modalElement = document.getElementById(`modal${d.id_personas}`);
                            const modal = bootstrap.Modal.getInstance(modalElement); // Obtener la instancia del modal
                            modal.hide(); // Cerrar el modal
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    });

                    // Agregar el evento de eliminación
                    document.getElementById(`btn-delete${d.id_personas}`).addEventListener('click', () => {
                        const confirmDelete = confirm('¿Estás seguro de que quieres eliminar esta persona?');
                        if (confirmDelete) {
                            fetch(`/personas/${d.id_personas}`, {
                                method: 'DELETE',
                                headers: {
                                    'Accept': 'application/json',
                                    'Authorization': `Bearer ${token}`
                                }
                            })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Error al eliminar la persona');
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log(data.message); // Muestra el mensaje de éxito
                                listarPersonas(); // Actualiza la lista de personas
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                        }
                    });
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Inicializar la lista de personas al cargar la página
    listarPersonas();

    // Manejar el evento para guardar una nueva persona
    document.getElementById('formulario').addEventListener('submit', (event) => {
        event.preventDefault(); // Previene el envío del formulario

        let nombre = document.getElementById('nombre').value;
        let apellido = document.getElementById('apellido').value;
        let email = document.getElementById('email').value;

        // Verificar si alguno de los campos está vacío
        if (!nombre || !apellido || !email) {
            alert('Todos los campos son obligatorios');
            return;  // Evita continuar si los campos no están completos
        }

        fetch('/personas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`
            },
            body: new URLSearchParams({
                'nombre': nombre,
                'apellido': apellido,
                'email': email
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message); });
            }
            return response.json();
        })
        .then(data => {
            const form = document.getElementById('formulario');
            if (form) {
                form.reset();  // Resetea el formulario si existe
            }
            listarPersonas(); // Actualiza la lista de personas
        })
        .catch(error => {
            // Mostrar un alerta si el email está repetido o si falta un campo
            alert(error.message);
        });
    });

});
