#!/usr/bin/python
from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_bytes
from ansible.module_utils.six import string_types
from Crypto.Hash import MD4


class FilterModule(object):
    def filters(self):
        return {'nt_hash': self.nt_hash}

    def nt_hash(self, data):
        if isinstance(data, string_types):
            try:
                h = MD4.new()
                encdata = str(data).encode('utf-16le')
            except Exception as exc:
                raise AnsibleFilterError(exc)
            h.update(to_bytes(encdata, errors='surrogate_or_strict'))
            return h.hexdigest()
        return data
