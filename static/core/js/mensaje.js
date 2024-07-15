function mensaje(){
    alert('Bienvenido a Obras ');
    console.log('testeando la consola');
}

function eliminar(codigo_producto){
    Swal.fire({
      title: 'Confirmar',
      text: 'Esta seguro que desea eliminar?',
      icon: 'info',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Confirmar'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire('Eliminado!','Producto Eliminado Correctamente', 'success')
        .then(function() {
            window.location.href = "/eliminar/"+codigo_producto+"/";
        })
      }
    })
}