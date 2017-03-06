import os

from polymorph.tools import YamlToCsv, RowTools


TEST_DATA_DIR = './polymorph/tests/test_data/'

def get_test_file_path(filename):
    return '{}{}'.format(TEST_DATA_DIR, filename)


def test_load_from_file():
    yaml_to_csv = YamlToCsv()
    path = get_test_file_path('simple_example.yaml')
    assert yaml_to_csv.load_from_file(path) == {'foo': 'bar'}


def test_write_to_file():
    yaml_to_csv = YamlToCsv()
    path = get_test_file_path('output.yaml')
    yaml_to_csv.write_to_file(path, {'foo': 'bar'})

    with open(path) as f:
        assert f.read() == '{foo: bar}\n'

    # should probably mock open instead of actually creating a file
    os.remove(path)


DATA = {
    'foo': 'bar',
    'cars': ['one', 'two'],
    'fruit': [
        {'apple': 'green'},
        {'banana': 'yellow'},
    ]
}

ROWS = [
    ('foo', 'bar'),
    ('cars.0', 'one'),
    ('cars.1', 'two'),
    ('fruit.0.apple', 'green'),
    ('fruit.1.banana', 'yellow'),
]

def test_to_rows():
    row_tools = RowTools()
    assert sorted(row_tools.to_rows(DATA)) == sorted(ROWS)


def test_rows_to_data():
    row_tools = RowTools()
    assert sorted(row_tools.rows_to_data(ROWS)) == sorted(DATA)
