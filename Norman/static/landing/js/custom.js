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
           userDetailsDict['hospitalEmail'] = $('#hospEmail').val();
           userDetailsDict['hospAddress'] = $('#hospAddress').val();
           userDetailsDict['hospSpecialty'] = $('#hospSpecialty').val();
           userDetailsDict['hospDesc'] = $('#hospDesc').val();
           console.log(userDetailsDict);
       })
    };

    goToHospital();
    doAuth();
    doPrivacy();
    doRegistration();

}).call(this, jQuery, window);
