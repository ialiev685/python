async def test_post_conveniences(ac):
    convenience_new = await ac.post('/conveniences', json={'title': 'Wi-Fi'})
    assert convenience_new.status_code == 200
    assert convenience_new.json()['data']['title'] == 'Wi-Fi'


async def test_get_conveniences(ac):
    conveniences = await ac.get('/conveniences')
    assert conveniences.status_code == 200
    assert isinstance(conveniences.json(), list)
