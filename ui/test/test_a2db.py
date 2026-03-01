import os
import logging
import uuid

import a2db


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

temp_db_path = os.path.join(os.environ.get('TEMP', ''), str(uuid.uuid4()))
log.debug('temp_db: %s' % temp_db_path)
db = a2db.A2db(temp_db_path)


def test1_get_set():
    table = 'test'

    val_int = 2342
    val_float = 1.337
    val_str = str(uuid.uuid4())
    val_list = list(val_str)
    val_dict = {
        'val_int': val_int,
        'val_float': val_float,
        'val_str': val_str,
        'val_list': val_list,
    }

    for key, value in val_dict.items():
        db.set(key, value, table)
        ret_value = db.get(key, table)
        assert ret_value == value
        assert type(ret_value) is type(value)

    string_test = (
        'Another String with \'" so called "quotation marks",\n'
        'a linebreak, emoji👍  and a key with spaces in it!.'
    )
    db.set('string test', string_test, table)
    ret_value = db.get('string test', table)
    assert ret_value == string_test

    db.set('val_dict', val_dict, table)
    ret_value = db.get('val_dict', table)
    assert ret_value == val_dict

    db.drop_table(table)
    assert table not in db.tables()


def test2_set_changes():
    key = 'test_entry'
    table = 'test_table'
    # set to something different than default:
    defaults = {'some': str(uuid.uuid4()), 'value': 123}
    changes = {'value': 124}
    db.set_changes(key, changes, defaults, table)
    now = db.get(key, table)
    assert now['value'] != defaults['value']

    # change to default
    changes['value'] = 123
    db.set_changes(key, changes, defaults, table)
    now = db.get(key, table)
    assert now is None
    assert key not in db.keys(table)

    # set something that's not in defaults:
    changes = {'blah': 'rabbits'}
    db.set_changes(key, changes, defaults, table)
    now = db.get(key, table)
    assert now == changes
    db.pop(key, table)
    assert key not in db.keys(table)
    db.drop_table(table)
    assert table not in db.tables()


def test3_get_changes():
    key = 'test_entry'
    table = 'test_table'

    # test nothing set at all
    defaults = {'some': str(uuid.uuid4()), 'value': 13374223}
    fetched = db.get_changes(key, defaults, table)
    assert defaults['some'] == fetched['some']
    assert defaults['value'] == fetched['value']

    # test set changes, get different and same
    changes = {'value': 8888, 'something_else': 'H2FH2WK2EGF1KKU2SDK'}
    db.set_changes(key, changes, defaults, table)
    fetched = db.get_changes(key, defaults, table)
    assert defaults['some'] == fetched['some']
    assert defaults['value'] != fetched['value']
    db.pop(key, table)
    assert key not in db.keys(table)
    db.drop_table(table)
    assert table not in db.tables()


def test4_shutdown():
    db.disconnect()
    os.remove(temp_db_path)
    assert not os.path.isfile(temp_db_path), 'temp_db file still exists!'


if __name__ == '__main__':
    import pytest

    pytest.main([__file__, '-v'])
