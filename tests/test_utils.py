from web_crawler.utils import get_md5


class TestUtils:

    def test_md5_hash(self):
        dummy_content = "test".encode("utf-8")
        res = get_md5(dummy_content)

        assert res == '098f6bcd4621d373cade4e832627b4f6'
