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
