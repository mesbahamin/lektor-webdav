# -*- coding: utf-8 -*-
import requests
import subprocess
from collections import namedtuple
from lektor.pluginsystem import Plugin, get_plugin
from xml.etree.ElementTree import parse, fromstring


WebdavFile = namedtuple('WebdavFile', ['path', 'name', 'content_type'])


def webdav_ls_file_names(webdav_id, path = None, **_):
    """Return a list of file names present in a webDAV folder"""
    return [f.name for f in webdav_ls_files(webdav_id, path)]


def webdav_ls_file_paths(webdav_id, path = None, **_):
    """Return a list of paths to files present in a webDAV folder"""
    return [f.path for f in webdav_ls_files(webdav_id, path)]


def webdav_ls_files(webdav_id, path = None, **_):
    """Return a list of WebDavFile named tuples for files present in a webDAV
    folder"""
    plugin = get_plugin('webdav')

    url = plugin.get_webdav_config(webdav_id, 'url')
    if path is not None:
        url += path

    username = plugin.get_webdav_config(webdav_id, 'username')
    pass_cmd = plugin.get_webdav_config(webdav_id, 'passcmd')
    password = _exec_password_command(pass_cmd)

    propfind_body = """<?xml version="1.0" encoding="utf-8" ?>
        <D:propfind xmlns:D="DAV:">
            <D:prop>
                <D:displayname/>
                <D:getcontenttype/>
            </D:prop>
        </D:propfind>
        """

    r = requests.request(
            'PROPFIND',
            url,
            headers = {'Depth': '1', 'Content-Type': 'application/xml'},
            data = propfind_body,
            auth = (username, password))

    xml_response = fromstring(r.content)
    xml_namespaces = {'D': 'DAV:'}
    files = [
        WebdavFile(path = p.text, name = n.text, content_type = t.text)
        for (p, n, t) in zip(
            xml_response.iterfind('.//D:href', namespaces = xml_namespaces),
            xml_response.iterfind('.//D:displayname', namespaces = xml_namespaces),
            xml_response.iterfind('.//D:getcontenttype', namespaces = xml_namespaces))
        if 'directory' not in t.text
    ]
    return files


def webdav_zip(*args, **kwargs):
    """Jinja2 doesn't have a built in zip filter, so we supply one under the
    'webdav' namespace"""
    return zip(*args, **kwargs)


def _exec_password_command(pass_cmd, timeout = 30):
    """Execute a command that returns a password"""
    list_of_args = pass_cmd.split(' ')
    out_bytes = subprocess.check_output(list_of_args)
    password = out_bytes.decode('utf-8')
    return password


class WebdavPlugin(Plugin):
    name = 'lektor-webdav'
    description = 'Get a list of files on a webdav server.'

    def get_webdav_config(self, webdav_id, key):
        return self.get_config().get('{}.{}'.format(webdav_id, key))

    def on_setup_env(self, **_):
        self.env.jinja_env.globals.update(webdav_ls_file_names = webdav_ls_file_names)
        self.env.jinja_env.globals.update(webdav_ls_file_paths = webdav_ls_file_names)
        self.env.jinja_env.globals.update(webdav_ls_files = webdav_ls_files)
        self.env.jinja_env.filters['webdav_zip'] = webdav_zip
