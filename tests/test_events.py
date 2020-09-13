

def test_list_events(client, app):
    resp = client.get("/api/v1/events")
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert resp.json['data']

