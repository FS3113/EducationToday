import unittest
from get_data_from_multiple_lists import view_html_structure


class MyTestCase(unittest.TestCase):
    def test_data_separated_in_too_many_lists(self):
        r = view_html_structure('https://english.ufl.edu/faculty-listing/')
        self.assertEqual(r[0]['Name'].replace(' ', '').replace('"', ''), 'UwemAkpan')
        self.assertEqual(r[1]['Name'].replace(' ', '').replace('"', ''), 'ApolloAmoko')
        self.assertEqual(r[2]['Name'].replace(' ', '').replace('"', ''), 'PietroBianchi')
        self.assertEqual(r[3]['Name'].replace(' ', '').replace('"', ''), 'CamilleBordas')
        self.assertEqual(r[4]['Name'].replace(' ', '').replace('"', ''), 'MarshaBryant')
        self.assertEqual(r[5]['Name'].replace(' ', '').replace('"', ''), 'RichardBurt')
        self.assertEqual(r[-1]['Name'].replace(' ', '').replace('"', ''), 'RaeX.Yan')

        self.assertEqual(r[0]['Research Interest'], 'Creative Writing (Fiction)')
        self.assertEqual(r[0]['Position'], 'Assistant Professor')
        self.assertEqual(r[-1]['Research Interest'], 'Victorian Literature and Culture, Literature and Science, Digital Humanities')
        self.assertEqual(r[-1]['Position'], 'Assistant Professor')


    def test_research_interest_separated_in_different_tags(self):
        r = view_html_structure('https://www.eecs.mit.edu/people/faculty-advisors')
        self.assertEqual(r[0]['Name'], 'Hal Abelson')
        self.assertEqual(r[0]['Email'], 'hal@mit.edu')
        self.assertEqual(r[0]['Position'], 'Class of 1922 Professor ')
        self.assertEqual(r[0]['Research Interest'], 'CSAIL AI Connections Cybersecurity')
        self.assertEqual(r[1]['Research Interest'], 'RLE InfoSys Biomed bio-EECS')
        self.assertEqual(r[2]['Research Interest'], 'Systems Wireless')
        self.assertEqual(r[3]['Research Interest'], 'CSAIL')


if __name__ == '__main__':
    unittest.main()
