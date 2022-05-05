from functools import cached_property

from SprintLib.utils import get_bytes, write_bytes, delete_file


class FileStorageMixin:

    _bytes = None

    @property
    def bytes(self):
        if self._bytes is not None:
            return self._bytes
        return get_bytes(self.fs_id)

    @bytes.setter
    def bytes(self, value):
        self._bytes = value

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
