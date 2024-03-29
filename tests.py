from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the 
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is 
        # accessible throughout this test class). This way, we'll be able to 
        # rely on this user in our tests without needing to know the numeric 
        # value of their id, since it will change each time our tests are run. 
        self.user_id = test_user.id
        self.second_user_id = second_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_get_new_user_form(self):
        """Check if view function renders new user form"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- used for testing new user form -->", html)

    def test_get_new_user_info(self):
        """Check if new user form submission redirects to user list
        and database has new entry"""
        with self.client as c:
            resp = c.post('/users/new',
                            data={
                                'first_name':'sssass',
                                'last_name':'bbbbb',
                                'url' : 'image_url' })
            self.assertEqual(resp.status_code, 302)
            self.assertIn(resp.location, "http://localhost/users")
            user_ids = db.session.query(User.id).all()
            self.assertEqual(len(user_ids), 3)

    def test_delete(self):
        """Check if delete button redirects to user list
        and database has one less entry"""
        with self.client as c:
            resp = c.post(f'/delete_user/{self.user_id}')
            self.assertEqual(resp.status_code, 302)
            self.assertIn(resp.location, "http://localhost/users")
            self.assertEqual(User.query.filter(User.id==self.user_id).first(), None)

    def test_get_user_details(self):
        """Check if clicking on user list link properly renders user details"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- user details for testing -->", html)
            self.assertIn("<p>test_first test_last</p>", html)