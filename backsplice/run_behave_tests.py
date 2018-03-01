#!/usr/bin/env python

import os

test_path = './website/tests/behave/features/'

features = ['course_catalog', 
          'edit_course_catalog',
         ]

current_directory = os.getcwd()
for feature in features:
    os.chdir(test_path + feature)
    os.system('/usr/bin/env python ' + current_directory + '/manage.py behave')
    os.chdir(current_directory)

