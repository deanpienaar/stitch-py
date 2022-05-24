from stitch.client import Stitch


# TODO: Write real tests
class TestStitch:
    def setup(self):
        self.client = Stitch(
            url='https://example.com',
            cert_path='./cert.pem',
            client_id='test-1234',
        )

    def test_has_attributes(self):
        assert self.client.client_id is not None
        assert self.client.cert_path is not None
        assert self.client.url is not None
