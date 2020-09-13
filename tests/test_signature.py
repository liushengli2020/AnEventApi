from eventapp.services.signature_util import generate_signature
def test_quit_event_failed(client, app):
    assert generate_signature('123','abc') == '8f16771f9f8851b26f4d460fa17de93e2711c7e51337cb8a608a0f81e1c1b6ae'