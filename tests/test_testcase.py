from .testcase import NinjaTestCase


class TestNinjaTestCase(NinjaTestCase):
    def test_get_public(self):
        res = self.client.get("/")
        assert res.status_code == 200

    def test_get_anonymous(self):
        res = self.client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res.status_code == 302

    def test_get_redirected_to_login(self):
        res_redirect = self.user_client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res_redirect.status_code == 302
        res = self.user_client.get(f"{self.root_path}login")
        assert res.status_code == 200

    def test_get_admin_authentificated(self):
        res = self.admin_client.get(f"{self.root_path}{self.docs_url[1:]}")
        assert res.status_code == 200
