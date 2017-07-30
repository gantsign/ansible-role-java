import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('command', [
    'java',
    'javac'
])
def test_java_tools(Command, command):
    cmd = Command('. /etc/profile && ' + command + ' -version')
    assert cmd.rc == 0
    assert ' 1.8.0_' in cmd.stderr


@pytest.mark.parametrize('version_dir_pattern', [
    'jdk1\\.8\\.0_[0-9]+$'
])
def test_java_installed(Command, File, version_dir_pattern):

    java_home = Command.check_output('find %s | grep --color=never -E %s',
                                     '/opt/java/',
                                     version_dir_pattern)

    java_exe = File(java_home + '/bin/java')

    assert java_exe.exists
    assert java_exe.is_file
    assert java_exe.user == 'root'
    assert java_exe.group == 'root'
    assert oct(java_exe.mode) == '0755'


@pytest.mark.parametrize('fact_group_name', [
    'java'
])
def test_facts_installed(File, fact_group_name):
    fact_file = File('/etc/ansible/facts.d/' + fact_group_name + '.fact')

    assert fact_file.exists
    assert fact_file.is_file
    assert fact_file.user == 'root'
    assert fact_file.group == 'root'
    assert oct(fact_file.mode) == '0644'
