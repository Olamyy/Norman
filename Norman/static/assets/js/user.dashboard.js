/**
 * Created by phvash on 4/26/17.
 */

(function($) {

    /** edit user data */
    var editProfile = function () {
        $('#edit').on('click', function (event) {

            event.preventDefault();

            var payload = {'email': $('#email').val(),
                           'name': $('#name').val(),
                            'reg_num': $('#reg_num').val(),
                            'password': $('#password').val(),
                            'temp_id': generate_id(5),
                            'action' : 'create'
                            };


        });
    }

})(window.jQuery);