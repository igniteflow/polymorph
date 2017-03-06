import yaml


class RowTools(object):
    """
    transform a Python object to csv friendly rows

    Example:

        {
            'foo': 'bar',
            'cars': ['one', 'two'],
            'fruit': [
                {'apple': 'green'},
                {'banana': 'yellow'},
            ]
        }

    Becomes rows:

    [
        ('foo', 'bar'),
        ('cars.0', 'one'),
        ('cars.1', 'two'),
        ('fruit.0.apple', 'green'),
        ('fruit.1.banana', 'yellow'),
    ]
    """
    rows = None
    keys = None

    def _str(self, data):
        if self.rows is None:
            self.rows = []

        identifier = '.'.join([str(i) for i in self.keys])
        self.rows.append((identifier, data))
        self.keys.pop()

    def _list(self, data):
        items = []
        for i, item in enumerate(data):
            if i > 0 and self.keys[-1] == (i - 1):
                # remove the index from the previous iteration
                self.keys.pop()
            items.append(self.recurse(item, key=i))
        return items

    def _dict(self, data):
        # assumes keys can only be strings
        for k, v in data.items():
            self.recurse(v, key=k)

    def recurse(self, data, key=None):
        if self.keys is None:
            self.keys = []

        if key is not None:
            self.keys.append(key)

        if isinstance(data, list):
            _data = self._list(data)
            self.keys.pop()
            return _data
        elif isinstance(data, dict):
            return self._dict(data)
        elif isinstance(data, (str, unicode)):
            self._str(data)

    def to_rows(self, data):
        self.recurse(data)
        return self.rows

    def rows_to_data(self, rows):
        # TODO
        pass


class YamlToCsv(object):
    def load_from_file(self, path):
        with open(path) as f:
            return yaml.load(f)

    def write_to_file(self, path, data):
        with open(path, 'w+') as f:
            f.write(yaml.dump(data))

    def to_rows(self, data):
        """
        csv will have two columns:
        (1) identifier
        (2) value
        """
        pass
