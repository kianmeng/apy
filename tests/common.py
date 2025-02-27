"""Implement som basic test fixtures"""
# pylint: disable=too-few-public-methods
import os
import tempfile
import shutil

from apy.anki import Anki

testDir = os.path.dirname(__file__)


class AnkiTest:
    """Create Anki collection wrapper"""

    def __init__(self, anki):
        self.a = anki

    def __enter__(self):
        return self.a

    def __exit__(self, exception_type, exception_value, traceback):
        self.a.__exit__(exception_type, exception_value, traceback)


class AnkiEmpty(AnkiTest):
    """Create Anki collection wrapper for an empty collection"""

    def __init__(self):
        (self.fd, self.name) = tempfile.mkstemp(suffix=".anki2")
        os.close(self.fd)
        os.unlink(self.name)
        super().__init__(Anki(collection_db_path=self.name))


class AnkiSimple(AnkiTest):
    """Create Anki collection wrapper"""

    def __init__(self):
        self.tmppath = os.path.join(tempfile.gettempdir(), "tempfile.anki2")
        shutil.copy2(testDir + "/data/test_base/Test/collection.anki2", self.tmppath)
        super().__init__(Anki(collection_db_path=self.tmppath))

    def __exit__(self, exception_type, exception_value, traceback):
        super().__exit__(exception_type, exception_value, traceback)
        os.remove(self.tmppath)
