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

    //Todo: Fix this.
    // var check_for_errors = function () {
    //               var errors = Cookies.get('error');
    //               if (errors){
    //                   Cookies.remove('error');
    //                   handle_error(errors)
    //               }
    // };

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
                             handle_error('Your passwords should be more than 8 characters.', 'error')
                         }
                         else{
                             Cookies.set('payload', payload);
                             window.location.href = 'register/plans';
                         }

                         }
            }
            else
                handle_error('You have to agree to our terms and conditions', 'error')
         })
    };

    var finishRegistration = function () {
                $("button[type=submit]").on('click', function() {
                  var plan_id = this.id;
                  var payload = Cookies.getJSON('payload');
                  payload['plan_id'] = plan_id;

                var  register_url  = $('#register_url').val();
                $.ajax({

                           url : register_url,
                           type:  "POST",
                           data : JSON.stringify(payload),
                           contentType: 'application/json',
                           dataType:"json",
                           success : function (response) {
                               console.log(response[0].data);
                               var ver_id = response[0].data.tempID;
                               var replace = '?action=verify&verID='+ver_id;
                               handle_redirect('/plans', replace)
                           },
                           error : function(xhr, errmsg, err){
                                        Cookies.set('errors', 'Hospital already exists');
                                        console.log(xhr)
                                        // handle_redirect('/plans', '')
                           }
                            })
                });
    };


    var updateHospitalDetails = function () {
        $("#updateHospital").on('click', function (event) {
            var payload = {
                'name': $('#name').val(),
                'email': $('#email').val(),
                'address': $('#address').val(),
                'description': $('#description').val()
            };
            var hospital_url= 'api/web/hospital';
            $.ajax({
                           url : hospital_url,
                           type:  "POST",
                           data : JSON.stringify(payload),
                           contentType: 'application/json',
                           dataType:"json",
                           success : function (response) {
                               console.log(response[0].data);
                               alert("Your Data has been saved");
                               //handle_redirect('/plans', replace)
                           },
                           error : function(){
                               alert("An issue occurred");
                           }
            })
        });

    };


    // check_for_errors();Todo: Uncomment this when function is fixed.

    handle_alerts('/dashboard/service-info', 'Choose Services', 'Choose the services of your choice to move on.');

    startRegistration();

    finishRegistration();

})(window.jQuery);