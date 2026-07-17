# Copyright (c) 2026 Splunk Inc.
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
import unittest

from statuspage_consts import quote_incident_id


class QuoteIncidentIdTests(unittest.TestCase):
    def test_leaves_a_normal_incident_id_unchanged(self):
        self.assertEqual(quote_incident_id("mtm9zphxc6sn"), "mtm9zphxc6sn")

    def test_encodes_path_and_query_characters(self):
        value = quote_incident_id("../subscribers?")

        self.assertEqual(value, "..%2Fsubscribers%3F")
        self.assertNotIn("/", value)
        self.assertNotIn("?", value)

    def test_rejects_dot_segments(self):
        self.assertIsNone(quote_incident_id("."))
        self.assertIsNone(quote_incident_id(".."))
