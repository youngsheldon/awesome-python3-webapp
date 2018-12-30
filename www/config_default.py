#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = 'Michael Liao'

configs = {
    'debug': True,
    'db': {
        'host': '192.168.31.11',
        'port': 3306,
        'user': 'sheldon',
        'password': 'sheldon',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}
