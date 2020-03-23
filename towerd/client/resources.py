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

    def __init__(self, filepath, gather_from_dir=False):
        self.path_dir = os.path.dirname(filepath)
        with open(filepath) as f:
            mapping = "".join([line.strip() for line in f.readlines()])
        self._add_mapping(mapping)

        if gather_from_dir:
            self._gather()

    def _add_mapping(self, mapping):
        try:
            resources = json.loads(mapping)
        except json.JSONDecodeError:
            warnings.warn(
                "No resources found. Try again with Resources._add_mapping(mapping)."
            )
            resources = []

        for resource in resources:
            _, category = resource.keys()
            category_dict = getattr(self, category, None)

            if not category_dict:
                setattr(self, category, ResourceNamespace())
                category_dict = getattr(self, category)

            reference = resource[category]
            category_dict[reference] = os.path.join(self.path_dir, resource["path"])

    def _gather(self):
        contents = {}
        walker = os.walk(self.path_dir)
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
