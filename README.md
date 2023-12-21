## Instructions for Using the AE Script and Blender Add-on

### Adobe After Effects Script

This script exports camera and null object data from After Effects to a JSON file.

#### How to Use:

1. **Open Your AE Project:**
   - Open the After Effects project containing the composition you want to export.

2. **Run the Script:**
   - Go to `File > Scripts > Run Script File...` in After Effects.
   - Navigate to and select the AE script file `Ae Comp Exporter.jsx`.
   - The script will prompt you for a location to save the JSON file and export the data.
     <p align="left">
     <img width="420" src="https://github.com/xudxud/Common/blob/28c8eb7a9b39a39f26dc50ceb2c708c742357348/b/images/img_AeTrackingData2Blender/03_OpenJsxFile.png">
     </p>
   <br />**Note:** *It's recommanded to enable all the exporting options.*
   <br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*You can decide what you want when importing JSON file to Blender.*

### Blender Add-on

This Blender add-on imports the JSON file created by the AE script and organizes the imported objects into specific collections.

#### Installation:

1. **Install the Add-on in Blender:**
   - Open Blender and go to `Edit > Preferences > Add-ons`.
     <p align="left">
     <img width="420" src="https://github.com/xudxud/Common/blob/8185539f449cb88a68ac4828194746c2270dc9e3/b/images/img_AeTrackingData2Blender/11_InstallAddon_1.png">
     </p>
   - Click `Install` and navigate to the `Ae Comp Importer.py` file.
     <br />Select the file and click `Install Add-on`.
     <p align="left">
     <img width="420" src="https://github.com/xudxud/Common/blob/8185539f449cb88a68ac4828194746c2270dc9e3/b/images/img_AeTrackingData2Blender/11_InstallAddon_2.png">
     </p>
   - In the Add-ons list, find and enable the add-on by checking the box next to its name.
     <p align="left">
     <img width="420" src="https://github.com/xudxud/Common/blob/8185539f449cb88a68ac4828194746c2270dc9e3/b/images/img_AeTrackingData2Blender/12_EnableAddon.png">
     </p>

#### How to Use:

1. **Import AE JSON Data:**
   - In Blender, go to `File > Import > AE JSON Import (.json)`.
   - Select the JSON file exported from After Effects.
   - Optionally, set the `Start Frame` and the other options in the file dialog.
     <br />The third option will generate points in a mesh using track points.
     <p align="left">
     <img width="420" src="https://github.com/xudxud/Common/blob/8185539f449cb88a68ac4828194746c2270dc9e3/b/images/img_AeTrackingData2Blender/14_ImportSettings.png">
     </p>
   - Click `Import AE JSON` to import the data into Blender.

2. **Check the Collections:**
   - In the Blender scene, you will find a new collection named "Comp from AE" containing the imported camera and its hierarchy.
   - If track points were imported, they will be in a nested collection named "Track Points".

---

### Notes:

- Ensure that your After Effects composition contains the data you want to export (camera and null objects).
- The AE script may require modification if your AE project has different requirements or data structures.
- The Blender add-on assumes a specific JSON structure. If your JSON file differs, you may need to adjust the add-on script.
- Test both the AE script and Blender add-on with your specific project data to ensure compatibility.
