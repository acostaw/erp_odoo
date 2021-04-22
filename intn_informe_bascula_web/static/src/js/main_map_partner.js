var openInfoWindow;

function initMapHome() {
  const myLatLng = { lat: -25.363, lng: 131.044 };
  const map = new google.maps.Map(document.getElementById("map_div_partner"), {
    zoom: 8,
    center: myLatLng,
  });

  const styles = {
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




  fetch('http://erptest.intn.gov.py/basculas_cliente')
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