/**
 * Created by lekanterragon on 3/12/17.
 */

(function($, window) {

    var doAuth = function () {
            $('#doAuth').on('click', function () {
                    redirectTo("/auth")
            })
    };
    var doPrivacy = function () {
            $('#privacy').on('click', function () {
                redirectTo("/privacy")
            })
    };

    var goToHospital = function () {
          $('#hospitalLanding').on('click', function () {
                 redirectTo("/hospital/landing")
            })
    };

    var redirectTo = function (uri) {
        return window.location.href = uri;
    };

    var base_url = $('#base_url').val();

    var doRegistration = function () {
       $('#doCompleteRegistration').on('click', function (event) {
            event.preventDefault();
            var userDetailsDict = {};
            userDetailsDict['hospitalEmail'] = $('#hospEmail');
            userDetailsDict['hospAddress'] = $('#hospAddress');
            userDetailsDict['hospPassword'] = $('#hospPassword');
            userDetailsDict['hospSpecialty'] = $('#hospSpecialty');
            userDetailsDict['hospDesc'] = $('#hospDesc');
            console.log(userDetailsDict);
            $.ajax(
                        {
                          type: "POST",
                          url: base_url + 'api/web/register',
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

        });

    };
    goToHospital();
    doAuth();
    doPrivacy();
    doRegistration();

}).call(this, jQuery, window);
