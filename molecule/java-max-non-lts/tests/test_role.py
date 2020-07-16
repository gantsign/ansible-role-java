import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_java(host):
    cmd = host.run('. /etc/profile && java -version')
    assert cmd.rc == 0
    m = re.search('(?:java|openjdk) version "([0-9]+)', cmd.stderr)
    assert m is not None
    java_version = m.group(1)
    assert '14' == java_version


def test_javac(host):
    cmd = host.run('. /etc/profile && javac -version')
    assert cmd.rc == 0
    m = re.search('javac ([0-9]+)', cmd.stdout)
    assert m is not None
    java_version = m.group(1)
    assert '14' == java_version


@pytest.mark.parametrize('version_dir_pattern', [
    'jdk-14(\\.[0-9]+\\.[0-9]+)?(\\+[0-9]+)?$'
])
def test_java_installed(host, version_dir_pattern):

    java_home = host.check_output('find %s | grep --color=never -E %s',
                                  '/opt/java/',
                                  version_dir_pattern)

    java_exe = host.file(java_home + '/bin/java')

    assert java_exe.exists
    assert java_exe.is_file
    assert java_exe.user == 'root'
    assert java_exe.group == 'root'
    assert oct(java_exe.mode) == '0755'


@pytest.mark.parametrize('fact_group_name', [
    'java'
])
def test_facts_installed(host, fact_group_name):
    fact_file = host.file('/etc/ansible/facts.d/' + fact_group_name + '.fact')

    assert fact_file.exists
    assert fact_file.is_file
    assert fact_file.user == 'root'
    assert fact_file.group == 'root'
    assert oct(fact_file.mode) == '0644'
