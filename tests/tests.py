import requests
import pytest


def get_status():
    resp = requests.get("http://localhost:8080/api/status")
    assert resp.status_code == 200
    return resp.json()


def test_status(mpv_instance, snapshot):
    status = get_status()
    snapshot.assert_match(status)


@pytest.mark.parametrize(
    "endpoint,arg,key,value,invert_actual",
    [
        ("play", "", "pause", False, False),
        ("pause", "", "pause", True, False),
        ("toggle_pause", "", "pause", False, True),
        ("fullscreen", "", "fullscreen", True, True),
        ("loop_file", "no", "loop-file", False, False),
        ("loop_file", "inf", "loop-file", True, False),
        ("loop_playlist", "no", "loop-playlist", False, False),
        (
            "loop_playlist",
            "inf",
            "loop-playlist",
            "inf",
            False,
        ),  # TODO: why "inf" for playlist, but True for files?
        ("add_volume", "10", "volume", "10.000000", False),
        ("set_volume", "100", "volume", "100.000000", False),
        ("add_sub_delay", "0.1", "sub-delay", 100, False),
        ("set_sub_delay", "1", "sub-delay", 1000, False),
        ("add_audio_delay", "0.1", "audio-delay", 100, False),
        ("set_audio_delay", "1", "audio-delay", 1000, False),
    ],
)
def test_post(mpv_instance, endpoint, arg, key, value, invert_actual):
    if invert_actual:
        status = get_status()
        value = not status[key]

    resp = requests.post(f"http://localhost:8080/api/{endpoint}/{arg}")
    assert resp.status_code == 200

    resp = requests.get("http://localhost:8080/api/status")
    assert resp.status_code == 200
    status = resp.json()
    assert status[key] == value
