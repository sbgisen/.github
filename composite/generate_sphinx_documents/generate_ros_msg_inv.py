#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2022 SoftBank Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import zlib

import bs4
import requests

inventory_header = u'{}\n{}\n{}\n{}\n'.format(
    '# Sphinx inventory version 2',
    '# Project: ROS Message',
    '# Version: 2.0',
    '# The remainder of this file is compressed with zlib.').encode('utf-8')

payloads = []
response = requests.get('https://docs.ros.org/en/noetic/api/').text
soup = bs4.BeautifulSoup(response, "html.parser")
message_types = ['msgs', 'srvs', 'actions']
for package in soup.select('a'):
    package_name = package.text[:-1]
    message_type = None
    if package_name.endswith('msgs'):
        message_type = 'msg'
    elif package_name.endswith('actions'):
        message_type = 'action'
    elif package_name.endswith('srvs'):
        message_type = 'srv'
    if message_type:
        try:
            response = requests.get('https://docs.ros.org/en/noetic/api/'
                                    + package_name + '/html/{}/'.format(message_type)).text
        except BaseException:
            continue
        soup = bs4.BeautifulSoup(response, "html.parser")
        for elem in soup.select('a'):
            if '.html' not in elem.text:
                continue
            message = elem.text.split('.')[0]
            if message_type == 'action':
                action_suffix = ('Action', 'Goal', 'Feedback', 'Result',
                                 'ActionGoal', 'ActionFeedback', 'ActionResult')
                for suffix in action_suffix:
                    payloads.append(
                        f'{package_name}.msg._{message}.{message} '
                        + f'py:class 1 {package_name}/html/{message_type}/{elem.text} {message}')
            else:
                payloads.append(
                    f'{package_name}.{message_type}._{message}.{message} '
                    + f'py:class 1 {package_name}/html/{message_type}/{elem.text} {message}')
payloads.append('rospy.Time py:class 1 rospy/html/rospy.rostime.Time-class.html -')
payloads.append('rospy.Duration py:class 1 rospy/html/rospy.rostime.Duration-class.html -')
inventory_payload = '{}'.format('\n'.join(payloads)).encode('utf-8') + '\n'.encode('utf-8')

# inventory_payload lines spec:
#   name domainname:type priority uri dispname
#
# * `name`       -- fully qualified name
# * `domainname` -- sphinx domain name
# * `type`       -- object type specified by domain (ex. label, module)
# * `uri`        -- relative uri with anchor
# * `dispname`   -- name to display when searching/linking
# * `priority`   -- how "important" the object is
#                   (determines placement in search results)
#
#   - 1: default priority (placed before full-text matches)
#   - 0: object is important (placed before default-priority objects)
#   - 2: object is unimportant (placed after full-text matches)
#   - -1: object should not show up in search at all

inventory = inventory_header + zlib.compress(inventory_payload)
open('ros_msgs.inv', 'wb').write(inventory)
