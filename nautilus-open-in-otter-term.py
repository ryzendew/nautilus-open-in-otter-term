#!/usr/bin/python3
import shutil
import subprocess
import urllib.parse

from gi import require_version

try:
    require_version("Nautilus", "4.1")
except ValueError:
    require_version("Nautilus", "4.0")

require_version("Gtk", "4.0")

import logging
import os
from gettext import gettext

from gi.repository import GObject, Nautilus

if os.environ.get("NAUTILUS_OTTER_TERM_DEBUG", "False") == "True":
    logging.basicConfig(level=logging.DEBUG)


class OtterTermNautilus(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self.is_select = False
        pass

    def get_file_items(self, files: list[Nautilus.FileInfo]):
        if not self.only_one_file_info(files):
            return []

        menu = []
        fileInfo = files[0]
        self.is_select = False

        if fileInfo.is_directory():
            self.is_select = True
            dir_path = self.get_abs_path(fileInfo)

            logging.debug("Selecting a directory!!")
            logging.debug(f"Create a menu item for entry {dir_path}")
            menu_item = self._create_nautilus_item(dir_path)
            menu.append(menu_item)

        return menu

    def get_background_items(self, directory):
        if self.is_select:
            self.is_select = False
            return []

        menu = []
        if directory.is_directory():
            dir_path = self.get_abs_path(directory)

            logging.debug("Not thing is selected. Launch from backgrounds!!")
            logging.debug(f"Create a menu item for entry {dir_path}")
            menu_item = self._create_nautilus_item(dir_path)
            menu.append(menu_item)

        return menu

    def _create_nautilus_item(self, dir_path: str) -> Nautilus.MenuItem:
        item = Nautilus.MenuItem(
            name="OtterTermNautilus::open_in_otter_term",
            label=gettext("Open in Otter Term"),
            tip=gettext("Open this folder in Otter Term"),
        )
        logging.debug(f"Created item with path {dir_path}")

        item.connect("activate", self._nautilus_run, dir_path)
        logging.debug("Connect trigger to menu item")

        return item

    def _nautilus_run(self, menu, path):
        which = shutil.which("otter-term")
        if which:
            args = ["otter-term", "--cwd", path]
        else:
            return

        subprocess.Popen(args, cwd=path)

    def get_abs_path(self, fileInfo: Nautilus.FileInfo):
        path = fileInfo.get_location().get_path()
        return path

    def only_one_file_info(self, files: list[Nautilus.FileInfo]):
        return len(files) == 1
