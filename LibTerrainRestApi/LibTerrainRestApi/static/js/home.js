// mappa Lefalet: https://leafletjs.com/examples/quick-start
/**
 * Inizializza una mappa Leaflet aggiungendo un layer ed una posizione di partenza
 */
function mapInitialize() {
    doMapInitialize();
}

function doMapInitialize() {
    myMap = L.map('mapid').on('locationerror ', setDefaultMapView)
        .on('click', onMapClick).locate({ setView: true });
    setMapTileLayer(myMap);
    markersLayer = L.featureGroup().on('click', removeMarkerOnClick).addTo(myMap);
    //myMap.addLayer(markersLayer);
}

function setDefaultMapView(e) {
    myMap.setView([51.505, -0.09], 11);
}

/**
 * Aggiunge un layer ad una mappa Leaflet
 * @param {any} map mappa cui aggiungere il layer
 */
function setMapTileLayer(map) {
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(map);
}

function onMapClick(e) {
    if (markersLayer.getLayers().length < 2) {
        var marker = L.marker(e.latlng);
        marker.on('click', removeMarkerOnClick);
        marker.bindPopup(e.latlng).openPopup();
        markersLayer.addLayer(marker);
    } else {
        window.alert("Click a marker to delete and retry");
    }
}

function removeMarkerOnClick(e) {
    var clickedMarker = this;
    markersLayer.removeLayer(clickedMarker);
}

//function positionSuccess(position) {
//    doMapInitialize(position.coords.latitude, position.coords.longitude);
//}
//function positionError(errorMessage) {
//    window.alert(errorMessage);
//    doMapInitialize(51.505, -0.09);
//}