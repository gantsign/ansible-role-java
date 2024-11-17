Ansible Role: Java
==================

[![Tests](https://github.com/gantsign/ansible-role-java/workflows/Tests/badge.svg)](https://github.com/gantsign/ansible-role-java/actions?query=workflow%3ATests)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.java-blue.svg)](https://galaxy.ansible.com/gantsign/java)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-java/master/LICENSE)

Role to install the Java JDK.

Requirements
------------

* Ansible Core >= 2.12

* Linux Distribution

    * Debian Family

        * Debian

            * Buster (10)
            * Bullseye (11)

        * Ubuntu

            * Focal (20.04)
            * Jammy (22.04)

    * RedHat Family

        * Rocky Linux

            * 8

        * Fedora

            * 35

    * SUSE Family

        * openSUSE

            * 15.4

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# Specify '8', '11', '17' or '21' to get the latest patch version of that
# release.
java_version: '21.0.2+13'

# Base installation directory for any Java distribution
java_install_dir: '/opt/java'

# Directory to store files downloaded for Java installation on the remote box
java_download_dir: "{{ x_ansible_download_dir | default(ansible_env.HOME + '/.ansible/tmp/downloads') }}"

# Location Java installations packages can be found on the local box
# local packages will be uses in preference to downloading new packages.
java_local_archive_dir: '{{ playbook_dir }}/files'

# Wether to use installation packages in the local archive (if available)
java_use_local_archive: true

# If this is the default installation, profile scripts will be written to set
# the JAVA_HOME environment variable and add the bin directory to the PATH
# environment variable.
java_is_default_installation: true

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

# Timeout for JDK download response in seconds
java_download_timeout_seconds: 600

# The timeout for the Adoptium API
java_api_timeout_seconds: 30
```

Example Playbooks
-----------------

By default this role will install the latest LTS JDK version provided by
Adoptium that has been tested and is known to work with this role:

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
      java_version: '8.0.402+6'
```

**Note:** with [curl](https://curl.haxx.se) and
[jq](https://stedolan.github.io/jq) you can view the available versions by
running the following command:

```bash
for i in 21 17 11 8; do (curl --silent http \
  "https://api.adoptium.net/v3/info/release_names?version=%5B$i,$(($i + 1)))\
&release_type=ga" | jq --raw-output '.releases[]' | sed -E 's/^jdk\-?//'); done
```

You can install the multiple versions of the JDK by using this role more than
once:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java
      java_version: '8'
      java_is_default_installation: false
      java_fact_group_name: java_8

    - role: ansible-role-java
      java_version: '11'
      java_is_default_installation: true
      java_fact_group_name: java
```

To perform an offline install, you need to specify a bit more information (i.e.
`java_major_version`, `java_release_name`, `java_redis_filename` and
`java_redis_sha256sum`). E.g. to perform an offline install of `11.0.22+7`:

```yaml
# Before performing the offline install, download
# `OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: gantsign.java
      java_major_version: '11'
      java_version: '11.0.22+7'
      java_release_name: 'jdk-11.0.22+7'
      java_redis_filename: 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz'
      java_redis_sha256sum: '25cf602cac350ef36067560a4e8042919f3be973d419eac4d839e2e0000b2cc8'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.java.general.version`

    * e.g. `8u402`

* `ansible_local.java.general.home`

    * e.g. `/opt/java/jdk8u402`

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
[Ansible Galaxy](https://galaxy.ansible.com/ui/standalone/namespaces/2463/).

Development & Testing
---------------------

This project uses the following tooling:
* [Molecule](http://molecule.readthedocs.io/) for orchestrating test scenarios
* [Testinfra](http://testinfra.readthedocs.io/) for testing the changes on the
  remote
* [pytest](http://docs.pytest.org/) the testing framework
* [Tox](https://tox.wiki/en/latest/) manages Python virtual
  environments for linting and testing
* [pip-tools](https://github.com/jazzband/pip-tools) for managing dependencies

A Visual Studio Code
[Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) is
provided for developing and testing this role.

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
