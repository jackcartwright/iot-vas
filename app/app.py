from flask import Flask, request, make_response, abort

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform
from gvm.protocols.gmpv224 import ReportFormatType

from lxml import etree

from werkzeug.middleware.proxy_fix import ProxyFix

from markupsafe import escape

from base64 import b64decode

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

@app.route("/version")
def get_version():
    with Gmp(connection=connection, transform=transform) as gmp:
        response = gmp.get_version()
        vers = response.xpath('version/text()')[0]
    return {'version': vers}

@app.route("/scanners")
def get_scanners():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_scanners()
            scanners = response.xpath('scanner/@id')
            names = response.xpath('scanner/name/text()')
        return {'scanners': scanners, 'names': names}
    except GvmError as e:
        abort(500)

@app.route("/configs")
def get_configs():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_scan_configs()
            ids = response.xpath('config/@id')
            names = response.xpath('config/name/text()')
        return {'configs': ids, 'names': names}
    except GvmError as e:
        abort(500)

@app.route("/port_lists")
def get_port_lists():
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            response = gmp.get_port_lists()
            ids = response.xpath('port_list/@id')
            names = response.xpath('port_list/name/text()')
        return {'port_lists': ids, 'names': names}
    except GvmError as e:
        abort(500)

@app.route("/create_task", methods = ['POST'])
def create_task():
    request_json = request.json
    if request_json.keys() >= {"name", "host", "config_id", "scanner_id"}:
        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username, password)
                target_id = gmp.create_target(name=request_json['name'], hosts=[request_json['host']], port_range='T:1-65535,U:1-65535').xpath('@id')
                task_id = gmp.create_task(name=request_json['name'], config_id=request_json['config_id'], target_id=target_id[0], scanner_id=request_json['scanner_id']).xpath('@id')
            return {'UUID': task_id[0]}
        except GvmError as e:
            abort(500)
    else:
        abort(400)

@app.route("/report/<uuid:report_id>.pdf", methods = ['GET'])
def get_report(report_id):
    try:
        with Gmp(connection=connection, transform=transform) as gmp:
            gmp.authenticate(username, password)
            report = gmp.get_report(report_id=escape(report_id), report_format_id=ReportFormatType.PDF)
            content = report.xpath('report/text()')[0]
            pdf_bytes = b64decode(content.encode("ascii"))
            response = make_response(pdf_bytes)
            response.headers.set('Content-Type', 'application/pdf')
            return response
    except GvmError as e:
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)
