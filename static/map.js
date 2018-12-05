// Most of markers code from: https://www.sitepoint.com/google-maps-javascript-api-the-right-way/
// Rest of code adjusted from: https://developers.google.com/maps/documentation/javascript/adding-a-google-map
// Everything was modified for this projects use


document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelectorAll('#map').length > 0)
  {
    if (document.querySelector('html').lang)
      lang = document.querySelector('html').lang;
    else
      lang = 'en';
  }
});

var map, infoWindow;

// main map function that is being called
function initMap()
{
  var location = {lat: 39.739235, lng: -104.990250}; // Set defult location to Denver
  map = new google.maps.Map(document.getElementById('map'), {
    center: location,
    zoom: 14
  });
  infoWindow = new google.maps.InfoWindow; // only using infowindow for geolocation failure

  var iconBase = 'https://maps.google.com/mapfiles/ms/micons/'
  var icons = {
    Community: {
      name: "Community Service",
      icon: iconBase + 'red' + "-dot.png"
    },
    Homeless: {
      name: "Homeless",
      icon: iconBase + 'ltblue' + "-dot.png"
    },
    Children: {
      name: "Children",
      icon: iconBase + 'pink' + "-dot.png"
    },
    Food: {
      name: "Food",
      icon: iconBase + 'green' + "-dot.png"
    },
    Social: {
      name: "Social Work",
      icon: iconBase + 'yellow' + "-dot.png"
    },
    Health: {
      name: "Health",
      icon: iconBase + 'purple' + "-dot.png"
    },
    Pets: {
      name: "Pets",
      icon: iconBase + 'orange' + "-dot.png"
    },
  };


  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      // add blue dot icon for users current location
      var image = {
        url: 'http://www.static.flymeos.com/resources/flymeos/flyme6/images/designChange/circle1.png',
        scaledSize: new google.maps.Size(15, 15)
      };

      // add blue dot to map
      marker = new google.maps.Marker({
        position: pos,
        clickable: false,
        icon: image,
        map: map
      })

      infoWindow.setPosition(pos);
      infoWindow.setContent('Location found.');
      map.setCenter(pos);
    }, function() {
      handleLocationError(true, infoWindow, map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }

  var legend = document.getElementById('legend');
  for (var key in icons) {
    var type = icons[key];
    var name = type.name;
    var icon = type.icon;
    var div = document.createElement('div');
    div.innerHTML = '<img src="' + icon + '"> ' + name;
    legend.appendChild(div);
  }

  // Push Legend onto top right of map
  map.controls[google.maps.ControlPosition.RIGHT_TOP].push
  (document.getElementById('legend'));


  // fetch marker data from json file hosted on github
  fetch('https://raw.githubusercontent.com/Bassatron/Auxil/master/data.json')
    .then(function(response){return response.json()})
    .then(plotMarkers);
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}


var markers;
var bounds;


function plotMarkers(m)
{
  markers = [];
  bounds = new google.maps.LatLngBounds();

  m.forEach(function (marker) {
    // position each marker
    var position = new google.maps.LatLng(marker.lat, marker.lng);
    var title = marker.Name;

    // Set the color of Marker based on type
    let colorurl = "https://maps.google.com/mapfiles/ms/icons/";
    if (marker.type == "Homeless") {
      var color = "ltblue";
    } else if (marker.type == "Children") {
      var color = "pink";
    } else if (marker.type == "Food") {
      var color = "green"
    } else if (marker.type == "Social Work") {
      var color = "yellow"
    } else if (marker.type == "Health"){
      var color = "purple"
    } else if (marker.type == "Pets") {
      var color = "orange"
    } else {   // for "Community Service"
      var color = "red"
    }
    colorurl += color + "-dot.png";

    var content = '<h1 id="firstHeading" class="firstHeading">' + marker.Name + '</h1>' +
                  '<br>' +
                  '<p>' +
                    'Website: ' + marker.Website +
                  '</p>';


    infoWindow = new google.maps.InfoWindow();

    markers.push(
      new google.maps.Marker({
        position: position,
        icon: colorurl,
        title: title,
        info: content,
        map: map,
        animation: google.maps.Animation.DROP
      })
    );

    bounds.extend(position);
  });
}
