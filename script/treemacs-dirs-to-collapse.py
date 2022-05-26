#!/usr/bin/env python3

"""Get collapse dirs under given path."""


from os import listdir
from os.path import isdir
from posixpath import join
import sys
import os

ROOT = sys.argv[1]
LIMIT = int(sys.argv[2])
SHOW_ALL = sys.argv[3] == "t"

if LIMIT <= 0:
    exit(0)


def dir_content(path):
    """
    Get content of give path.

    Excluding unreadable files and dotfiles (unless SHOW_ALL is True)
    """
    ret = []

    for item in listdir(path):
        full_path = join(path, item)
        if os.access(full_path, os.R_OK) and (SHOW_ALL or item[0] != "."):
            ret.append(full_path)

    return ret


def main():
    """
    Write collapsed dirs to stdio.

    Fold the folders in reverse order from the normal file location,
    and the maximum depth is LIMIT

    Output format:
    ((suffix, current dir, steps...))
    """
    out = sys.stdout
    # Get subdirs
    dirs = [d for d in dir_content(ROOT) if isdir(d)]

    out.write('(')
    for cur_dir in dirs:
        collapsed = cur_dir
        depth = 0
        steps = []
        content = dir_content(cur_dir)
        while True:
            if depth > LIMIT:
                depth = 0
                steps = []
                collapsed = cur_dir

                break

            if len(content) == 0:
                break

            if len(content) == 1 and isdir(content[0]):
                single_sub_path = content[0]

                depth += 1
                collapsed = join(collapsed, single_sub_path)
                steps.append(single_sub_path)

                content = dir_content(collapsed)

                continue

            break

        if depth > 0 and not ('"' in collapsed or '\\' in collapsed):
            final_dir = steps[-1]
            display_suffix = final_dir[len(cur_dir):]

            steps_str = '" "'.join(steps)
            out.write(f'("{display_suffix}" "{cur_dir}" "{steps_str}")')

    out.write(')')


if __name__ == '__main__':
    main()
