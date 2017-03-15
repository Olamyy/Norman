/**
 * Created by lekanterragon on 3/12/17.
 */

(function($, window) {

    var doAuth = function () {
            $('#doAuth').on('click', function () {
                window.location.href = "/auth"
            })
    };
    var doPrivacy = function () {
            $('#privacy').on('click', function () {
                window.location.href = "/privacy"
            })
    };

    var redirectTo = function (uri) {
        window.location.href = uri;
    };

    var initRegistration = function () {
        $('#doRegister').on('click', function (event) {
            event.preventDefault();
            var email = $('#emailReg').val();
            var password = $('#password').val();
            Cookies.set('reg_details', { email: email, password: password });
                swal({
                  title: '<h4>Registration Type</h4>',
                   html: '<p>Are you a user or an hospital?<p> ',
                  showCancelButton: true,
                  showCloseButton: true,
                   confirmButtonText:
                    '<i class="fa fa-user"></i> User',
                  cancelButtonText:
                    '<i class="fa fa-hospital-o"></i> Hospital'
                }).then(function () {
                  swal(
                    redirectTo('/auth/register/user')
                  )
                }, function (dismiss) {
                  if (dismiss === 'cancel') {
                    swal(
                        redirectTo('/auth/register/hospital')
                    )
                  }
})


        });
    };

    var base_url = $('#base_url').val();

    var doRegistration = function () {
       var userDetailsDict = Cookies.getJSON('reg_details');
       $('#doCompleteRegistration').on('click', function (event) {
            event.preventDefault();
            var hospitalEmail = $('#hospEmail');
            var hospitalPassword = $('#hospPassword');
            if (!userDetailsDict.email){
                     hospitalEmail.attr("placeholder", "Enter hospital email");
            }else {
                    hospitalEmail.attr("placeholder", userDetailsDict.email);
            }
            if(!userDetailsDict.password){
                                     hospitalPassword.attr("placeholder", "Enter hospital password");
            } else {
                    hospitalPassword.attr("placeholder", userDetailsDict.password);
            }
            userDetailsDict['description'] = $('#hospDescription').val();
            userDetailsDict['specialty'] = $('#hospSpecialty').val();
            userDetailsDict['address'] = $('#hospAddress').val();
            if (!userDetailsDict) {
                toastr("The details you submitted are invalid/incomplete");
            } else {
                $.ajax(
                        {
                          type: "POST",
                          url: base_url + 'api/web/register?type=hospital',
                          data: {
                            "data": userDetailsDict
                          },
                          dataType: 'json',
                          async : false,
                          success: function (response) {
                              swal('Well Done');
                          },
                          error : function(response){
                                swal("Ooops", "The details you submitted are invalid/incomplete", 'error');
                          }
                        });
            }
        });

    };
    doAuth();
    doPrivacy();
    initRegistration();
    doRegistration();

}).call(this, jQuery, window);
