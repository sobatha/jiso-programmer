"""１つのテストメソッドでは１つの項目のみ確認する
https://rinatz.github.io/python-book/ch08-02-pytest/
"""


def validate(text):
    return 0 < len(text) <= 100


import pytest


class TestValidate:
    @pytest.mark.parametrize("text", ["a", "a" * 50, "a" * 100])
    def test_valid(self, text):
        # 検証が正しい場合
        assert validate(text)

    @pytest.mark.parametrize("text", ["", "a" * 101])
    def test_invalid(self, text):
        assert not validate(text)


"""テストケースは準備、実行、検証に分割する
"""


class TestSignupAPIView:
    @pytest.fixture
    def target_api(self):
        return "/api/signup"

    def test_do_signup(self, target_api, django_app):
        # 　準備　---
        from account.models import User

        params = {
            "email": "signup@example.com",
            "name": "yamadataro",
            "password": "xxxxxxxx",
        }

        # 実行 ---
        res = django_app.post_json(target_api, params=params)

        # 検証 ---
        user = User.objects.all()[0]
        expected = {
            "status_code": 201,
            "user_email": "signup@example.com",
        }
        actual = {
            "status_code": res.status_code,
            "user_email": user.email,
        }
        assert expected == actual
