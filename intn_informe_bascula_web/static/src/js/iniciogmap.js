var map;
var ubicacion;
function initMapHome() {

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        document.getElementById("lat").value = pos.lat ;
        document.getElementById("lng").value = pos.lng;
//        document.getElementById("latCercano").value = pos.lat;
//        document.getElementById("lngCercano").value = pos.lng;
         comerciosCercanos();

      },
      function () {
        handleLocationError(true, infoWindow, map.getCenter());
      }
    );
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: No se pudo encontrar su ubicación."
      : "Error: Por favor active su GPS o revise los permisos."
  );
  infoWindow.open(map);
}
