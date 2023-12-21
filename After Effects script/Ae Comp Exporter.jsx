#target aftereffects

// Function to export camera keyframes
function exportCameraKeyframes(cameraLayer) {
    var keyframeData = [];
    for (var i = 1; i <= cameraLayer.property("Position").numKeys; i++) {
        keyframeData.push({
            time: cameraLayer.property("Position").keyTime(i),
            value: cameraLayer.property("Position").keyValue(i)
        });
    }
    return keyframeData;
}

// Function to export solids and nulls with just their current positions
function exportSolidsAndNulls(comp) {
    var objectsData = [];
    for (var i = 1; i <= comp.numLayers; i++) {
        var layer = comp.layer(i);
        if (layer instanceof AVLayer && (layer.nullLayer || layer.source instanceof SolidSource)) {
            var objData = {
                name: layer.name,
                type: layer.nullLayer ? "null" : "solid",
                position: layer.transform.position.value // Just get current position
                // No keyframe extraction
            };
            objectsData.push(objData);
        }
    }
    return objectsData;
}

// Function to export keyframes of a property
function exportKeyframes(property) {
    var keyframes = [];
    for (var i = 1; i <= property.numKeys; i++) {
        keyframes.push({
            time: property.keyTime(i),
            value: property.keyValue(i)
        });
    }
    return keyframes;
}

// Function to export camera data including calculated focal length
function exportCameraData(cameraLayer, comp) {
    var sensorWidth = 36; // Default sensor width in mm

    if (!cameraLayer || !cameraLayer.cameraOption) {
        alert("Error: No valid camera layer found.");
        return null;
    }

    // Correctly accessing the zoom value
    var zoom = cameraLayer.cameraOption.zoom.value;
    var compWidth = comp.width;

    if (zoom === undefined || zoom === 0) {
        alert("Error: Zoom value is invalid or zero.");
        return null;
    }

    if (compWidth === undefined || compWidth === 0) {
        alert("Error: Composition width is invalid or zero.");
        return null;
    }

    // Calculate focal length using the formula
    var focalLength = (zoom * sensorWidth) / compWidth;

    var cameraData = {
        positionKeyframes: exportKeyframes(cameraLayer.property("Position")),
        rotationKeyframes: exportKeyframes(cameraLayer.property("Orientation")),
        sensorWidth: sensorWidth,
        focalLength: focalLength
    };
    return cameraData;
}

// UI Function
function showUI() {
    var win = new Window("dialog", "Export Settings");
    win.orientation = "column";
    win.alignChildren = "fill";

    var fileGroup = win.add("group");
    fileGroup.add("statictext", undefined, "File path:");
    var filePath = fileGroup.add("edittext", undefined, "");
    filePath.size = [200, 20];
    var browseBtn = fileGroup.add("button", undefined, "Browse");
    browseBtn.onClick = function() {
        var selectedFile = File.saveDialog("Save your file");
        if (selectedFile) filePath.text = selectedFile.fsName;
    }

    var sensorSizeGroup = win.add("group");
    sensorSizeGroup.add("statictext", undefined, "Sensor size (mm):");
    var sensorSizeInput = sensorSizeGroup.add("edittext", undefined, "36");
    sensorSizeInput.size = [50, 20];

    var exportOptions = win.add("panel", undefined, "Export Options");
    var exportCameraCheckbox = exportOptions.add("checkbox", undefined, "Export Camera");
    exportCameraCheckbox.value = true;
    var exportNullsCheckbox = exportOptions.add("checkbox", undefined, "Export Nulls");
    exportNullsCheckbox.value = true;

    var buttons = win.add("group");
    buttons.alignment = "center";
    var okButton = buttons.add("button", undefined, "OK");
    var cancelButton = buttons.add("button", undefined, "Cancel");

    okButton.onClick = function() {
        if (!filePath.text) {
            alert("Please specify a file path.");
            return;
        }
        win.close();
        main(filePath.text, parseFloat(sensorSizeInput.text), exportCameraCheckbox.value, exportNullsCheckbox.value);
    };

    cancelButton.onClick = function() {
        win.close();
    };

    win.center();
    win.show();
}

// Updated Main Function with Parameters
function main(filePath, sensorSize, exportCamera, exportNulls) {
    var comp = app.project.activeItem;
    if (!(comp && comp instanceof CompItem)) {
        alert("No active composition.");
        return;
    }

    var data = {
        fps: comp.frameRate,
        options: {
            exportCamera: exportCamera,
            exportNulls: exportNulls,
        }
    };

    if (exportCamera) {
        var cameraLayer = comp.activeCamera;
        if (!cameraLayer) {
            alert("No active camera.");
            return;
        }
        var cameraData = exportCameraData(cameraLayer, comp, sensorSize);
        if (cameraData === null) {
            return;
        }
        data.camera = cameraData;
    }

    if (exportNulls) {
        data.objects = exportSolidsAndNulls(comp);
    }

    var file = new File(filePath);
    if (!/\.json$/i.test(filePath)) {
        file = new File(filePath + ".json");
    }
    file.open("w");
    file.write(JSON.stringify(data, null, 4));
    file.close();

    alert("Export completed to: " + file.fsName);
}

// Call UI
showUI();
