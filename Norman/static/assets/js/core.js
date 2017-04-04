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
                         Cookies.set('payload', payload);
                         window.location.href = '/auth/register/plans';
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

                  console.log(payload)

                $.ajax({

                           url : register_url,
                           type:  "POST",
                           data : JSON.stringify(payload),
                           contentType: 'application/json',
                           dataType:"json",
                           success : function (json) {
                                        console.log(json);
                           },
                           error : function(xhr, errmsg, err){
                                        console.log(xhr)
                                        console.log(err)
                                        console.log(errmsg)
                           }
                            })
                });

    };

    startRegistration();

    finishRegistration();

})(window.jQuery);