#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from setuptools import find_packages, setup

setup(
    name = 'TracTicketAdminPlugin',
    version='1.0',
    packages = ['ticketadmin'],
    package_data = { 'ticketadmin': [] },

    author = 'Leif Högberg',
    author_email = 'leihog@gmail.com',
    description = 'Adds ticket related commands to trac-admin',
    long_description = open(os.path.join(os.path.dirname(__file__), 'README')).read(),
    url = 'https://github.com/leihog/TracTicketAdmin',
    license = 'BSD',

    install_requires = ['Trac>=0.12'],
    entry_points = {
        'trac.plugins': [
            'ticketadmin.api = ticketadmin.api',
        ],
    },
)