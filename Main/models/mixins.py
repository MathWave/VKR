from SprintLib.utils import get_bytes, write_bytes, delete_file


class FileStorageMixin:
    @property
    def text(self):
        return get_bytes(self.fs_id).decode("utf-8")

    def write(self, bytes):
        self.fs_id = write_bytes(bytes)
        self.save()

    def remove_from_fs(self):
        delete_file(self.fs_id)
