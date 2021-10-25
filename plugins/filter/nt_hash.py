#!/usr/bin/python

import hashlib
from ansible.module_utils.six import iteritems, string_types, integer_types, reraise
from ansible.module_utils._text import to_bytes, to_native, to_text

class FilterModule(object):
    def filters(self):
        return {'nt_hash': self.nt_hash}

    def nt_hash(self, data):
        if isinstance(data, string_types):
            try:
                h = hashlib.new('md4')
                encdata = str(data).encode('utf-16le')
            except Exception as e:
                # hash is not supported?
                raise AnsibleFilterError(e)

            h.update(to_bytes(encdata, errors='surrogate_or_strict'))
            return h.hexdigest()
        return data

