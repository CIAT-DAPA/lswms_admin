$(document).ready(function() {
    $('#example').DataTable({
        "lengthMenu": [3, 10, 25, 50], // Define las opciones de selección de cantidad por página
        "pageLength": 3 // Establece el valor predeterminado a 5 elementos por página
    });
});
