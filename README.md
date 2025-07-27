# Blender Batch Texture Exporter (BTX) Addon
![Blender](https://img.shields.io/badge/Blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white)

![BTXlogo](https://qu.ax/EKkBL.png)

## What is this addon for?

**[<ins>Blender</ins>](https://www.blender.org/) Batch Texture Exporter** addon allows you to export textures from selected objects in a scene, copying or creating symlinks to the textures in a specified directory. Perfect for asset management and sharing projects with clean texture organization!

- **Texture Tracking**  
  Creates symlinks that point to original texture locations, helping you:
  - Find scattered textures across different folders
  - Preserve original file paths

- **Non-destructive Workflow**  
  Exported textures **don't replace originals** in your material nodes - they're copied to your specified location while keeping original node paths intact.

---

>![Q1](https://qu.ax/jjpyn.jpg)

>![BTX_ui](https://qu.ax/NKapF.png)

## Features

- **Octane Render Support**  
  Works with both standard [<ins>Blender</ins>](https://www.blender.org/) and [<ins>Octane Blender Edition</ins>](https://home.otoy.com/render/octane-render/) `IMAGE` nodes.

- **Select multiple objects**  
  Export textures for one or multiple selected objects in the scene.

- **Multi-Material Handling**  
  Processes **all materials** assigned to selected objects, even if:
  - Object uses multiple materials
  - Materials are shared between objects
  - Materials contain multiple texture nodes

- **Format support**  
  Handles `PNG`, `JPG`, `TGA`, `EXR`, `DDS` and other common formats.

- **Custom output directory**  
  Choose the destination directory for the exported textures.

- **Create subfolders**  
  Optionally, create a subfolder for each object in the output directory.

- **Overwrite existing files**  
  Optionally overwrite existing texture files in the destination folder.

- **Create symlinks**  
  Instead of copying textures, create symbolic links to the original textures.

- **Support for node-based materials**  
  Processes textures from node-based materials in `MESH` and `FONT` objects.


## Installation

1. Download the latest `BTX_BatchTextureExporter.zip` from [<ins>Releases</ins>](https://github.com/LocalDataBase/BTX/releases)
2. In Blender:
   - `Edit` → `Preferences` → `Add-ons`
   - Click `Install...` and select the downloaded file
   - Enable the addon by checking its box

> **Supported Blender Versions:** 2.80, 2.90, 3.0+, 4.0+  
> *(Tested on 3.6 LTS/4.3.2)*

## Usage

> [!NOTE]
>Addon **only works with unpacked .blend files**:
>   - Use `File > External Data > Unpack Resources` first.

1. **Select the objects** you want to export textures from (they should be of type `MESH` or `FONT`).
2. Go to the **3D Viewport**.
3. Open the **Tool Shelf** (`N` key) and locate the **Tool > Batch Texture Exporter** tab.
4. Click on the **Export Textures** button.

> [!WARNING]
> If you export many large textures, blender may freeze for a while, don't worry, this is how the export process works. You can open the output directory folder and watch the export process in real time.

### Options

| Option                | Description |
|-----------------------|-------------|
| **`Output Directory`**  | Select the folder where the textures will be copied. |
| **`Create Subfolder`**  | If enabled, each object's textures will be placed in a separate folder named after the object. |
| **`Overwrite Files`**   | If enabled, existing textures in the output directory will be overwritten. |
| **`Create Symlinks`**   | If enabled, symbolic links to the textures will be created instead of copying the files. |


## 📂 Example Output

If **`Create Subfolder`** is enabled, the exported textures will be structured as follows:

```
Textures/
│── Object1/
│   ├── texture1.png
│   └── texture2.jpg
│── Object2/
│   └── texture1.png
```

If **`Create Symlinks`** is enabled, the addon will create symbolic links instead of copying the files:

```
Textures/
│── Object1/
│   └── texture1.png -> /original/path/to/texture1.png
```


## Troubleshooting

### No textures exported?
Make sure the selected objects have materials with **image textures**. The addon works only with **node-based materials** that use `IMAGE` nodes.

### Error during copy?
Ensure that:
- The file paths are correct
- You have permission to write to the output directory
- The original textures exist and are accessible

### Permission errors?
- Try different output directory
- On Windows, run Blender as Admin
