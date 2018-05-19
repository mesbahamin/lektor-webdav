import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'lektor-webdav',
    version = '0.1.1.post5',
    url = 'https://github.com/mesbahamin/lektor-webdav',

    author = 'Amin Mesbah',
    author_email = 'dev@aminmesbah.com',
    license = 'MIT',

    project_urls = {
        'Source': 'https://github.com/mesbahamin/lektor-webdav',
        'Tracker': 'https://github.com/mesbahamin/lektor-webdav/issues',
    },

    description = 'Lektor plugin to get a list of files from a WebDAV server',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Lektor',
        'License :: OSI Approved :: MIT License',
    ],
    keywords = 'lektor webdav blog website files plugin',

    py_modules = ['lektor_webdav'],
    entry_points = {
        'lektor.plugins': [
            'webdav = lektor_webdav:WebdavPlugin',
        ]
    },
    install_requires = [
        'requests'
    ]
)
