#!/usr/bin/env python

"""
    Django CleverCSS Configuration
"""

import os

from django.conf import settings

"""
    The following are used to get CCSS files from your template
    directories and to render CSS files into your MEDIA_ROOT. For example,
    if you have /foo/templates set as your TEMPLATE_DIRS, /foo/media set as
    your MEDIA_ROOT, "baz" set as your CCSS_PATH, "bar" set as your CSS_PATH, and a file called
    /foo/templates/baz/screen.ccss, then the generated CSS file will be
    named /foo/media/bar/screen.css.

    By default CCSS_PATH is set to be the same as CSS_PATH
"""
CSS_PATH = getattr(settings, "CSS_PATH", "styles")
CCSS_PATH = getattr(settings, "CSS_OUT_PATH", CSS_PATH)
