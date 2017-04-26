/**
 * Created by phvash on 4/26/17.
 */

(function($) {

    /** handle all errors */
    var handle_error = function (error, error_id) {
            var error_text = '<div class="alert alert-danger alert-dismissible" role="alert">' +
                             '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span' +
                             ' aria-hidden="true">&times;</span></button>'+ error + '</div>';
                               $('#'+error_id).html(error_text);
    };

    /** update user data */
    var updateUser = function () {
        $('#update').on('click', function (event) {

            event.preventDefault();

            var payload = {
                            'first_name': $('#first_name').val(),
                            'last_name': $('#last_name').val(),
                            'email': $('#email').val(),
                            'password': $('#password').val(),
                            'action' : 'update'
                           };

            if(payload['password'].length < 5){
                             handle_error('Your passwords should be more than 8 characters.', 'error')
                         }
            else{

                var  register_url  = $('#register_url').val();

                $.ajax({
                    url : register_url,
                    type:  "POST",
                    data : JSON.stringify(payload),
                    contentType: 'application/json',
                    dataType: "json",
                    success : function (response) {
                                       var ver_id = response[0].data.tempID;
                                       var replace = '?action=verify&verID='+ver_id;
                                       handle_redirect('/register', replace)
                                   },
                    error : function(xhr, errmsg, err){
                                     console.log(xhr);
                                     if (xhr.responseJSON.error_code == 'HOSPEXISTS'){
                                         localStorage.setItem('errors', 'Hospital already exists');
                                         handle_redirect('/plans', '')
                                     }
                                                // handle_redirect('/plans', '')
                           }
                })
            }


        });
    }

})(window.jQuery);