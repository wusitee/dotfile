#!/usr/bin/python
import http.client
import json
import socket
import sys
import time

NODE = '🇨🇳 台湾 07 家宽'
SOCKET = '/run/mihomo/controller.sock'


class Controller(http.client.HTTPConnection):
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(SOCKET)


def request(method, path, body=None):
    connection = Controller('localhost', timeout=3)
    try:
        connection.request(method, path, body=json.dumps(body) if body else None,
                           headers={'Content-Type': 'application/json'})
        response = connection.getresponse()
        data = response.read()
        if response.status >= 300:
            raise RuntimeError('Mihomo controller returned HTTP ' + str(response.status))
        return json.loads(data) if data else None
    finally:
        connection.close()


try:
    if sys.argv[1:] == ['select']:
        for attempt in range(30):
            try:
                request('PUT', '/proxies/GLOBAL', {'name': NODE})
                break
            except (OSError, http.client.HTTPException):
                time.sleep(0.5)
        else:
            raise RuntimeError('Mihomo controller did not start')
    elif sys.argv[1:] != ['check']:
        raise RuntimeError('Usage: mihomo-route.py select|check')

    config = request('GET', '/configs')
    route = request('GET', '/proxies/GLOBAL')
    if config.get('mode') != 'global' or not config.get('tun', {}).get('enable'):
        raise RuntimeError('TUN must be enabled and mode must be Global')
    if route.get('type') != 'Selector' or route.get('now') != NODE:
        raise RuntimeError('Select the fixed Taiwan 家宽 node in GLOBAL')
    print('Proxy check passed: TUN enabled; Global → ' + NODE, file=sys.stderr)
except (OSError, ValueError, RuntimeError, http.client.HTTPException) as error:
    print('Proxy check failed: ' + str(error), file=sys.stderr)
    sys.exit(1)
