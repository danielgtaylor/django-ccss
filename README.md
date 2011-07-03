Django CleverCSS
================
The django-ccss module provides a quick and simple way for you to integrate CleverCSS into your Django workflow. <a href="http://sandbox.pocoo.org/clevercss/">CleverCSS</a> is a Python-like syntax for generating CSS that supports nesting, variables, and a few other neat features, making it extremely useful for rapidly developing and managing complex CSS configurations. The goal of this module is to be as simple and straightforward as possible while speeding up the development of your Django site.

Features
--------
The django-ccss module has the following features:

 * Generate CSS from templates using any valid Django template loader
     * This includes files, app templates, eggs, etc
     * The loading order is the same as for any normal Django template
 * Automatically regenerate CSS using the development server
 * Manually generate CSS using the 'ccss' command
 * Requires no database tables, custom views or extra caching
 * The only dependency is Django itself

Installation & Overview
-----------------------
Installation of the django-ccss module is incredibly easy!

 1. Download the source to your Django project as 'ccss'
 1. Add 'ccss' to your INSTALLED_APPS in settings.py
 1. Create CleverCSS templates in any template directory
     * By default you must put the files under the styles directory (see settings)
     * You must name the templates with a .ccss extension
     * You may use any number of subfolders to organize your templates
 1. Run the development server with ./manage.py runserver
 1. Whenever you update your production servers, run ./manage.py ccss

Your CSS files will be in your MEDIA_ROOT under the styles directory by default.

Settings
--------
The following settings are available and can be set in your settings.py:

<table>
    <tr>
        <th>Name</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>CSS_PATH</td>
        <td>"styles"</td>
        <td>The path, relative to your MEDIA_ROOT, to put rendered CSS templates</td>
    </tr>
    <tr>
        <td>CCSS_PATH</td>
        <td>CSS_PATH</td>
        <td>The path, relative to your TEMPLATE_DIRS, to look for CleverCSS templates</td>
    </tr>
</table>


Limitations
-----------
While it is possible to load CleverCSS templates from Python eggs, zip files, and other more exotic sources it is not possible to query those sources for .ccss files easily. This means that those templates will not be automatically found and rendered to CSS; instead you must manually do so with e.g. ./manage.py ccss name1.ccss subdir/name2.ccss ... and if they are found by Django's template loaders the corresponding CSS files will be generated in your media path.

Quick Example
-------------
Still a bit confused? Here's a quick and dirty example. After adding 'ccss' to your INSTALLED_APPS create a 'templates' directory in the same location as this file you are currently reading. Inside of that directory create a 'styles' directory. Inside of there, create a file named test.ccss and put the following into it:

    basecolor = red;

    body:
        color: white
        background-color: black

    a:
        color: $basecolor
        text-decoration: underline

        &:hover:
            color: $basecolor.brighten(30)
            text-decoration: underline

Then run ./manage.py ccss and take a look in your MEDIA_ROOT at styles/test.css. That file can now be included like normal in your Django templates. When you've created a default view and base template that includes the CSS file, you can run ./manage.py runserver and go to http://localhost:8000/ in your browser like normal. Anytime you update your test.ccss file the test.css file will be automatically regenerated, all you need to do is hit refresh in your browser. When you deploy to a production server and no longer use the development server, use ./manage.py ccss to regenerate outdated CSS files.

Alternatives
------------
Several alternatives exist which provide similar functionality in different ways. While I believe they are more complex, more difficult to setup, and more difficult to use you may find that they are exactly what you need.

 * <a href="http://code.google.com/p/django-clevercss/">django-clevercss</a>
 * <a href="http://github.com/dziegler/django-css">django-css</a>

License
-------
Copyright (c) 2009 Daniel G. Taylor <dan@programmer-art.org>

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
