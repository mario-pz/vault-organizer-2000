"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
"""

import os
import shutil
import mimetypes
from pathlib import Path
from typing import List

import imghdr


def move_files(source_dir: str, target_dirs: dict) -> None:
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                for target_dir, mime_prefix in target_dirs.items():
                    if mime_type.startswith(mime_prefix):
                        target_path = os.path.join(target_dir, file)
                        print(f"Moving {file_path} to {target_path}")
                        shutil.move(file_path, target_path)
                        break
            else:
                image_type = imghdr.what(file_path)
                if image_type == "webp":
                    target_path = os.path.join(target_dirs["image"], file)
                else:
                    target_path = os.path.join(target_dirs["video"], file)

                shutil.move(file_path, target_path)


def organize_files(source_dir: str, file_types: List[str]) -> None:
    target_dirs = {
        "image": os.path.join(source_dir, "image"),
        "video": os.path.join(source_dir, "video"),
        "application": os.path.join(source_dir, "documents"),
        "image/webp": os.path.join(source_dir, "video"),
    }

    for file_type in file_types:
        target_dir = target_dirs.get(file_type)
        if target_dir is None:
            target_dir = os.path.join(source_dir, file_type)
            Path(target_dir).mkdir(exist_ok=True)
            target_dirs[file_type] = target_dir

    move_files(source_dir, target_dirs)


if __name__ == "__main__":
    source_directory = "."

    file_types_to_organize = [
        # Look up to mimetypes documentation to add more
        # If you don't specify something not on this list
        # It will move to an "unrecognized" directory
        "image",
        "video",
        "application",
        "image/webp",
    ]

    organize_files(source_directory, file_types_to_organize)
