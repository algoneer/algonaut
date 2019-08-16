from unittest import TestCase

from algonaut.utils.email import jinja_email, send_email


class TestJinjaEMails(TestCase):
    def test_basic_mail(self):
        tests = {"base": {}}
        for key, context in tests.items():
            result = jinja_email(
                "email/{}.multipart".format(key), context, version="v1", language="en"
            )
            assert hasattr(result, "html") and result.html
            assert hasattr(result, "text") and result.text
            # this is just a rudimentary check to make sure the codes are in the mail
            for ck, cv in context.items():
                assert result.html.find(cv) != -1
                assert result.text.find(cv) != -1
