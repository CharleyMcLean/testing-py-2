import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage works"""

        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        """Test for no rsvp"""

        result = self.client.get("/")
        self.assertIn("Please RSVP", result.data)
        self.assertNotIn("Party Details", result.data)

    def test_rsvp(self):
        """Test RSVP"""
        
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertNotIn("Please RSVP", result.data)
        self.assertIn("Party Details", result.data)

class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        """Check /games route using testdb"""
        result = self.client.get("/games")
        self.assertIn("Monopoly", result.data)


if __name__ == "__main__":
    unittest.main()
