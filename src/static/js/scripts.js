function addKeyValueField() {
    var valuesContainer = document.getElementById('values-container');

    // Create a container for each pair of fields
    var fieldContainer = document.createElement('div');
    fieldContainer.className = 'mb-3';

    var keyInput = document.createElement('input');
    keyInput.type = 'text';
    keyInput.className = 'form-control';
    keyInput.placeholder = 'Key';
    keyInput.name = 'keys[]'; // Use an array to send multiple keys in form data

    var valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.className = 'form-control';
    valueInput.placeholder = 'Value';
    valueInput.name = 'values[]'; // Use an array to send multiple values in form data

    // Create a button to remove this pair of fields with a trash icon
    var removeFieldBtn = document.createElement('button');
    removeFieldBtn.type = 'button';
    removeFieldBtn.className = 'btn btn-danger float-end remove-button';
    
    // Create an icon element for removal
    var removeIcon = document.createElement('i');
    removeIcon.className = 'fas fa-trash'; // Assuming you're using FontAwesome icons
    removeIcon.title='Remove Field'
    // Append the icon to the remove button
    removeFieldBtn.appendChild(removeIcon);
    
    removeFieldBtn.onclick = function () {
        valuesContainer.removeChild(fieldContainer);
        checkRemoveButtonVisibility();
    };

    // Append the key and value input fields, then the remove button
    fieldContainer.appendChild(keyInput);
    fieldContainer.appendChild(valueInput);
    fieldContainer.appendChild(removeFieldBtn);

    valuesContainer.appendChild(fieldContainer);

    checkRemoveButtonVisibility();
}

function checkRemoveButtonVisibility() {
    var valuesContainer = document.getElementById('values-container');
    var fieldContainers = valuesContainer.querySelectorAll('.mb-3');
    var removeKeyValueBtn = document.getElementById('removeKeyValueBtn');

    if (fieldContainers.length >= 2) {
        removeKeyValueBtn.style.display = 'inline-block';
    } else {
        removeKeyValueBtn.style.display = 'none';
    }
}
