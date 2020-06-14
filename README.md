# vgloss
A web-based media organization program.

WARNING: This is still in active development and not ready for production use.


## Development Setup

Python requirements:

    $ pip install -r dev-requirements.txt
    $ pip install -e .

External requirements:

  * libvips - $ apt install libvips-tools
  * exiftool - $ apt install libimage-exiftool-perl

vgloss commands are run using the `vgloss` executable. By default it uses the
current directory as base, but you can use `VGLOSS_BASE` to specify another
base. To start, you'll need to initialize a folder as a vgloss gallery:

    $ VGLOSS_BASE=test1/ vgloss init

To develop, run Django dev server on port 8000 and run webpack server on port
8001, forwarding non-js requests to port 8000. Go to port 8001 to develop JS:

    $ VGLOSS_BASE=test1/ vgloss serve
    $ yarn run serve --port 8001 --hot

Files are scanned on init and at the start of serve. To recognize changes on
the filesystem without re-running serve, use the scan command:

    $ VGLOSS_BASE=test1/ vgloss scan

Tests are located in `tests/` and can be run like a normal Django application:

    $ ./manage.py test


## Hacking

  * vgloss/ - The vgloss Python package, which is a Django application.
    * dist/ - Destination for Javascript build.
  * src/ - Javascript source.
  * public/ - Static assets copied to vgloss/dist/.

**Django Application**: vgloss is a Django application with settings in
"vgloss/settings.py". Running the "vgloss" command runs `vgloss.main.main()`,
which sets up Django with that settings file. "manage.py" also is hardcoded to
use the same settings file.

**Base Directory**: Unlike a typical Django application, vgloss does not have a
fixed location for the database. Instead, data files are all relative to the
`BASE_DIR` setting, which is the current directory if not overwritten by the
`VGLOSS_BASE` environment variable. All metadata for vgloss is stored in
`<BASE_DIR>/.vgloss/`, the so called "data directory" pointed to by the
`DATA_DIR` setting. Here are some data files of interest:

  * `<BASE_DIR>/.vgloss/db.sqlite3`
  * `<BASE_DIR>/.vgloss/thumbnails/`

**Serving files**: Files are served through Django in production (although this
should probably change in the future). URLs which aren't recognized as files or
APIs are served a static file from `vgloss/dist/`, which contains the JS which
in turn makes API requests. Any path not recognized is served "index.html" (see
`vgloss/urls.py`) so JS can read the URL and display the correct page, which is
typical of projects using Vue router. When developing using the webpack dev
server the situation is acutally reversed: webpack passes certain URLs to
Django and serves the rest itself (see `vue.config.js`).

**File Model**: Except for serving the original files themselves, all metadata
is scanned beforehand and thumbnails are saved. The `File` model holds this
metadata. Notice that it's primary key is the hash of a file. If the same file
exists more than once on the filesystem, only one `File` instance will be
created.

**FilePath Model**: Since we only create one `File` instance when a file is
duplicated, this is where we store where those files are actually located on
the filesystem. `FilePath` has a foreign key to `File`.


## Acknowledgments

Folder SVG taken from: https://www.svgrepo.com/svg/97469/folder
