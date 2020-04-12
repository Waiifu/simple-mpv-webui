import pytest
import subprocess
import time


@pytest.fixture()
def mpv_instance():
    process = subprocess.Popen(
        ["mpv --config-dir=./environment/ ./environment/test_media/*\ -\ dummy.mp3"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(0.4)  # wait for MPV to be ready
    yield process
    process.terminate()
    # out, err = process.communicate()
    # if out:
    #     print("MPV stdout:")
    #     print(str(out.decode()))
    # if err:
    #     print("MPV stderr:")
    #     print(str(err.decode()))
