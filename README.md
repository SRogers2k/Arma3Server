# Arma 3 Dedicated Server in Docker with 2FA accounts

This has been tested with local mods and workshop mods on a Liberation Server. All refereces to "lib" or "lib1" indicate this. Any references to "Lythium" are to the map used.

Forked from https://github.com/BrettMayson/Arma3Server

Uses steamcmd-2fa https://github.com/WoozyMasta/steamcmd-2fa

The directory structure aims to make creating multiple servers as easily and intuitively as possible.

## Usage

### Folder structure
    .
    ├─ <server name>        # Any name you like
    │   ├── configs         # All configs for server (main.cfg, main_basic.cfg (if required))
    │   ├── mods            # All local mods
    

### Creating the image and creating the container
Use the docker-compose.yml file inside a folder.
Copy the `.env.example` file to `.env`, containing at least `STEAM_USER` and `STEAM_PASSWORD` (and `STEAMCMDSECRET` if 2fa is required.).

1. Download and extract zip
2. In the extracted directory, build the image ```docker build -t <image name>```.
3. Create the container ```docker-compose up -d```

Profiles are saved in `/arma3/configs/profiles`

### docker-compose

Use `docker-compose up -d` to start the server.

Use `docker-compose down` to shutdown the server.

Use `docker-compose logs` to see server logs.

See [Docker-compose](https://docs.docker.com/compose/install/#install-compose) for an installation guide.


## Loading mods

### Local

Don't worry about having to edit the names to lowercase, this is done automatically.

1. Place the mods inside `/<servername>/mods`.
2. Be sure that the mod folder is all lowercase and does not show up with quotation marks around it when listing the directory eg `'@ACE(v2)'`
    If this is NOT the case, the mods will prevent the server from booting.
4. Make sure that each mod contains a lowercase `addons` folder. This folder also needs to be lowercase in order for the server to load the required PBO files inside.
5. Start the server.

### Workshop

Set the environment variable `MODS_PRESET` to the HTML preset file exported from the Arma 3 Launcher. The path can be local file or a URL.

`-e MODS_PRESET="my_mods.html"`

`-e MODS_PRESET="http://example.com/my_mods.html"`

### You can have both local and workshop mods for the same server
## Branches
Not yet implemented

## Creator DLC
Not yet implemented

## Troubleshooting

### Steam timeouts when downloading workshop items
Steamcmd has a limitation when downloading large mods. The rule I use: if the mod is >1Gb, install it locally.

## To do
- Check if Steam2fa works when `STEAMCMDSECRET` is empty (if 2fa is not required).
- Move mod preset html file to the server (currently local only) mod directory. Then edit code to point to the specific server mod dir to grab html (don't be lazy and just change the env var).
- Add rename for local mods with spaces.
- Remove Steamcmd2fa and use wget instead.
