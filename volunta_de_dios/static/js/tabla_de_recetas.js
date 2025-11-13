document.addEventListener('DOMContentLoaded', function() {
    const citasTableBody = document.querySelector('#citasTable tbody');
    const addRowButton = document.getElementById('addRow');
    let nextId = 2; // Start ID from 2 since 1 is already in the example row

    // Function to add a new row
    addRowButton.addEventListener('click', function() {
        const newRow = citasTableBody.insertRow();
        newRow.setAttribute('data-id', nextId);
        newRow.innerHTML = `
            <td>${nextId}</td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="editable-cell"><input type="text" value=""></td>
            <td class="action-buttons">
                <button class="btn-save"><i class="bi bi-save"></i></button>
                <button class="btn-edit d-none"><i class="bi bi-pencil"></i></button>
                <button class="btn-delete"><i class="bi bi-trash"></i></button>
            </td>
        `;
        nextId++;
        // Enable editing for the newly added row
        enableRowEditing(newRow);
    });

    // Event delegation for table actions (edit, save, delete)
    citasTableBody.addEventListener('click', function(event) {
        const target = event.target;
        const row = target.closest('tr'); // Get the closest row element

        if (!row) return; // If no row is found, exit

        if (target.closest('.btn-edit')) {
            enableRowEditing(row);
        } else if (target.closest('.btn-save')) {
            saveRowEditing(row);
        } else if (target.closest('.btn-delete')) {
            deleteRow(row);
        }
    });

    // Function to enable editing for a row
    function enableRowEditing(row) {
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const originalText = cell.textContent.trim();
            if (!cell.querySelector('input')) { // Prevent adding multiple inputs
                cell.innerHTML = `<input type="text" value="${originalText}">`;
            }
        });

        // Show save button, hide edit button
        row.querySelector('.btn-save').classList.remove('d-none');
        row.querySelector('.btn-edit').classList.add('d-none');
    }

    // Function to save row editing
    function saveRowEditing(row) {
        row.querySelectorAll('.editable-cell').forEach(cell => {
            const input = cell.querySelector('input');
            if (input) {
                cell.textContent = input.value;
            }
        });

        // Show edit button, hide save button
        row.querySelector('.btn-save').classList.add('d-none');
        row.querySelector('.btn-edit').classList.remove('d-none');
    }

    // Function to delete a row
    function deleteRow(row) {
        if (confirm('¿Estás seguro de que quieres eliminar esta fila?')) {
            row.remove();
        }
    }
});