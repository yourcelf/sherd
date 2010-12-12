from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import os

root = os.path.abspath(os.path.dirname(__file__))
os.chdir(root)

master_file = open(os.path.join(root, ".git", "refs", "heads", "master"))
VERSION = '0.1.git-' + master_file.read().strip()
master_file.close()

# Make data go to the right place.
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

data_dir = "sherd/templates/"
data = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

setup(
    name='sherd',
    version=VERSION,
    description="Generator for DDoS and censorship resistant static web pages.",
    long_description="""
``sherd`` is a generator for static web pages which is designed with two aims:

 * Make the site as resistant to DDoS attacks as possible
 * Preserve the ability to have permanent links to files.

The scenario is this: you have a static web page (a web page that consists only
of html, images, and javascript), and you want to publish it on the web.
However, you're concerned that you might become a victim of DDoS attacks, or
censorship efforts which could prevent you from using large server farms.  You
could easily mirror your site to a lot of other domains in case the main site
is taken off-line.  But then the web loses the ability to link directly to
files on your site.

Sherd works by parsing a static document tree, and generating a javascript
front-end that loads pages in the background using AJAX.  The pages on your
site will have URLs like this:

    http://example.com/#/id/123

where ``/id/123`` is the path to the static file "123".  The index file (the
"gateway") hosted on http://example.com/ is a small html file that bootstraps
other files from mirrors, such as:

    http://example.mirror1.com
    http://example.mirror2.com
    http://mirror3.com/example

Thus, keeping http://example.com online is just a matter of serving a single,
few kilobyte HTML file, which can be heavily cached.  All other files go to the
mirrors.  If a mirror is taken off-line, the javascript works around the down
site and uses the other mirrors.  And even if example.com were to succumb and
be taken off-line, any of the mirrors can act as the gateway to the rest of
them just as easily.

To use sherd, simply invoke it with a source directory (which should be a
static HTML web site that uses relative linking for all internal links), an
output directory, and a text file with a list of mirrors (one per line):

    ./sherd.py <input dir> <output dir> <mirror list>

    """,
    author="Charlie DeTar",
    author_email="cfd@media.mit.edu",
    url="http://github.com/yourcelf/grocktx",
    license="MIT License",
    platforms=["any"],
    packages=['grocktx'],
    data_files=[(data_dir, data)],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
    ],
    include_package_data=True,
)
