def test_get_activities(client):
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    # Expect at least the pre-seeded activities
    assert 'Chess Club' in data
    assert 'participants' in data['Chess Club']
    assert isinstance(data['Chess Club']['participants'], list)


def test_signup_and_duplicate_signup(client):
    activity = 'Chess Club'
    email = 'newstudent@mergington.edu'

    # Signup should succeed
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in client.get('/activities').json()[activity]['participants']

    # Duplicate signup should return 400
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_unregister(client):
    activity = 'Programming Class'
    # take an existing participant
    existing = client.get('/activities').json()[activity]['participants'][0]

    # Unregister should succeed
    resp = client.post(f"/activities/{activity}/unregister?email={existing}")
    assert resp.status_code == 200
    assert existing not in client.get('/activities').json()[activity]['participants']

    # Unregistering again should fail
    resp2 = client.post(f"/activities/{activity}/unregister?email={existing}")
    assert resp2.status_code == 400
