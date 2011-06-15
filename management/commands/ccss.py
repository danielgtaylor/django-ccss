#!/usr/bin/env python

"""
    Django command to generate CSS from CleverCSS templates.
"""

import glob
import os

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template import Context
from django.template.loader import render_to_string
from django.template.loaders.app_directories import app_template_dirs

from ... import conf
from ...contrib.clevercss import convert


class Command(BaseCommand):
    """
        A command to generate CSS files from CleverCSS templates stored in
        any of your Django template directories. You can either pass
        explicit filenames into the command or let if scan for outdated
        files in your template and app template directories. The output
        will be written to your media root, ready to be served.
    """
    option_list = BaseCommand.option_list + (
        make_option("-a", "--all", dest="all", default=False,
                    action="store_true", help="Regenerate all CSS files"),
    )
    help = "Generate CSS files from CleverCSS templates."
    args = "[file1.css file2.css ...]"

    def handle(self, *args, **options):
        """
            Check arguments, find outdated files if necessary, and generate new
            CSS files from the CleverCSS templates that can be found.
        """
        verbosity = int(options.get("verbosity", 1))
        genall = options.get("all", False)

        if genall and args:
            raise CommandError("Files and --all are mutually exclusive " \
                               "options!")

        # Get the base output path in which to create CSS files
        outpath = os.path.join(settings.MEDIA_ROOT, conf.CSS_PATH)

        if args:
            # Process a specific list of files
            filenames = args
        else:
            # Try to get all CleverCSS templates and process them. Note that
            # this ONLY works for template directories, not eggs, zip files, or
            # other custom loaders. It searches both TEMPLATE_DIRS and any
            # app template directories like the Django loaders.
            filenames = set()

            if verbosity > 1:
                print "Scanning for templates..."

            for template_path in settings.TEMPLATE_DIRS + app_template_dirs:
                # The path in which to look for CleverCSS templates
                path = os.path.join(template_path, conf.CSS_PATH)

                # Walk the path and recursively find all CleverCSS templates
                for root, dirs, files in os.walk(path):
                    # Filter out any other files we don't care about
                    for template in [f for f in files if f.endswith(".ccss") \
                                         and not f.startswith(".#")]:
                        # The directory relative to the template + css path
                        # root
                        reldir = os.path.dirname(os.path.join(root,
                                                  template)[len(path) + 1:])
                        # The name of the template without its extension
                        base = ".".join(template.split(".")[:-1])
                        # Full output CSS path
                        outfile = os.path.join(outpath, reldir, base + ".css")

                        # Only generate if input is newer or --all was passed!
                        if genall or not os.path.exists(outfile) or \
                                os.path.getmtime(outfile) < \
                                os.path.getmtime(os.path.join(root, template)):
                            # Add the relative path to the CleverCSS template
                            filenames.add(os.path.join(reldir, template))
                        elif verbosity > 1:
                            print "%s.css is up to date" % \
                                                    os.path.join(reldir, base)


            if verbosity > 1:
                print "Found %d out of date templates" % len(filenames)

        if verbosity > 1 and filenames:
            print "Processing templates..."

        for entry in filenames:
            # Get path names for input and output files
            base = ".".join(entry.split(".")[:-1])
            infile = os.path.join(conf.CSS_PATH, base + ".ccss")
            outfile = os.path.join(outpath, base + ".css")

            # Make sure the output path exists, then write the generated CSS
            if not os.path.exists(os.path.dirname(outfile)):
                os.makedirs(os.path.dirname(outfile))

            open(outfile, "w").write(convert(render_to_string(infile)))

            if verbosity > 0:
                print "Generated %s.css" % base

        if verbosity > 1 and not filenames:
            print "All CSS files are up to date."
