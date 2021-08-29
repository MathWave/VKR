from os import listdir
from os.path import isfile, join
from shutil import copyfile, copytree


def copy_content(from_dir, to_dir, exc=()):
    for file in listdir(from_dir):
        if file in exc:
            continue
        full_path = join(from_dir, file)
        if isfile(full_path):
            func = copyfile
        else:
            func = copytree
        func(full_path, join(to_dir, file))
