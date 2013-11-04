class TestMain():

    def test_url(self):
        lista = ['http', 1, 2, 3]
        assert 'http' in lista

    def test_url2(self):
        lista = ['https', 2]
        assert 'https' in lista
