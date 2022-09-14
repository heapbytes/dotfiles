# vim: set fileencoding=utf-8

import fnmatch
import os
import stat

from ranger.api import register_linemode
from ranger.core.linemode import LinemodeBase

from .icons import file_node_extensions, file_node_exact_matches, file_node_pattern_matches


def get_icon(file):
    basename = os.path.basename(file.relative_path)

    em_icon = file_node_exact_matches.get(basename.lower())
    if em_icon is not None:
        return em_icon

    for pattern, pm_icon in file_node_pattern_matches.items():
        if fnmatch.filter([basename], pattern):
            return pm_icon

    default = '' if file.is_directory else ''
    return file_node_extensions.get(file.extension, default)


def get_symbol(file):
    if file.is_link:
        if not file.exists:
            return '!'
        if file.stat and stat.S_ISDIR(file.stat.st_mode):
            return '~'
        return '@'

    if file.is_socket:
        return '='

    if file.is_fifo:
        return '|'

    if not file.is_directory and file.stat:
        mode = file.stat.st_mode
        if mode & stat.S_IXUSR:
            return '*'
        if stat.S_ISCHR(mode):
            return '-'
        if stat.S_ISBLK(mode):
            return '+'

    # if file.is_directory:
    #     return '/'

    return ''


@register_linemode
class DevIcons2Linemode(LinemodeBase):
    name = 'devicons2'
    uses_metadata = False

    def filetitle(self, file, metadata):
        return '{0} {1}{2}'.format(
            get_icon(file),
            file.relative_path,
            get_symbol(file),
        )
