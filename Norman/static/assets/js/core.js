/**
 * Created by lekanterragon on 4/1/17.
 */

(function($) {

	"use strict";

    var  base_url  = $('#base_url').val();


    var handle_error = function (error, error_id) {
            var error_text = '<div class="alert alert-danger alert-dismissible" role="alert">' +
                             '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span' +
                             ' aria-hidden="true">&times;</span></button>'+ error + '</div>';
                               $('#'+error_id).html(error_text);
    };

    var handle_success = function (success, success_id) {
            var success_text = '<div class="alert alert-info alert-dismissible" role="alert">' +
                             '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span' +
                             ' aria-hidden="true">&times;</span></button>'+ success + '</div>';
                               $('#'+success_id).html(success_text);
    };

    var handle_alerts = function (uri, title, message) {
        if(uri){
            var current_uri = window.location.pathname;
            if(current_uri == uri){
                sweetAlert(title, message)
            }
        }else{
              swal(title, message)
        }
    };

    var handle_redirect = function (remove, replace) {
                         var url = window.location.href.replace(remove, '');
                         window.location.href = url+replace;
    };

	var generate_id = function (length)           {
                var text = "";
                var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

                for( var i=0; i < length; i++ )
                    text += possible.charAt(Math.floor(Math.random() * possible.length));

                return text;
};


	var startRegistration = function () {
         $('#mainregisterBtn').on('click', function (event) {
            event.preventDefault();
            if ($('#checkbox-signup').is(":checked")){
                     var payload = {'email': $('#email').val(),
                           'name': $('#name').val(),
                            'reg_num': $('#reg_num').val(),
                            'password': $('#password').val(),
                            'temp_id': generate_id(5),
                            'action' : 'create'
                            };
                     var  verify_password  = $('#verify_password').val();
                     if(payload['password'] != verify_password){
                         handle_error('Your passwords should match.', 'error')
                     }
                     else{
                         if(payload['password'].length < 5){
                             handle_error('Your passwords should be more than 5 characters.', 'error')
                         }
                         else{
                             var  register_url  = $('#register_url').val();
                             console.log(register_url);
                             $.ajax({
                                   url : register_url,
                                   type:  "POST",
                                   data : JSON.stringify(payload),
                                   contentType: 'application/json',
                                   dataType:"json",
                                   success : function (response) {
                                       var ver_id = response[0].data.tempID;
                                       var replace = '/register?action=verify&verID='+ver_id;
                                       handle_redirect('/register', replace)
                                   },
                                   error : function(xhr, errmsg, err){
                                                if (xhr.responseJSON.error_code == 'HOSPEXISTS'){
                                                    localStorage.setItem('errors', 'Hospital already exists');
                                                    // handle_redirect('/plans', '')
                                                    handle_error('Hospital already exists', 'HOSPEXISTS')
                                                }
                           }
                            })


                         }

                         }
            }
            else
                handle_error('You have to agree to our terms and conditions', 'error')
         })
    };


    var updateHospitalDetails = function () {
        $("#updateHospital").on('click', function (event) {
            event.preventDefault();
            var payload = {
                'name': $('#name').val(),
                'email': $('#email').val(),
                'address': $('#address').val(),
                'description': $('#description').val(),
                'action': 'update',
                'hospital_id': $('#hospital_id').val()
            };
            var hospital_url= $('#hospital_url').val();;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
            $.ajax({
                           url : hospital_url,
                           type:  "POST",
                           data : JSON.stringify(payload),
                           contentType: 'application/json',
                           dataType:"json",
                           success : function (response) {
                               console.log(response[0].data);
                               console.log("Your Data has been saved");
                               var success = "Successfully saved changes";
                               handle_success(success,'success');
                           },
                           error : function(xhr, errmsg, err){
                               console.log(xhr);
                               handle_error("Make sure your inputs are correct",'error');
                           }
            })
        });

    };

    var addPatient = function () {
      $('#addPatient').on('click', function(event){
          event.preventDefault();
          var payload= {
              'first_name': $('#first_name').val(),
              'last_name': $('#last_name').val(),
              'email': $('#email').val(),
              'hospital_id': $('#hospital_id').val(),
              'action':'create'
          };
          var patient_url = $('#patient_url').val();
          $.ajax({
                   url : patient_url,
                   type:  "POST",
                   data : JSON.stringify(payload),
                   contentType: 'application/json',
                   dataType:"json",
                success:function(response){
                       var success = "Successfully added New patient";
                       handle_success(success,'success');
                },
                error:function(xhr, errmsg,err){
                    console.log(xhr);
                    handle_error("Make sure your inputs are correct and use a unique email",'error');
                }
          })
      });
    };

    var requestService = function () {
        $('#requestService').on('click', function(event) {
            event.preventDefault();
            var payload = {
                'name': $('#service_name').val(),
                'short_description': $('#short_description').val(),
                'long_description': $('#long_description').val(),
                'action': 'create'
            };
        var service_url = $('#service_url').val();
        $.ajax({
            url: service_url,
            type: "POST",
            data: JSON.stringify(payload),
            contentType: 'application/json',
            dataType: "json",
            success: function (response) {
                console.log(response[0].data);
                console.log("data created");
                var success = "Successfully requested for a service";
                handle_success(success, 'success');
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr);
                handle_error("Make sure your inputs are correct", 'error');
            }
            })
        });
    };

    var check_for_errors = function () {
                 var  errors = localStorage.getItem('errors');
                  if (errors){
                      localStorage.removeItem('errors');
                      handle_error(errors)
                  }
    };

    check_for_errors();

    handle_alerts('/dashboard/service-info', 'Choose Services', 'Choose the services of your choice to move on.');

    startRegistration();

    updateHospitalDetails();

    addPatient();

    requestService();

})(window.jQuery);