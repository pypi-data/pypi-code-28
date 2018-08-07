"""
Copyright 2017-2018 Government of Canada - Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import json
import re

from binascii import hexlify, unhexlify
from math import ceil, log
from typing import Any, Union

from von_anchor.error import BadWalletQuery


ENCODE_PREFIX = {
    str: 1,
    bool: 2,
    int: 3,
    float: 4,
    None: 9
}

DECODE_PREFIX = {ENCODE_PREFIX[k]: k for k in ENCODE_PREFIX if k and k != str}


I32_BOUND = 2**31
def encode(raw_value: Any) -> str:
    """
    Encode credential attribute value, leaving any (stringified) int32 alone: indy-sdk predicates
    operate on int32 values properly only when their encoded values match their raw values.

    To disambiguate for decoding, the operation reserves a sentinel for the null value and otherwise adds
    2**31 to any non-trivial transform of a non-int32 input, then prepends a digit marking the input type:
    * 1: string
    * 2: boolean
    * 3: non-32-bit integer
    * 4: floating point
    * 9: other (stringifiable)

    :param raw_value: raw value to encode
    :return: encoded value
    """

    if raw_value is None:
        return str(I32_BOUND)  # sentinel

    stringified = str(raw_value)
    if isinstance(raw_value, bool):
        return '{}{}'.format(
            ENCODE_PREFIX[bool],
            I32_BOUND + 2 if raw_value else I32_BOUND + 1)  # sheesh: python bool('False') = True; just use 2 sentinels
    if isinstance(raw_value, int) and -I32_BOUND <= raw_value < I32_BOUND:
        return stringified  # it's an i32, leave it (as numeric string)

    hexed = '{}{}'.format(
        ENCODE_PREFIX.get(type(raw_value), ENCODE_PREFIX[None]),
        str(int.from_bytes(hexlify(stringified.encode()), 'big') + I32_BOUND))

    return hexed


def decode(value: str) -> Union[str, None, bool, int, float]:
    """
    Decode encoded credential attribute value.

    :param value: numeric string to decode
    :return: decoded value, stringified if original was neither str, bool, int, nor float
    """

    assert value.isdigit() or value[0] == '-' and value[1:].isdigit()

    if -I32_BOUND <= int(value) < I32_BOUND:  # it's an i32: it is its own encoding
        return int(value)
    if int(value) == I32_BOUND:
        return None

    (prefix, value) = (int(value[0]), int(value[1:]))
    ival = int(value) - I32_BOUND
    if ival == 0:
        return ''  # special case: empty string encodes as 2**31
    if ival == 1:
        return False  # sentinel for bool False
    if ival == 2:
        return True  # sentinel for bool True

    blen = ceil(log(ival, 16)/2)
    ibytes = unhexlify(ival.to_bytes(blen, 'big'))
    return DECODE_PREFIX.get(prefix, str)(ibytes.decode())


def raw(orig: Any) -> dict:
    """
    Stringify input value, empty string for None.

    :param orig: original attribute value of any stringifiable type
    :return: stringified raw value
    """

    return '' if orig is None else str(orig)


def cred_attr_value(orig: Any) -> dict:
    """
    Given a value, return corresponding credential attribute value dict for indy-sdk processing.

    :param orig: original attribute value of any stringifiable type
    :return: dict on 'raw' and 'encoded' keys for indy-sdk processing
    """
    return {'raw': raw(orig), 'encoded': encode(orig)}


def canon(raw_attr_name: str) -> str:
    """
    Canonicalize input attribute name as it appears in proofs and credential offers: strip out
    white space and convert to lower case.

    :param raw_attr_name: attribute name
    :return: canonicalized attribute name
    """

    if raw_attr_name:  # do not dereference None, and '' is already canonical
        return raw_attr_name.replace(' ', '').lower()
    return raw_attr_name


def canon_wql(query: dict) -> dict:
    """
    Canonicalize WQL attribute marker and value keys for input to indy-sdk wallet credential filtration.
    Canonicalize original values to proper indy-sdk raw values as per raw().

    Raise BadWalletQuery for WQL mapping '$or' to non-list.

    :param query: WQL query
    :return canonicalized WQL query dict
    """

    for k in query:
        attr_match = re.match('attr::([^:]+)::(marker|value)$', k)
        if isinstance(query[k], dict):  # only subqueries are dicts: recurse
            query[k] = canon_wql(query[k])
        if k == '$or':
            if not isinstance(query[k], list):
                raise BadWalletQuery('Bad WQL; $or value must be a list in {}'.format(json.dumps(query)))
            query[k] = [canon_wql(subq) for subq in query[k]]
        if attr_match:
            qkey = 'attr::{}::{}'.format(canon(attr_match.group(1)), attr_match.group(2))
            query[qkey] = query.pop(k)
            tag_value = query[qkey]
            if isinstance(tag_value, dict) and len(tag_value) == 1:
                if '$in' in tag_value:
                    tag_value['$in'] = [raw(val) for val in tag_value.pop('$in')]
                else:
                    wql_op = set(tag_value.keys()).pop()  # $neq, $gt, $gte, etc.
                    tag_value[wql_op] = raw(tag_value[wql_op])
            else:  # equality
                query[qkey] = raw(query[qkey])

    return query
