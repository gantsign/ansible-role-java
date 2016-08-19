import pytest

@pytest.mark.parametrize('command', [
    ('java'),
    ('javac')
])
def test_java_tools(Command, command):
    cmd = Command('. /etc/profile && ' + command + ' -version')
    assert cmd.rc == 0
