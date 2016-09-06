import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('command', [
    'java',
    'javac'
])
def test_java_tools(Command, command):
    cmd = Command('. /etc/profile && ' + command + ' -version')
    assert cmd.rc == 0
