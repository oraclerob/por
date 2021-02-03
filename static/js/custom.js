function show_spinner(message) {
  toastr.clear();
  toastr.options = {
                     "maxOpened" : 1,
                     "autoDismiss" : true,
                     "closeButton": true,
                     "debug": false,
                     "newestOnTop": false,
                     "progressBar": false,
                     "positionClass": "toast-top-center",
                     "preventDuplicates": true,
                     "onclick": null,
                     //"showDuration": "300",
                     //"hideDuration": "1000",
                     "timeOut": "0",
                     "extendedTimeOut": "0",
                     "showEasing": "swing",
                     "hideEasing": "linear",
                     "showMethod": "fadeIn",
                     "hideMethod": "fadeOut",
                   };
 
 toastr.info("<div class=\"fa fa-spinner fa-spin\"></div> " + message, "");
 
 }

$(document).ready(function() {
/* off-canvas sidebar toggle */
$('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
    $('.collapse').toggleClass('in').toggleClass('hidden-xs').toggleClass('visible-xs');

});

$("#door-stamp").on("click", function (e) {
      $.ajax({
          type: 'GET',
          url: '/' + myappname + '/toggle-door',
          //success: updateSuccess(response),
          success: function (response) {
              console.log('Toggle Door clicked');
              //alert(JSON.stringify(response.results[0]));
              toastr.clear();
              if (response.results[0] == 1)
                  show_spinner("Closing Door...")
              else
                  show_spinner("Opening Door...")

              st = setTimeout(function() {
                location.reload();
              }
              .bind(this)
              , 15000);
  
          },
          complete: function () {
          }
      });
  });
});




function sessionTimer() {

        var sessionAlive = 300;

        var notifyBefore = 30; // Give client 30 seconds to choose.
        setTimeout(function() {

            Messenger.options = {
                extraClasses: 'messenger-fixed messenger-on-top',
                theme: 'flat'
            }

            msg = Messenger().post({
              message: "Session expiring, do you want to continue?",
              type: 'success',
              showCloseButton: true,
              actions: {
                retry: {
                  label: 'Extend session',
                  phrase: 'Extend session',
                  auto: true,
                  delay: 10,
                  action: function() {
                    history.go(0);
                  }
                },
                cancel: {
                  action: function() {
                    $(location).attr('href', myapploginurl);
                    return msg.cancel();
                  }
                }
              }
            });


        }, (sessionAlive - notifyBefore) * 1000);

        setTimeout(function() {
            $(location).attr('href', myapploginurl)
        }, (sessionAlive * 1000) + 100);

    };

