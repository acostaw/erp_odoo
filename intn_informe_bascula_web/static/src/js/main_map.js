var openInfoWindow;

document.getElementById("searchTerm").value = "";
document.getElementById("ciudad").value = "";
  document.getElementById('dpto').value='0';
  document.getElementById('estado').value='0';

document.getElementById("cancelButton").addEventListener("click", borrar);

document.getElementById("searchButton").addEventListener("click", buscar);

var input = document.getElementById("searchTerm");
input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   event.preventDefault();
   document.getElementById("searchButton").click();
  }
});


function borrar() {
  var val = document.getElementById("searchTerm").value;
  var city = document.getElementById("ciudad").value;
  var d = document.getElementById("dpto");
  var dpto = d.value;
  var e = document.getElementById("estado");
  var estado = e.value;

  //if (val != '' && city != '' && dpto != '0' && estado != '0'){
  initMap();
  //}

  document.getElementById("searchTerm").value = "";
  document.getElementById("ciudad").value = "";
  document.getElementById('dpto').value='0';
  document.getElementById('estado').value='0';

}

function buscar(){
    var val = document.getElementById("searchTerm").value;
    console.log(val);
    var city = document.getElementById("ciudad").value;
    var d = document.getElementById("dpto");
    var dpto = d.value;
    var e = document.getElementById("estado");
    var estado = e.value;
    url = 'http://erptest.intn.gov.py/search-bascula?searchTerm='+ val +'&dpto='+ dpto + '&ciudad='+ city +'&estado=' + estado;


    const myLatLng = { lat: -25.2819, lng: -57.635};
  const map = new google.maps.Map(document.getElementById("map_div"), {
    zoom: 8,
    center: myLatLng,
  });


  fetch(url)
          .then(function(response) {
            return response.json();
          })
          .then(function(myJson) {

            // Sets the map on all markers in the array.
            function setMapOnAll(map) {
              for (let i = 0; i < markers.length; i++) {
                markers[i].setMap(map);
              }
            }


            var items = '';
            items = myJson;

            for (var i of this.Object.keys(items)){
                var partner_lat = items[i].partner_lat;
                var partner_lng = items[i].partner_lng;

                var latlngset = new google.maps.LatLng(partner_lat, partner_lng);

                var marker = new google.maps.Marker({
                    map: map, title: items[i].name, position: latlngset
                });
                map.setCenter(marker.getPosition())

                var content = "<b>" + items[i].name + "</p>"+ items[i].basculas ;

                var infowindow = new google.maps.InfoWindow() ;

                google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
                    return function () {

                        if (openInfoWindow)
                            openInfoWindow.close();

                        infowindow.setContent(content);
                        openInfoWindow = infowindow;
                        infowindow.open(map, marker);

                    };
                })(marker, content, infowindow));


            }
          });


}


function initMap() {

  const myLatLng = { lat: -25.363, lng: 131.044 };
  const map = new google.maps.Map(document.getElementById("map_div"), {
    zoom: 8,
    center: myLatLng,
  });


  const styles = {
  default: [],
  hide: [
    {
      featureType: "poi.business",
      stylers: [{ visibility: "off" }],
    },
    {
      featureType: "transit",
      elementType: "labels.icon",
      stylers: [{ visibility: "off" }],
    },
  ],
};
 map.setOptions({ styles: styles["hide"] });




  fetch('http://erptest.intn.gov.py/partners')
          .then(function(response) {
            return response.json();
          })
          .then(function(myJson) {
            var items = '';
            items = myJson;

            for (var i of this.Object.keys(items)){
                var partner_lat = items[i].partner_lat;
                var partner_lng = items[i].partner_lng;

                var latlngset = new google.maps.LatLng(partner_lat, partner_lng);

                var marker = new google.maps.Marker({
                    map: map, title: items[i].name, position: latlngset
                });
                map.setCenter(marker.getPosition())

                var content = "<b>" + items[i].name + "</p>"+ items[i].basculas ;

                var infowindow = new google.maps.InfoWindow() ;

                google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
                    return function () {

                        if (openInfoWindow)
                            openInfoWindow.close();

                        infowindow.setContent(content);
                        openInfoWindow = infowindow;
                        infowindow.open(map, marker);

                    };
                })(marker, content, infowindow));


            }
          });


}