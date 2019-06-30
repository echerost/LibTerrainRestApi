var map;
var markersLayer;
var elevation;
var controlLayer;
var canSelectPoints = false;

var opts = {
  map: {
    zoomControl: false
  },
  elevationControl: {
    options: {
      theme: "lime-theme",
      useHeightIndicator: true,
      elevationDiv: "#elevation-div",
      detachedView: true
    },
  },
  layersControl: { options: { collapsed: false } },
};

function initMapTerrainProfile() {
  map = L.map('map').on('locationerror ', setDefaultMapView)
    .on('click', addMarker).on('eledata_loaded', eledata_loaded).locate({ setView: true });//.on('eledata_reloaded', drawEllipse)
  setMapTileLayer(map);
  markersLayer = L.featureGroup().on('click', removeMarker).addTo(map);

  elevation = L.control.elevation(opts.elevationControl.options);
  elevation.addTo(map);
  controlLayer = L.control.layers(null, null, opts.layersControl.options);
  //controlLayer.addTo(map); //per selezionare i layer manualmente(checkbox)
}

/**
 * Aggiunge un layer ad una mappa Leaflet
 * @param {any} map mappa cui aggiungere il layer
 */
function setMapTileLayer(map) {
  var tileLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 24,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
      '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
  }).addTo(map);
  return tileLayer;
}

/**
 * Set map view to a default location
 */
function setDefaultMapView() {
  map.setView([43.968526774903815, 11.125824451446533], 15);
}

function addMarker(e) {
  // can select points only if user clicked button in navbar
  if (!canSelectPoints) {
    alert("See navbar on the left");
    return;
  }
  if (markersLayer.getLayers().length > 2) {
    window.alert("Click a marker to delete and retry");
    return;
  }
  var marker = L.marker(e.latlng);
  marker.on('click', removeMarker);
  marker.bindPopup(e.latlng).openPopup();
  markersLayer.addLayer(marker);

  // after two selected points shows offsets and devices form
  if (markersLayer.getLayers().length >= 2) {
    showOffsetView();
  }
}

function removeMarker(e) {
  var clickedMarker = this;
  markersLayer.removeLayer(clickedMarker);
}

function eledata_loaded(e) {
  var q = document.querySelector.bind(document);
  var track = e.track_info;
  controlLayer.addOverlay(e.layer, e.name);
  q('.totlen .summaryvalue').innerHTML = track.distance.toFixed(2) + " km";
  q('.maxele .summaryvalue').innerHTML = track.elevation_max.toFixed(2) + " m";
  q('.minele .summaryvalue').innerHTML = track.elevation_min.toFixed(2) + " m";
}

/**
 * Draw an ellipse over terrain elevation profile
 * Call this function only after elevation profile
 */
function drawEllipse() {
  var coordinates = elevation._data;
  var firstH = coordinates[0].z;
  var lastH = coordinates[coordinates.length - 1].z;

  // punti partenza
  var startX = 0;
  var startY = elevation._y(firstH);//altezza primo elemento
  var endX = elevation._width();
  var endY = elevation._y(lastH);//altezza ultimo elemento

  // centro
  var mX = (startX + endX) / 2;
  var mY = (startY + endY) / 2;

  var length = Math.sqrt(Math.pow((mX - startX), 2) + Math.pow((mY - startY), 2));
  var h = mY - startY;
  var angle = h / length * 180 / Math.PI;

  // draw ellipse
  var base = d3.selectAll("svg").filter(".background").select("rect");
  var parent = base.select(function () { return this.parentNode; });
  parent.append("ellipse")
    .attr("cx", mX)
    .attr("cy", mY)
    .attr("rx", length)
    .attr("ry", 3)
    .attr("transform", "rotate(" + angle + "," + mX + "," + mY + ")")
    .attr("fill-opacity", 0.3);
}

function resetAllData(resetMarkers = true) {
  resetElevationData(resetMarkers);
  resetOffsetView();
  document.getElementById('modal_div').style.display = 'none';
  activateMap();
}

function resetElevationData(resetMarkers = true) {
  //document.getElementById('elevation-div').innerHTML = '';
  elevation.clear();
  if (resetMarkers) { markersLayer.clearLayers(); }
  //elevation = L.control.elevation(opts.elevationControl.options);
  //elevation.addTo(map);
  //controlLayer = L.control.layers(null, null, opts.layersControl.options);
  showElevationView(false);
}

function activateMap() {
  canSelectPoints = true;
}