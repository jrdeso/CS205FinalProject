import json
import os
import warnings


class Resources:
    """
    Resources are obtained from a json file of an array of objects with two
    key-value pairs: the key 'path' mapping to a filepath and a string
    key that categorizes the path mapping to a unique identifier.

    {
      "path": "assets/test/test.txt"
      "text": "test1"
    }

    The path in the JSON object above can be accessed by

    print(resources.text.test1)     # outputs 'assets/test/test.txt'
    OR
    print(resources.text['test1'])  # in case an identifier contains a space
    """

    def __init__(self, resourcePath, mapFromFile=False, mapFromDir=False, nameMap=False):
        self.pathDir = os.path.dirname(resourcePath)
        with open(resourcePath) as f:
            self.mapping = "".join([line.strip() for line in f.readlines()])

        if mapFromFile:
            self.mapFromFile(self.mapping)

        if mapFromDir:
            self.mapFromDir()

        if nameMap:
            self._nameMap()

    def mapFromFile(self, mapping):
        try:
            resources = json.loads(mapping)
        except json.JSONDecodeError:
            warnings.warn(
                "No resources found. Try again with Resources._mapFromFile(mapping)."
            )
            resources = []

        for resource in resources:
            _, category = resource.keys()
            self._setInternal(resource['path'], resource[category], category)

    def mapFromDir(self):
        walker = os.walk(self.pathDir)
        for (dirpath, dirnames, filenames) in walker:
            for filename in filenames:
                reference, _ = os.path.splitext(filename)
                category = os.path.basename(dirpath)
                self._setInternal(os.path.join(category, filename), reference, category)

    def _setInternal(self, path, reference, category):
        categoryDict = getattr(self, category, None)

        if not categoryDict:
            setattr(self, category, ResourceNamespace())
            categoryDict = getattr(self, category)

        reference = reference
        categoryDict[reference] = os.path.join(self.pathDir, path)

    def _nameMap(self):
        contents = {}
        walker = os.walk(self.pathDir)
        for (dirpath, dirnames, filenames) in walker:
            for filename in filenames:
                if contents.get(filename, None) is None:
                    contents[filename] = []
                contents[filename].append(os.path.join(dirpath, filename))
        self.contents = contents


class ResourceNamespace(dict):
    """
    Simple namespace object. Allows dot notation for accessing a dictionary.
    For example, dict.attribute.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
