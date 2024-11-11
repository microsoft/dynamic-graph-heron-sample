import shutil
import tempfile

from pathlib import Path

def copy_files(src_folder, dest_folder, glob_pattern="**/*", preserve_structure=False):
    """Copy files from src_folder to dest_folder based on a glob pattern.

    If preserve_structure is True, the directory structure of src_folder is preserved in dest_folder.
    If False, all files are copied directly into dest_folder without keeping the folder structure.

    i.e. copy_files("data", "output", "*.tsv") will copy all files with .tsv extension
         from source folder to destination folder.

    Args:
        src_folder (str): The source directory from which to copy files.
        dest_folder (str): The destination directory where files should be copied.
        glob_pattern (str): The glob pattern to match files. Defaults to '**/*' to match all files recursively.
        preserve_structure (bool): Whether to preserve the source folder's directory structure in the destination.
    """
    for f in Path(src_folder).glob(glob_pattern):
        if f.is_file():
            dest_file = (Path(dest_folder) / f.relative_to(src_folder)) if preserve_structure else (Path(dest_folder) / f.name)
            copy_file(f, dest_file)
        else:
            print(f"Encountered directory {f} - Proceeding to copy files in directory.")


def copy_file(src_file, dest_file):
    """Copy src_file to dest_file.

    Note that the dest_file is the target file name, not the target folder name.
    """
    if src_file == dest_file:
        return
    Path(dest_file).parent.mkdir(parents=True, exist_ok=True)
    print(f"Copying file: {src_file} -> {dest_file}")
    shutil.copy2(src_file, dest_file)