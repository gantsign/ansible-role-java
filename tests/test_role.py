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
    assert ' 1.8.0_' in cmd.stderr


def test_java_installed(Command, File):

    java_home = Command.check_output('find %s | grep --color=never -E %s',
                                     '/opt/java/',
                                     'jdk1\\.8\\.0_[0-9]+$')

    java_exe = File(java_home + '/bin/java')

    assert java_exe.exists
    assert java_exe.is_file
    assert java_exe.user == 'root'
    assert java_exe.group == 'root'
    assert oct(java_exe.mode) == '0755'


def test_facts_installed(File):
    fact_file = File('/etc/ansible/facts.d/java.fact')

    assert fact_file.exists
    assert fact_file.is_file
    assert fact_file.user == 'root'
    assert fact_file.group == 'root'
    assert oct(fact_file.mode) == '0644'
