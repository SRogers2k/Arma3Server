import os
import re
import subprocess
import urllib.request
import shutil

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501


def download(mods):
    steamcmd = ["/usr/games/steamcmd"]
    steamcmd.extend(["+force_install_dir", "/arma3"])
    steamcmd.extend(["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]])
    for id in mods:
        steamcmd.extend(["+workshop_download_item", "107410", id])
    steamcmd.extend(["+quit"])
    subprocess.call(steamcmd)

    # Finally, prep mod directories and files by making them lowercase
    # Workshop files to lowercase and remove spaces

    tolowercase = "find /arma3/steamapps/workshop/content/107410 -depth -exec rename 'y/A-Z/a-z/' {} +"
    removespaces = "find /arma3/steamapps/workshop/content/107410 -type f -name '* *' -exec rename 's/ /_/g' {} +"
    tolowercaselocal = "find /arma3/mods -depth -exec rename 'y/A-Z/a-z/' {} +"
    removespaceslocal = "find /arma3/mods -type f -name '* *' -exec rename 's/ /_/g' {} +"
    subprocess.run(tolowercase, shell=True, check=True)
    subprocess.run(removespaces, shell=True, check=True)
    subprocess.run(tolowercaselocal, shell=True, check=True)
    subprocess.run(removespaceslocal, shell=True, check=True)

    # ctab is popular but doesn't follow the normal key structure
    source_ctab_dir = '/arma3/steamapps/workshop/content/107410/724582108/@ctab/serverkey'
    destination_ctab_dir = '/arma3/steamapps/workshop/content/107410/724582108/keys'
    # Check if the source directory exists
    if os.path.exists(source_ctab_dir):
        # Ensure the destination directory exists
        if not os.path.exists(destination_ctab_dir):
            os.makedirs(destination_ctab_dir)

        # Copy all files from the source directory to the destination
        for file_name in os.listdir(source_ctab_dir):
            source_file = os.path.join(source_ctab_dir, file_name)
            destination_file = os.path.join(destination_ctab_dir, file_name)

            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_file)

        print(f"Files from '{source_ctab_dir}' have been copied to '{destination_ctab_dir}'.")
    else:
        print(f"Source directory '{source_ctab_dir}' does not exist.")

def preset(mod_file):
    if mod_file.startswith("http"):
        req = urllib.request.Request(
            mod_file,
            headers={"User-Agent": USER_AGENT},
        )
        remote = urllib.request.urlopen(req)
        with open("preset.html", "wb") as f:
            f.write(remote.read())
        mod_file = "preset.html"
    mods = []
    moddirs = []
    with open(mod_file) as f:
        html = f.read()
        regex = r"filedetails\/\?id=(\d+)\""
        matches = re.finditer(regex, html, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            mods.append(match.group(1))
            moddir = WORKSHOP + match.group(1)
            moddirs.append(moddir)
        download(mods)
        for moddir in moddirs:
            keys.copy(moddir)
    return moddirs
