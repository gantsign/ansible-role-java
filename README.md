Ansible Role: Java
==================

[![Tests](https://github.com/gantsign/ansible-role-java/workflows/Tests/badge.svg)](https://github.com/gantsign/ansible-role-java/actions?query=workflow%3ATests)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.java-blue.svg)](https://galaxy.ansible.com/gantsign/java)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-java/master/LICENSE)

Role to install the Java JDK.

**Important:** since the 9.0.0 release of this role the version numbers used
have changed to use the semantic version from the AdoptOpenJDK v3 API. The
fields required for offline install have also changed as have the install
directories.

Requirements
------------

* Ansible >= 2.7

* Linux Distribution

    * Debian Family

        * Debian

            * Jessie (8)
            * Stretch (9)

        * Ubuntu

            * Xenial (16.04)
            * Bionic (18.04)

    * RedHat Family

        * CentOS

            * 7
            * 8

        * Fedora

            * 31

    * SUSE Family

        * openSUSE

            * 15.1

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# Specify '8', '9', '10', '11', '12', '13', '14' or '15' to get the latest patch
# version of that release.
java_version: '11.0.9.1+1'

# Base installation directory for any Java distribution
java_install_dir: '/opt/java'

# Directory to store files downloaded for Java installation on the remote box
java_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# Location Java installations packages can be found on the local box
# local packages will be uses in preference to downloading new packages.
java_local_archive_dir: '{{ playbook_dir }}/files'

# Wether to use installation packages in the local archive (if available)
java_use_local_archive: yes

# If this is the default installation, profile scripts will be written to set
# the JAVA_HOME environment variable and add the bin directory to the PATH
# environment variable.
java_is_default_installation: yes

# Name of the group of Ansible facts relating this Java installation.
#
# Override if you want use this role more than once to install multiple versions
# of Java.
#
# e.g. java_fact_group_name: java_8
# would change the Java home fact to:
# ansible_local.java_8.general.home
java_fact_group_name: java

# The SHA-256 for the JDK redistributable
java_redis_sha256sum:

# Mirror location for JDK download (e.g. https://example.com/provisioning/files)
java_redis_mirror:

# File name for the JDK redistributable installation file
java_redis_filename:

# OpenJDK Implementation (hotspot, openj9)
java_implementation: hotspot

# Timeout for JDK download response in seconds
java_download_timeout_seconds: 600

# The timeout for the AdoptOpenJDK API
java_api_timeout_seconds: 30
```

Example Playbooks
-----------------

By default this role will install the latest LTS JDK version provided by
AdoptOpenJDK that has been tested and is known to work with this role:

```yaml
- hosts: servers
  roles:
    - role: gantsign.java
```

You can install a specific version of the JDK by specifying the `java_version`.

```yaml
- hosts: servers
  roles:
    - role: gantsign.java
      java_version: '8.0.282+8'
```

**Note:** with [curl](https://curl.haxx.se) and
[jq](https://stedolan.github.io/jq) you can view the available versions by
running the following command:

```bash
for ((i = 8; i <= 15; i++)) do (curl --silent http \
  "https://api.adoptopenjdk.net/v3/assets/feature_releases/$i/ga?\
architecture=x64&heap_size=normal&image_type=jdk&jvm_impl=hotspot&\
os=linux&project=jdk&sort_order=DESC&vendor=adoptopenjdk" \
   | jq --raw-output '.[].version_data.semver'); done
```

You can install the multiple versions of the JDK by using this role more than
once:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java
      java_version: '8'
      java_is_default_installation: no
      java_fact_group_name: java_8

    - role: ansible-role-java
      java_version: '11'
      java_is_default_installation: yes
      java_fact_group_name: java
```

To perform an offline install, you need to specify a bit more information (i.e.
`java_major_version`, `java_release_name`, `java_redis_filename` and
`java_redis_sha256sum`). E.g. to perform an offline install of `11.0.9.1+1`:

```yaml
# Before performing the offline install, download
# `OpenJDK11U-jdk_x64_linux_hotspot_11.0.9.1_1.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: gantsign.java
      java_major_version: '11'
      java_version: '11.0.9.1+1'
      java_release_name: 'jdk-11.0.9.1+1'
      java_redis_filename: 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.9.1_1.tar.gz'
      java_redis_sha256sum: 'e388fd7f3f2503856d0b04fde6e151cbaa91a1df3bcebf1deddfc3729d677ca3'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.java.general.version`

    * e.g. `8u282`

* `ansible_local.java.general.home`

    * e.g. `/opt/java/jdk8u282`

Overriding `java_fact_group_name` will change the names of the facts e.g.:

```yaml
java_fact_group_name: java_8
```

Would change the name of the facts to:

* `ansible_local.java_8.general.version`
* `ansible_local.java_8.general.home`

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/gantsign).

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including python-pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

Because the above can be tricky to install, this project includes
[Molecule Wrapper](https://github.com/gantsign/molecule-wrapper). Molecule
Wrapper is a shell script that installs Molecule and it's dependencies (apart
from Linux) and then executes Molecule with the command you pass it.

To test this role using Molecule Wrapper run the following command from the
project root:

```bash
./moleculew test
```

Note: some of the dependencies need `sudo` permission to install.

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
