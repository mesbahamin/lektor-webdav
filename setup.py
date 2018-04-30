from setuptools import setup

setup(
    name='lektor-webdav',
    version='0.1',
    author=u'Amin Mesbah',
    author_email='dev@aminmesbah.com',
    license='MIT',
    py_modules=['lektor_webdav'],
    entry_points={
        'lektor.plugins': [
            'webdav = lektor_webdav:WebdavPlugin',
        ]
    },
    install_requires=[
        'requests'
    ]
)
