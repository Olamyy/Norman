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
                             handle_error('Your passwords should be more than 5 characters.', 'error')
                         }
            else{

                var  user_api_url  = $('#use_api_url').val();

                $.ajax({
                    url : user_api_url,
                    type:  "POST",
                    data : JSON.stringify(payload),
                    contentType: 'application/json',
                    dataType: "json",
                    success : function (response) {
                               console.log(response[0].data);
                               alert("Your Data has been saved");
                               //handle_redirect('/plans', replace)
                           },
                    error : function(){
                               alert("An issue occurred");
                           }
                })
            }


        });
    }

})(window.jQuery);