
// CODICE GESTIONE INTERNA PAGINA

/**
 * Display computed data (speed and offsets)
 * @param {any} src_offset source computed offset
 * @param {any} dst_offset destination computed offset
 */
function displayOffsetResult(src_offset, dst_offset, loss, bitrate) {
  document.getElementById("offset_mode_lb").style.display = 'none';
  document.getElementById("auto_offset_div").style.display = 'none';
  document.getElementById("manual_offset_div").style.display = 'none';
  document.getElementById("result_src_offset").innerText = src_offset;
  document.getElementById("result_dst_offset").innerText = dst_offset;
  document.getElementById("result_bitrate_dwn").innerText = bitrate[0];
  document.getElementById("result_bitrate_up").innerText = bitrate[1];
  document.getElementById("result_loss").innerText = loss;
  document.getElementById('result_offset_div').style.display = 'block';
}

function resetOffsetView() {
  offsetModeChanged('auto');
  document.getElementById('offset_mode').value = 'auto';
  document.getElementById('offset_mode_lb').style.display = 'block';
  document.getElementById("result_src_offset").innerText = '';
  document.getElementById("result_dst_offset").innerText = '';
  document.getElementById('result_offset_div').style.display = 'none';
}

/**
 * Add devices to passed select HTML element
 * @param {any} selectElement HTML select target element
 * @param {any} device_list devices to add
 */
function addDevicesOptions(selectElement, device_list) {
  for (var device of device_list) {
    var opt = document.createElement('option');
    opt.value = opt.innerText = device;
    selectElement.appendChild(opt);
  }
}

/**
 * Fill user device drop down menu with a list of device
 * @param {any} device_list devices between which the user must choose
 */
function fillDeviceSelectionOptions(device_list) {
  var select = document.getElementById('src_device');
  addDevicesOptions(select, device_list);
  select = document.getElementById('dst_device');
  addDevicesOptions(select, device_list);
}

/**
 * Update HTML when user changes offset mode(manual or auto)
 * @param {any} mode offset mode chosen by user
 */
function offsetModeChanged(mode) {
  switch (mode) {
    case 'auto':
      document.getElementById("manual_offset_div").style.display = 'none';
      document.getElementById("auto_offset_div").style.display = 'block';
      break;
    case 'manual':
      document.getElementById("auto_offset_div").style.display = 'none';
      document.getElementById("manual_offset_div").style.display = 'block';
      break;
  }
}

/**
 * Show or hide terrain profile data
 * @param {any} flag true: show, false: hide
 */
function showElevationView(flag = true) {
  var elevdata = document.getElementById('elevdata');
  if (flag) { elevdata.style.display = 'block'; }
  else { elevdata.style.display = 'none'; }
}

function showOffsetView() {
  document.getElementById('modal_div').style.display = 'block';;
}

function hideElementById(elementID) {
  document.getElementById(elementID).style.display = 'none';
}