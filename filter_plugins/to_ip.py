from IPy import IP
import socket
from ansible.module_utils._text import to_native
from ansible.errors import AnsibleError

class FilterModule(object):
    def filters(self):
        return {'to_ip': self.to_ip}

    def str_to_ip(self, item):
        try:
            IP(item)
        except:
            try:
                return socket.gethostbyname(item)
            except Exception as e:
                raise AnsibleError('Failed to lookup hostname "' + item + '": ' % to_native(e))
        return item

    def list_to_ips(self, items):
        ret = []
        for item in items:
            ret.append(self.str_to_ip(item))
        return ret

    def to_ip(self, item):
        if type(item) is list:
            return self.list_to_ips(item)
        elif type(item) is str:
            return self.str_to_ip(item)
        else:
            raise AnsibleError("Cannot handle type " % type(item))
