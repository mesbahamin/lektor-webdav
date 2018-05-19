# Lektor WebDAV Plugin

[![PyPI version shields.io](https://img.shields.io/pypi/v/lektor-webdav.svg)](https://pypi.python.org/pypi/lektor-webdav/)

Get a list of files hosted on a WebDAV server for use in your
[Lektor](https://www.getlektor.com/) templates.


## Installation

```
mkdir packages
cd packages
git clone https://github.com/mesbahamin/lektor-webdav
```

I'll try to set this up soon so it can be installed properly with `lektor
plugins add`.


## Configuration

For each WebDAV server you want to use, add a section in `configs/webdav.ini`:

```
[photos]
url = https://my.webdav.domain/photography/
username = my_user@example.com
passcmd = pass my_webdav_server
```

Replace 'photos' with whatever label you want for this particular webdav server.


### Options

|Option   | Description
|---------|-------------------------------------------------------------------------
|url      | URL of your WebDAV folder
|username | Username with which to authenticate with the WebDAV server
|passcmd  | A command that will return your WebDAV password as a UTF-8 string


## Use In Templates

This plugin exposes the following for use in Jinja2 templates:


### Functions

- `webdav_ls_files`
    - Return a list of all files (not folders) in a WebDAV directory. The files
      are returned in the form of a list of `WebdavFile` instances.
    - Parameters:
        - `webdav_id`. This is the name you chose as the section title in
          `webdav.ini` ('photos' in the above snippet).
        - `path` (optional). If you want to look in a subfolder of your WebDAV
          folder, pass its name in here.
- `webdav_ls_file_names`
    - Same as `webdav_ls_files`, but only return the names.
- `webdav_ls_file_paths`
    - Same as `webdav_ls_files`, but only return the paths.


### Tuples

- `WebdavFile`: A named tuple that holds information about a file.
    - `path`
        - The full path of the file with the WebDAV server's URL as its root.
        - Example: `'/photographs/my_photograph_of_a_wall.jpg'`
    - `name`
        - Just the name of the file itself.
        - Example: `'my_photograph_of_a_wall.jpg'`
    - `content_type`
        - Filetype metadata supplied by the WebDAV server.
        - Example: `'images/jpeg'`


### Filters

- `webdav_zip`
    - Jinja2 doesn't have a `zip` filter, so I included one here since I needed
      to pair up my photos with generated thumbnails (see example below).
    - Usage: `{{ zipped_iterator_ab = iterator_a|zip(iterator_b) }}`


## Example

I made this because I wanted to make a photo gallery on my blog. I already had
a webDAV server through my Fastmail account, and I wanted to host the images
there.

My full site configuration can be found
[here](https://github.com/mesbahamin/amin.space), but here are the main bits:


### Config

My `webdav.ini` looks like this:

```
[photography]
url = https://myfiles.fastmail.com/photography/
username = me@mydomain.com
passcmd = pass sync/fastmail_webdav
```

I using [pass](https://www.passwordstore.org/) to manage my passwords, so
I invoke it in `passcmd`.


### Template

The template for my photography page looks like this:

```
{% extends "layout.html" %}
{% block body %}
<h2>Photography</h2>
<section class="photos">
<div class="photo-list">
{% set photo_host_url = bag('photo_list', 'host_url') %}
{% set thumb_dimension = bag('photo_list', 'thumb_dimension') %}
{%
    for photo_file_name, thumbnail_file_name
    in (
        webdav_ls_file_names('photography')
        |webdav_zip(webdav_ls_file_names('photography', 'thumbnails')
    )
    |sort(reverse=True))
%}
    {% set photo_url = photo_host_url + photo_file_name %}
    {% set thumb_url = photo_host_url + 'thumbnails/' + thumbnail_file_name %}
    <div class="photo">
    <a href="{{ photo_url }}">
        <img src="{{ thumb_url }}" width="{{ thumb_dimension }}" height="{{ thumb_dimension }}"/>
    </a>
    </div>
{% endfor %}
</div>
</section>
{% endblock %}
```

I get a list of my WebDAV hosted photos and a list of pre-generated thumbnails.
Then I zip them together with `webdav_zip` and iterate through them
simultaneously.


### Result

My gallery page looks like [this](https://www.amin.space/photography/).

When I want to add more photos, I simply upload them to my WebDAV server, then
run `lektor build`.
