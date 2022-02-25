from functools import cached_property

from SprintLib.utils import get_bytes, write_bytes, delete_file


class FileStorageMixin:

    @cached_property
    def bytes(self):
        return get_bytes(self.fs_id)

    @cached_property
    def text(self):
        try:
            return self.bytes.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def write(self, bytes):
        self.fs_id = write_bytes(bytes)
        self.save()

    def remove_from_fs(self):
        delete_file(self.fs_id)
