var firstime = true;

function Boton_2s (pk) {
  setTimeout(function (){
    $(pk).click(function(){return true;}).click();
  },300);
}

function salir(){
  if(confirm("Deseas Salir Del Sistema?")){
    document.location='logout/';
  }else{
    OmegaNotify.fail("Intento De cierre de sesion fallido..!");
  }
}

function add_event_telefonos() {
  $("#add_equipos").click(function(event) {
    if ($(this).data('id') == "1") {
      $("#crear_pc").modal("show")
    }else if ($(this).data('id') == "2") {
      $("#crear_phone").modal("show")
    }else {
      OmegaNotify.alert({'warning':'Alerta','iconClass':'fa fa-plus', 'description':'<h5>Debes selecionar un tipo de equipo primero</h5>', 'buttonClass':'btn btn-info'});
    }
  });
  $("#add_equipos_dos").click(function(event) {
    if ($(this).data('id') == "1") {
      $("#crear_pc_dos").modal("show")
    }else if ($(this).data('id') == "2") {
      $("#crear_phone_dos").modal("show")
    }else {
      OmegaNotify.alert({'warning':'Alerta','iconClass':'fa fa-plus', 'description':'<h5>Debes selecionar un tipo de equipo primero</h5>', 'buttonClass':'btn btn-info'});
    }
  });
  $("#ordenes_boton_completar").click(function(event) {
    $("#modal_completar_orden_dos").modal("show");
    $("#orden_modal_completar").select2();
    $('.datetimepicker').datetimepicker({format: "YYYY-MM-DD",locale: 'es',});
  });
}


add_event_telefonos();


function add_event_tipo() {
  $('.datetimepicker').datetimepicker({format: "YYYY-MM-DD",locale: 'es',});
  $("#cliente").change(function(event) {
      $("#tipo").removeAttr('disabled');
      buscar_equipos();
  });
  $("select").select2();
  $(".add_user").click(function(event) {
    $("#crear_cliente").modal("show");
  });
  $("#tipo").change(function(event) {
      $("#equipo").removeAttr('disabled');
      buscar_equipos();
      if ($("#cliente").val()=='') {
        $("#add_equipos").addClass('disabled');
      }else {
        $("#add_equipos").removeClass('disabled');
      };
      $("#add_equipos").data('id', $(this).val())
  });
}

add_event_tipo();



function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
function llenar_select_clientes(data) {
  $('#cliente').empty();
    $.each(data.clientes, function(index, val) {
      $('#cliente').append($('<option>', {
        value: val.id,
        text: val.nombre
      }));
      $('#cliente').select2('val', data.nuevo);
    });
    $.each($('#crear_clientef input'), function(index, val) {
       $(this).val("");
    });
    $("#sexo").select2('val', '');
    $("#crear_cliente").modal("hide");
}

function vaciar_telefonos_direcciones() {
  $("#telefonoydirecciones").html('')
  $("#telefonoydirecciones").append('<div class="form-group" id="clienes_telefono"><label for="telefono">Telefono</label><span style="position: absolute; right: 0;" id="add_phone"><i class="btn btn-info fa fa-plus"></i></span><input type="text" class="form-control telefonos" id="telefono" name="telefono" placeholder="Telefono"></div><div class="form-group" id="clienes_direccion"><label for="direccion">Direccion</label><span style="position: absolute; right: 0;" id="add_address" ><i class="fa fa-plus btn btn-info"></i></span><input type="text" class="form-control direccions" id="direccion" name="direccion" placeholder="Direccion"></div>')
}

function vaciar_telefonos_direcciones_update() {
  $("#telefonoydirecciones_update").html('')
  $("#telefonoydirecciones_update").append('<div class="form-group" id="clienes_telefono_update"><label for="telefono_update">Telefono</label><span style="position: absolute; right: 0;" id="add_phone_update"><i class="btn btn-info fa fa-plus"></i></span></div><div class="form-group" id="clienes_direccion_update"><label for="direccion">Direccion</label><span style="position: absolute; right: 0;" id="add_address_update" ><i class="fa fa-plus btn btn-info"></i></span></div>')
}

function save_cliente() {
  var lista_telefonos = [];
  var lista_direcciones = [];
  $.each($("#clienes_telefono input"), function(index, val) {
    lista_telefonos.push($(this).val());
  });
  $.each($("#clienes_direccion input"), function(index, val) {
    lista_direcciones.push($(this).val());
  });
  $.ajax({
    url: 'crear_cliente/',
    type: 'POST',
    dataType: 'json',
    data: {cedula: $("#cedula").val(),
            nombre: $("#nombre").val(),
            apellido: $("#apellido").val(),
            sexo: $("#sexo").val(),
            fecha_de_nacimiento: $("#fecha_de_nacimiento").val(),
            telefonos: lista_telefonos,
            direcciones: lista_direcciones,
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    llenar_select_clientes(data);
    OmegaNotify.success('Guardado Exitosamente');
    vaciar_telefonos_direcciones();
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function buscar_equipos() {
  $.ajax({
    url: 'get_equipos/',
    type: 'POST',
    dataType: 'json',
    data: {cliente: $("#cliente").val(), tipo: $("#tipo").val()},
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    $('#equipo').empty();
    $.each(data, function(index, val) {
      $('#equipo').append($('<option>', {
        value: val.id,
        text: val.name
      }));
    });
    $('#equipo').select2('val','');
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}


function save_pc() {
  $.ajax({
    url: 'crear_equipo/',
    type: 'POST',
    dataType: 'json',
    data: { tipo: "1",
            cliente: $("#cliente").val(),
            marca: $("#Marca_pc").val(),
            modelo: $("#Modelo_pc").val(),
            tarjeta_madre: $("#tarjeta_madre_pc").val(),
            HDD: $("#HHD_pc").val(),
            CPU: $("#CPU_pc").val(),
            RAM: $("#RAM_pc").val(),
            unida_DVD: $("#Unidad_de_DVD_pc").val(),
            fuente_de_poder: $("#Fuente_de_poder_pc").val(),
            observaciones: $("#observaciones_pc").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    OmegaNotify.success('Guardado Exitosamente');
    buscar_equipos();
    $("#crear_pc").modal("hide");
    document.getElementById("crear_pcf").reset();
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function save_pc_dos() {
  $.ajax({
    url: 'crear_equipo/',
    type: 'POST',
    dataType: 'json',
    data: { tipo: "1",
            cliente: $("#cliente").val(),
            marca: $("#Marca_pc").val(),
            modelo: $("#Modelo_pc").val(),
            tarjeta_madre: $("#tarjeta_madre_pc").val(),
            HDD: $("#HHD_pc").val(),
            CPU: $("#CPU_pc").val(),
            RAM: $("#RAM_pc").val(),
            unida_DVD: $("#Unidad_de_DVD_pc").val(),
            fuente_de_poder: $("#Fuente_de_poder_pc").val(),
            observaciones: $("#observaciones_pc").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    OmegaNotify.success('Guardado Exitosamente');
    $("#crear_pc_dos").modal("hide");
    Boton_2s("#Pcs");
    document.getElementById("crear_pcf_dos").reset();
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function save_phone() {
  $.ajax({
    url: 'crear_equipo/',
    type: 'POST',
    dataType: 'json',
    data: { tipo: "2",
            cliente: $("#cliente").val(),
            marca: $("#Marca").val(),
            modelo: $("#Modelo").val(),
            serial: $("#Serial").val(),
            IMEI: $("#IMEI").val(),
            bateria: $("#Bateria").val(),
            observaciones: $("#observaciones").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    buscar_equipos();
    $("#crear_phone").modal("hide");
    document.getElementById("crear_phonef").reset();
    OmegaNotify.success('Guardado Exitosamente');
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function save_phone_dos() {
  $.ajax({
    url: 'crear_equipo/',
    type: 'POST',
    dataType: 'json',
    data: { tipo: "2",
            cliente: $("#cliente").val(),
            marca: $("#Marca").val(),
            modelo: $("#Modelo").val(),
            serial: $("#Serial").val(),
            IMEI: $("#IMEI").val(),
            bateria: $("#Bateria").val(),
            observaciones: $("#observaciones").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    $("#crear_phone_dos").modal("hide");
    Boton_2s("#Celulares");
    document.getElementById("crear_phonef_dos").reset();
    OmegaNotify.success('Guardado Exitosamente');
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function OpenInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

function save_peticion() {
  $.ajax({
    url: 'crear_peticion/',
    type: 'POST',
    dataType: 'json',
    data: { 
            cliente: $("#cliente").val(),
            object_id: $("#equipo").val(),
            tipo: $("#tipo").val(),
            fecha_de_recibido: $("#fecha_de_recibido").val(),
            observaciones: $("#Observaciones").val(),
            descripcion: $("#Descripcion").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    document.getElementById("agregar_peticion").reset();
    $.each($("#agregar_peticion select"), function(index, val) {
      $(this).select2('val', '');
      $(this).attr('disabled', 'disabled');
    });
    OmegaNotify.success('Guardado Exitosamente');
    $("#cliente").removeAttr('disabled')
    OpenInNewTab('Factura.pdf/'+data)
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function searchSuccess(data, textStatus, jqXHR){
    $('#contenido').html(data);
}

$("#Clientes").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_clientes/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
  
});

$("#Celulares").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_telefonos/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
  
});

$("#Pcs").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_pc/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#Users").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_user/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#O_Registradas").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_ordenes/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#O_Cumplidas").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_ordenes_cumplidas/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#O_Entregadas").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_ordenes_entregadas/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#Bitacora").click(function(event) {
  $.ajax({
    type: "POST",
    url: "lista_bitacora/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    });
});

$("#inicio").click(function(event) {
  $.ajax({
    type: "POST",
    url: "indexAjax/",
    success: searchSuccess,
    dataType: 'html',
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
    }).done(function(){
      $("select").select2();
    add_event_telefonos();
    add_event_tipo();
    });
});

function add_telefone_direccion() {
  $("#add_phone").click(function(event) {
    $("#clienes_telefono").append('<input type="text" class="form-control telefonos" id="telefono" name="telefono" placeholder="Telefono">')
  });

  $("#add_address").click(function(event) {
    $("#clienes_direccion").append('<input type="text" class="form-control direccions" id="direccion" name="direccion" placeholder="Direccion">')
  });
}

function add_telefone_direccion_update() {
  $("#add_phone_update").click(function(event) {
    $("#clienes_telefono_update").append('<input type="text" class="form-control telefonos" id="telefono_update" name="telefono_update" placeholder="Telefono">')
  });

  $("#add_address_update").click(function(event) {
    $("#clienes_direccion_update").append('<input type="text" class="form-control direccions" id="direccion_update" name="direccion_update" placeholder="Direccion">')
  });
}

add_telefone_direccion();

$("#reset_clientes").click(function(event) {
  vaciar_telefonos_direcciones();
  add_telefone_direccion();
});

$("#reset_clientes_update").click(function(event) {
  vaciar_telefonos_direcciones_update();
  add_telefone_direccion();
});



function get_cliente(id_cliente) {
  $.getJSON('update_cliente/', {id: id_cliente}, function(json, textStatus) {
      vaciar_telefonos_direcciones_update()
      $("#id_cliente").val(json.id);
      $("#nombre_update").val(json.nombre);
      $("#apellido_update").val(json.apellido);
      $("#cedula_update").val(json.cedula);
      $("#fecha_de_nacimiento_update").val(json.fecha_de_nacimiento);
      $("#sexo_update").select2('val', json.sexo);
      $.each(json.telefonos, function(index, val) {
        $("#clienes_telefono_update").append('<input type="text" class="form-control telefonos" id="telefono_update" name="telefono_update" value="'+val+'" placeholder="Telefono">')
      });
      $.each(json.direcciones, function(index, val) {
        $("#clienes_direccion_update").append('<input type="text" class="form-control direccions" id="direccion_update" name="direccion_update" value="'+val+'" placeholder="Direccion">')
      });
      add_telefone_direccion_update();
  });
}

function update_cliente() {
  var lista_telefonos = [];
  var lista_direcciones = [];
  $.each($("#clienes_telefono_update input"), function(index, val) {
    lista_telefonos.push($(this).val());
  });
  $.each($("#clienes_direccion_update input"), function(index, val) {
    lista_direcciones.push($(this).val());
  });
  $.ajax({
    url: 'update_cliente/',
    type: 'POST',
    dataType: 'json',
    data: { id: $("#id_cliente").val(),
            cedula: $("#cedula_update").val(),
            nombre: $("#nombre_update").val(),
            apellido: $("#apellido_update").val(),
            sexo: $("#sexo_update").val(),
            fecha_de_nacimiento: $("#fecha_de_nacimiento_update").val(),
            telefonos: lista_telefonos,
            direcciones: lista_direcciones,
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    $("#udate_cliente").modal("hide");
    OmegaNotify.success('Guardado Exitosamente');
    vaciar_telefonos_direcciones_update();
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

$("#self_change_password").click(function(event) {
  $("#id_user").val($(this).data('id'));
});

$(".self_update_user").click(function(event) {
  $("#id_user").val($(this).data('id'));
  $("#usuario").val($(this).data('username'));
  $("#first_name").val($(this).data('firstname'));
  $("#last_name").val($(this).data('lastname'));
  $("#email").val($(this).data('email'));
});

function send_password(){
  $.ajax({
      url: 'change_password/',
      type: 'POST',
      data: {
        id: $("#id_user").val(),
        password: $("#pwd1").val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      document.getElementById("FChangePassword").reset();
      $("#MChangePassword").modal("hide");
      OmegaNotify.success("Password Actualizada");
  });
}

function update_user(){
  $.ajax({
      url: 'update_user/',
      type: 'POST',
      data: {
        id: $("#id_user").val(),
        first_name: $("#first_name").val(),
        last_name: $("#last_name").val(),
        username: $("#usuario").val(),
        email: $("#email").val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      $(".self_update_user").data('id', resp.id);
      $("#nombre_del_usuario").text(resp.first_name+' '+resp.last_name);
      $(".self_update_user").data('username', resp.username);
      $(".self_update_user").data('firstname', resp.first_name);
      $(".self_update_user").data('lastname', resp.last_name);
      $(".self_update_user").data('email', resp.email);
      document.getElementById("FUpdateUser").reset();
      $("#MUpdateUser").modal("hide");
      OmegaNotify.success("Datos Modificados...!!");
  });
}

$("#cedula").change(function(event) {
  $.getJSON('/revisar_cedula/', {cedula: $(this).val()}, function(json, textStatus) {
    if (json) {
      OmegaNotify.fail('Cedula ya Reguistrada');
      $("#cedula").val('');
    };
  });
});



function get_telefono(id_cliente) {
  $.getJSON('update_phone/', {id: id_cliente}, function(json, textStatus) {
      $("#id_telefono").val(json.id);
      $("#cliente_up").select2('val', json.cliente);
      $("#Marca_up").val(json.marca);
      $("#Modelo_up").val(json.modelo);
      $("#Serial_up").val(json.serial);
      $("#IMEI_up").val(json.IMEI);
      $("#Bateria_up").val(json.bateria);
      $("#observaciones_up").val(json.observaciones);
  });
}

function update_phone() {
  $.ajax({
    url: 'update_phone/',
    type: 'POST',
    dataType: 'json',
    data: { id: $("#id_telefono").val(),
            cliente: $("#cliente_up").val(),
            marca: $("#Marca_up").val(),
            modelo: $("#Modelo_up").val(),
            serial: $("#Serial_up").val(),
            IMEI: $("#IMEI_up").val(),
            bateria: $("#Bateria_up").val(),
            observaciones: $("#observaciones_up").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    $("#update_phone").modal("hide");
    OmegaNotify.success('Guardado Exitosamente');
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function get_pc(id_cliente) {
  $.getJSON('update_pc/', {id: id_cliente}, function(json, textStatus) {
      $("#id_pc").val(json.id);
      $("#cliente_up").select2('val', json.cliente);
      $("#Marca_pc_up").val(json.marca);
      $("#Modelo_pc_up").val(json.modelo);
      $("#HHD_pc_up").val(json.HDD);
      $("#tarjeta_madre_pc_up").val(json.tarjeta_madre);
      $("#CPU_pc_up").val(json.CPU);
      $("#RAM_pc_up").val(json.RAM);
      $("#Unidad_de_DVD_pc_up").val(json.unida_DVD);
      $("#Fuente_de_poder_pc_up").val(json.fuente_de_poder);
      $("#observaciones_pc_up").val(json.observaciones);
  });
}

function update_pc() {
  $.ajax({
    url: 'update_pc/',
    type: 'POST',
    dataType: 'json',
    data: { 
            id: $("#id_pc").val(),
            cliente: $("#cliente_up").val(),
            marca: $("#Marca_pc_up").val(),
            modelo: $("#Modelo_pc_up").val(),
            HDD: $("#HHD_pc_up").val(),
            tarjeta_madre: $("#tarjeta_madre_pc_up").val(),
            CPU: $("#CPU_pc_up").val(),
            RAM: $("#RAM_pc_up").val(),
            unida_DVD: $("#Unidad_de_DVD_pc_up").val(),
            fuente_de_poder: $("#Fuente_de_poder_pc_up").val(),
            observaciones: $("#observaciones_pc_up").val(),
    },
    beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));},
  })
  .done(function(data) {
    $("#update_pc").modal("hide");
    OmegaNotify.success('Guardado Exitosamente');
  })
  .fail(function() {
  })
  .always(function() {
  });
  
}

function update_user2(){
  $.ajax({
      url: 'update_user/',
      type: 'POST',
      data: {
        id: $("#id_useuario").val(),
        first_name: $("#first_name_up").val(),
        last_name: $("#last_name_up").val(),
        username: $("#usuario_up").val(),
        email: $("#email_up").val(),
        tipo: $("#tipo_usuario").val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      $("#MUpdateUser2").modal("hide");
      OmegaNotify.success("Modificado Con Exito...!");
  });
}

function delete_peticion(id_celular){
  if(confirm("Deseas Borrar Peticion?")){
    $.ajax({
          url: 'delate_ordenes/',
          type: 'POST',
          data: {
            id: id_celular,
          },
          beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
      }).done(function(resp){
          $("#O_Registradas").click();
          OmegaNotify.success("Eliminada Con Exito.");
      });
  }else{
    OmegaNotify.fail("Has Cancelado la Eliminacion.");
  }
}
function completar_orden(){
   $.ajax({
      url: 'completar_orden/',
      type: 'POST',
      data: {
        id: $('#orden_modal_completar').val(),
        garantia: $('#garantia_orden_completar_orden_completar').val(),
        diagnostico: $('#diagnostico_orden_completar').val(),
        observaciones: $('#observaciones_orden_completar').val(),
        fecha_de_culminacion: $('#fecha_de_culminacion_orden_completar').val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      $("#modal_completar_orden_dos").modal("hide");
      document.getElementById("form_completar_orden").reset();
      OmegaNotify.success("Completada Con Exito." , "");
      Boton_2s("#O_Registradas");

  });
}

function entregar_orden_cumplida(){
  $("#modal_completar_orden_tres").modal("show");
  $("#orden_cumplida_modal , #cliente_entrega_orden").select2();
  $('.datetimepicker').datetimepicker({format: "YYYY-MM-DD",locale: 'es',});
}
function editar_orden_cumplida (id) {
  OmegaNotify.fail("Funcion En Desarrollo..");
}

function entregar_orden(){
   $.ajax({
      url: 'entregar_orden/',
      type: 'POST',
      data: {
        id: $('#orden_cumplida_modal').val(),
        fecha_entrega: $('#fecha_entrega_orden').val(),
        cliente: $('#cliente_entrega_orden').val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      $("#modal_completar_orden_tres").modal("hide");
      document.getElementById("form_completar_orden").reset();
      OmegaNotify.success("Completada Con Exito." , "");
     Boton_2s("#O_Cumplidas");

  });
}
function Pdf_all(){
  OmegaNotify.fail("Funcion En Desarrollo");
}
function Pdf_one (pk) {
  OmegaNotify.fail("Funcion En Desarrollo");
}

function create_user(){
  $.ajax({
      url: 'create_user/',
      type: 'POST',
      data: {
        first_name: $("#first_name_cre").val(),
        last_name: $("#last_name_cre").val(),
        username: $("#usuario_cre").val(),
        password: $("#pass_cre").val(),
        email: $("#email_cre").val(),
        tipo: $("#tipo_usuario_cre").val(),
      },
      beforeSend: function(xhr) {xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));}
  }).done(function(resp){
      $("#MCreateUser2").modal("hide");
      OmegaNotify.success("Usuario Creado");
  });
}

function get_user(id_cliente) {
  $.getJSON('update_user/', {id: id_cliente}, function(json, textStatus) {
      $("#id_useuario").val(json.id);
      $("#usuario_up").val(json.username);
      $("#first_name_up").val(json.first_name);
      $("#last_name_up").val(json.last_name);
      $("#email_up").val(json.email);
      if (json.admistrador) {
        $("#tipo_usuario").select2('val','1');
      }else{
        $("#tipo_usuario").select2('val','2');
      };
  });
}