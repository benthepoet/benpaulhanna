#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ben Hanna'
SITENAME = u'(\u03BBx.x) Ben Hanna'
SITEURL = ''

SITESUBTITLE = 'Software Engineer and Functional Programming Enthusiast'

PATH = 'content'

TIMEZONE = 'America/Detroit'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)
          
ICONS = (('github', 'https://github.com/benthepoet'),
         ('stack-overflow', 'https://stackoverflow.com/users/8171618/ben-hanna'),
         ('linkedin', 'https://www.linkedin.com/in/ben-hanna-0a275135'),)

DEFAULT_PAGINATION = 10

DISPLAY_CATEGORIES_ON_MENU = True
HIDE_AUTHORS = True

THEME = 'themes/pelican-alchemy/alchemy'

