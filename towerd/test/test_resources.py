import os
import tempfile
import unittest

from ..Resources import Resources


class TestResources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.TemporaryDirectory()
        cls.tmp_subdir1 = tempfile.TemporaryDirectory(dir=cls.tmp_dir.name)
        cls.tmp_subdir2 = tempfile.TemporaryDirectory(dir=cls.tmp_dir.name)
        cls.tmp_subdir3 = tempfile.TemporaryDirectory(dir=cls.tmp_subdir2.name)

        tmp_resource_fd, cls.tmp_resource = tempfile.mkstemp(dir=cls.tmp_dir.name)
        with os.fdopen(tmp_resource_fd, mode="w") as resource_file:
            resource_file.write(
                '[{"path":"assets/sound/arrow1.mp4","sound":"arrow1"},{"path":"assets/image/tower1.png","image":"archer_tower"}]'
            )

        _, cls.tmp_tmp1 = tempfile.mkstemp(suffix="_file", dir=cls.tmp_subdir1.name)
        _, cls.tmp_tmp2 = tempfile.mkstemp(suffix="_file", dir=cls.tmp_subdir2.name)
        _, cls.tmp_tmp3 = tempfile.mkstemp(suffix="_file", dir=cls.tmp_subdir3.name)

    def test_resources(self):
        resources = Resources(TestResources.tmp_resource)

        self.assertEqual(
            resources.sound.arrow1,
            os.path.join(resources.pathDir, "assets/sound/arrow1.mp4"),
        )
        self.assertEqual(
            resources.image.archer_tower,
            os.path.join(resources.pathDir, "assets/image/tower1.png"),
        )

    def test_gather(self):
        resources = Resources(TestResources.tmp_resource, gatherFromDir=True)

        tmp_files = [
            TestResources.tmp_tmp1,
            TestResources.tmp_tmp2,
            TestResources.tmp_tmp3,
        ]

        for tmp_file in tmp_files:
            tmp_results = resources.contents[os.path.basename(tmp_file)]
            self.assertEqual(tmp_results[0], tmp_file)
