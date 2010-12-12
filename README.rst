Sherd: DDoS Resistant Static Generator
======================================

Suppose you have a static website that serves documents.  Perhaps they're
politically sensitive, likely to be censored, or for any other reason, you're
concerned about the thread of DDoS.  You can't rely on hosting on the cloud
(companies may not have your back), or maybe you can't afford it.

The easy and obvious solution is to mirror your files far and wide.  That way,
if any one site goes offline, the others remain accessible.  The problem with
this is that you lose the main currency of the web: the ability to link
consistently and reliably to your documents.  Links break when the main site
goes down.

``sherd`` is one solution to this.  It is a generator that creates an AJAX
frontend to your static website, and loads the contents of each page from
mirrors.  All you have to do to keep your site online is maintain the domain
name, keep your mirrors up-to-date, and on the main domain, serve a single,
small bootstrapping HTML file -- everything else goes to the mirrors.  URLs for
the original static site are turned into AJAX paths::

    http://example.com         -> http://example.com/#/
    http://example.com/id/123  -> http://example.com/#/id/123
    http://example.com/#anchor -> http://example.com/#/index.html#anchor

The bootstrapping file (http://example.com/index.html) is only about 2KB, and
is the only thing example.com will ever have to serve, making it much easier to
withstand floods of traffic.  All other content is taken from random mirrors,
while preserving the top-level domain.  If a mirror goes offline, the remaining
mirrors are seamlessly used in its place.  If for some reason the gateway
(http://example.com) goes offline, any of the remaining mirrors still work to
serve the files as before.

Usage
-----

To use::

    ./sherd.py <source dir> <output dir> <mirror list>

* ``source dir`` is a directory containing the static website to sherd-ify
* ``output dir`` is the destination into which to copy files
* ``mirror list`` is a textfile listing the URLs of mirrors, one per line.

After running sherd, sync the ``output dir`` to all of your mirrors, and you're
good to go.

About
-----

Written by Charlie DeTar.  Licensed under the MIT License:

Copyright (c) 2011 Charlie DeTar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
