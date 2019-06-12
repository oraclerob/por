$(document).ready(function() {
/* off-canvas sidebar toggle */
$('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
    $('.collapse').toggleClass('in').toggleClass('hidden-xs').toggleClass('visible-xs');
});


      toastr.clear();

      toastr.options = {
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

     $('#search').on('change keyup paste', function(){
	    toastr.info("<div class=\"fa fa-spinner fa-spin\"></div> Loading.... ", "");
	    setTimeout( function () { $('#search_form').submit();  }, 1000);

     });

});

function show_spinner(frame) {
 toastr.options = {
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

toastr.info("<div class=\"fa fa-spinner fa-spin\"></div> Loading.... ", "");

}



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
                    $(location).attr('href', '/por/login/');
                    return msg.cancel();
                  }
                }
              }
            });


        }, (sessionAlive - notifyBefore) * 1000);

        setTimeout(function() {
            $(location).attr('href', '/por/login/')
        }, (sessionAlive * 1000) + 100);

    };

  var map = null;

 function initAutocomplete() {
        var cityBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(-31.037797299068444, 114.78436081903419),
        new google.maps.LatLng(-33.037797299068444, 116.78436081903419));
        var bounds = new google.maps.LatLngBounds();

        var CircleOptions = {
          strokeColor: '#FF0000',
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: '#F00000',
          fillOpacity: 0.10,
          radius: 10,
          clickable: true
        };

        var cityCircle = new google.maps.Circle(CircleOptions);

        infoWindow = new google.maps.InfoWindow;


        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');

            infoWindow.open(map);
            map.setCenter(pos);
            map.setZoom(20);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }


       // This example adds a search box to a map, using the Google Place Autocomplete
      // feature. People can enter geographical searches. The search box will return a
      // pick list containing a mix of places and predicted search terms.

      // This example requires the Places library. Include the libraries=places
      // parameter when you first load the API. For example:
      // <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

          map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -32.037797299068444,lng: 115.78436081903419},
          zoom: 13,
          mapTypeId: 'roadmap',
          strict : true,
          bounds: cityBounds,
          types: ['establishment'],
        });

        // Create the search box and link it to the UI element.
        var input = document.getElementById('pac-input');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });


        // Listen for the event fired when the user selects a prediction and retrieve
        // more details for that place.
        searchBox.addListener('places_changed', function() {
          var clickHandler;
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // For each place, get the icon, name and location.
          bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }
            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
              map.setCenter(place.geometry.location);
              map.setZoom(20);  // Why 17? Because it looks good.
            } else {
              bounds.extend(place.geometry.location);
              map.setCenter(place.geometry.location);
              map.setZoom(20);  // Why 17? Because it looks good.
            }

            //markers = [];
            //var marker = new google.maps.Marker({
            //map: map,
            //title: place.name,
            //position: place.geometry.location
            //});

             //markers.push(marker);

             //google.maps.event.addListener(marker, 'click', function() {
             //    map.setZoom(20);
             //    map.setCenter(marker.getPosition());
             // });

             //TODO not working
             //cityCircle.setMap(map);
             //cityCircle.setCenter(place.geometry.location);
             //map.fitBounds(cityCircle.getBounds());

             //google.maps.event.addListener(cityCircle ,"click",function(e){
             //  clickHandler = new ClickEventHandler(cityCircle.getMap(), {lat: -32.037797299068444, lng: 115.78436081903419});
             //});


          });


        });

        clickHandler = new ClickEventHandler(map, {lat: -32.037797299068444, lng: 115.78436081903419});

      }



      var ClickEventHandler = function(map, origin) {
        this.origin = origin;
        this.map = map;
        this.placesService = new google.maps.places.PlacesService(map);
        this.infowindow = new google.maps.InfoWindow();
        // Listen for clicks on the map.
        this.map.addListener('click', this.handleClick.bind(this));
      };

      ClickEventHandler.prototype.getPlaceInformation = function(placeId) {

        var me = this;
        this.placesService.getDetails({placeId: placeId}, function(place, status) {
          me.infowindow.close();
          if (status === 'OK') {

             var inputNames = [ 'name', 'formatted_address', 'url',  'website'];
            for ( var val in inputNames ) {
               document.getElementById(inputNames[val]).value = place[inputNames[val]];
            }
            document.getElementById('lat').value = place.geometry.location.lat();
            document.getElementById('lng').value = place.geometry.location.lng();
            document.getElementById('place_id').value = placeId;
            var template = '<div id="infoContent">';
            template += '<ul>';
            template += '<li><span>Name: </span>'+place.name+'</li>';
            template += '<li><span>Address: </span>'+place.formatted_address+'</li>';
            //template += '<li><span>Place Id: </span>'+placeId+'</li>';
            //template += '<li><span>Google Maps URL: </span><a href="'+place.url+'" target="_blank">'+place.url+'</a></li>';
            //template += '<li><span>Latitude: </span>'+place.geometry.location.lat()+'</li>';
            //template += '<li><span>Longitude: </span>'+place.geometry.location.lng()+'</li>';
            template += '<li><span>Website: </span><a href="'+place.website+'" target="_blank">'+place.website+'</a></li>';
            template += '</ul>';
            me.infowindow.setContent(template);
            me.infowindow.setPosition(place.geometry.location);
            me.infowindow.open(me.map);
            $('#name').trigger('keyup');
          }
        });
      };


  ClickEventHandler.prototype.handleClick = function(event) {
    console.log('You clicked on: ' + event.latLng);
    // If the event has a placeId, use it.
    if (event.placeId) {

        //console.log('You clicked on place:' + event.placeId);
      // Calling e.stop() on the event prevents the default info window from
      // showing.
      // If you call stop here when there is no placeId you will prevent some
      // other map click event handlers from receiving the event.
      event.stop();
      this.getPlaceInformation(event.placeId);
    }
  };


  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed. You must allow this website to access your location if you want the location automatically found.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }



