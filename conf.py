#!/usr/bin/env python

"""
    Django CleverCSS Configuration
"""

import os

from django.conf import settings

"""
    The following is the name used both to get CCSS files from your template
    directories and to render CSS files into your MEDIA_ROOT. For example,
    if you have /foo/templates set as your TEMPLATE_DIRS, /foo/media set as
    your MEDIA_ROOT, "styles" set as your CSS_PATH, and a file called
    /foo/templates/styles/screen.ccss, then the generated CSS file will be
    named /foo/media/styles/screen.css.
"""
CSS_PATH = getattr(settings, "CSS_PATH", "styles")
