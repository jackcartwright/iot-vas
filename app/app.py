import sys

from flask import Flask
from flask_restful import Resource, Api

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform

from lxml import etree

from werkzeug.middleware.proxy_fix import ProxyFix


path = '/run/gvmd/gvmd.sock'
connection = UnixSocketConnection(path=path)
transform = EtreeCheckCommandTransform()

# default username with greenbone containers
username = 'admin'

# default password with greenbone containers
# CHANGE ACCORDING TO:
# https://greenbone.github.io/docs/latest/22.4/container/index.html#setting-up-an-admin-user
# AFTER docker compose up -d
password = 'admin'

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1
)
api = Api(app)

class version(Resource):
    def get(self):
        with Gmp(connection=connection, transform=transform) as gmp:
            response = gmp.get_version()
            vers = response.xpath('version/text()')[0]
        return {'version': vers}

class scanners(Resource):
    def get(self):
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                response = gmp.get_scanners()
                scanners = response.xpath('scanner/@id')
                names = response.xpath('scanner/name/text()')
            return {'scanners': scanners, 'names': names}
        except GvmError as e:
            return {'error': '1'}

class configs(Resource):
    def get(self):
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                response = gmp.get_scan_configs()
                ids = response.xpath('config/@id')
                names = response.xpath('config/name/text()')
            return {'configs': ids, 'names': names}
        except GvmError as e:
            return {'error': '1'}

class port_lists(Resource):
    def get(self):
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                response = gmp.get_port_lists()
                ids = response.xpath('port_list/@id')
                names = response.xpath('port_list/name/text()')
            return {'port_lists': ids, 'names': names}
        except GvmError as e:
            return {'error': '1'}

api.add_resource(version, '/version')
api.add_resource(scanners, '/scanners')
api.add_resource(configs, '/configs')
api.add_resource(port_lists, '/port_lists')

if __name__ == '__main__':
    app.run(debug=True)
