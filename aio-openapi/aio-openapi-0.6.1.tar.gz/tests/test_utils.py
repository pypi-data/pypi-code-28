import pytest

from openapi import utils
from openapi.exc import JsonHttpException, ImproperlyConfigured
from openapi.json import dumps
from openapi.db import utils as db


def test_env():
    assert utils.get_env() == 'test'


def test_debug_flag():
    assert utils.get_debug_flag() is False


def test_json_http_exception():
    ex = JsonHttpException(status=401)
    assert ex.status == 401
    assert ex.text == dumps({'message': 'Unauthorized'})
    assert ex.headers['content-type'] == 'application/json; charset=utf-8'


def test_json_http_exception_reason():
    ex = JsonHttpException(status=422, reason='non lo so')
    assert ex.status == 422
    assert ex.text == dumps({'message': 'non lo so'})
    assert ex.headers['content-type'] == 'application/json; charset=utf-8'


def test_exist_database_none():
    with pytest.raises(ImproperlyConfigured):
        db.create_tables({})


def test_replace_key():
    assert utils.replace_key({}, 'foo', 'bla') == {}
    assert utils.replace_key({'foo': 5}, 'foo', 'bla') == {'bla': 5}
