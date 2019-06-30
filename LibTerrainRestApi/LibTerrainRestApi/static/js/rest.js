
// CODICE REST

var devices;
function requestLinkData() {
  if (markersLayer.getLayers().length != 2) {
    alert("Select two points");
    return;
  }
  var xhttp = new XMLHttpRequest();
  var dataToSend = createRequestData();
  xhttp.open("POST", "/api/v1/link", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(JSON.stringify(dataToSend));
  xhttp.onreadystatechange = function () {
    if (this.readyState == XMLHttpRequest.DONE) {
      switch (this.status) {
        case 400:
          document.getElementById("info").innerText = 'Error 400';
          break;
        case 500:
          document.getElementById("info").innerText = 'Error 500';
          break;
        case 200:
          var profile = JSON.parse(this.responseText);
          // link non possibile
          if (!profile.link_is_possible) {
            alert("Connection is not possible");
            resetAllData();
            return false;
          }
          resetElevationData(false);
          // aggiunge offset altezza primo e ultimo punto
          var coordinates = profile.profile.features[0].geometry.coordinates;
          coordinates[0][2] += profile.offsets.source;
          coordinates[coordinates.length - 1][2] += profile.offsets.destination;
          //{ TEST: per verificare il corretto ridisegno dell'elevazione ed ellisse
          //var coordinates = profile.profile.features[0].geometry.coordinates;
          //var randHeight = Math.floor((Math.random() * 20) + 1);
          //var randmid = Math.floor((Math.random() * coordinates.length));
          //coordinates[randmid][2] += randHeight;
          //document.getElementById("info").innerText = profile.link_is_possible.toString().toUpperCase();
          //}
          elevation.loadData(JSON.stringify(profile.profile));
          drawEllipse();
          displayOffsetResult(profile.offsets.source, profile.offsets.destination, profile.loss, profile.maximum_bitrate);
          showElevationView();
          break;
      }
    }
  };
}

/**
 * Get device names via rest api
 */
function requestDeviceData() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/api/v1/devices");
  xhttp.send();
  xhttp.onreadystatechange = function () {
    if (this.readyState == XMLHttpRequest.DONE) {
      switch (this.status) {
        case 400:
          document.getElementById("info").innerText = 'Error 400';
          break;
        case 500:
          document.getElementById("info").innerText = 'Error 500';
          break;
        case 200:
          devices = JSON.parse(this.responseText);
          fillDeviceSelectionOptions(devices);
          break;
      }
    }
  };
}

/**
 * Get user inserted data to compute profile elevation, link speed, etc
 */
function createRequestData() {
  var points = markersLayer.getLayers();
  var first = points[0].getLatLng();
  var second = points[1].getLatLng();
  var data = {
    // points
    source: {
      type: 'Point',
      coordinates: [first.lng, first.lat] //[11.129426, 43.951486]
    },
    destination: {
      type: 'Point',
      coordinates: [second.lng, second.lat]//[11.129399, 43.952413]
    }
  };
  // offsets
  switch (document.getElementById("offset_mode").value) {
    case 'auto':
      data['offsets'] = {
        auto: parseInt(document.getElementById('auto_offset').value)
      };
      break;
    case 'manual':
      data['offsets'] = {
        source: parseInt(document.getElementById('manual_src_offset').value),
        destination: parseInt(document.getElementById('manual_dst_offset').value)
      };
      break;
  }
  // devices
  data['source_device'] = document.getElementById('src_device').value;
  data['destination_device'] = document.getElementById('dst_device').value;
  return data;
}