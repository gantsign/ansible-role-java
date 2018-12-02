Ansible Role: Java
==================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-java.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-java)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.java-blue.svg)](https://galaxy.ansible.com/gantsign/java)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-java/master/LICENSE)

Role to install the Java JDK.

This roles supports the following JDK vendors:

* [AdoptOpenJDK](https://adoptopenjdk.net)
    * For Java >= 8 (default for Java >= 11)
* [Oracle JDK](http://www.oracle.com/technetwork/java/index.html)
    * For Java < 11 (default for Java < 11)

**Deprecation notice:** support for the Oracle JDK will be dropped once
Oracle ends public support for the Oracle JDK (in January 2019).

Requirements
------------

* Ansible >= 2.5

* Linux Distribution

    * Debian Family

        * Debian

            * Jessie (8)
            * Stretch (9)

        * Ubuntu

            * Trusty (14.04)
            * Xenial (16.04)
            * Bionic (18.04)

    * RedHat Family

        * CentOS

            * 6
            * 7

        * Fedora

            * 28

    * SUSE Family

        * openSUSE

            * 15.0

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# Specify '8', '9', '10' or '11' to get the latest patch version of that
# release.
java_version: 'jdk-11.0.1+13'

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

# The JDK vendor (oracle/adoptopenjdk)
# Default is oracle for Java < 11 and adoptopenjdk for Java >= 11
java_vendor: default

# The SHA-256 for the JDK redistributable
java_redis_sha256sum:


### The following only apply to Oracle Java versions ###

# Timeout for JDK download response in seconds
java_jdk_download_timeout_seconds: 600

# Base location for Java mirror
java_mirror_base: 'http://download.oracle.com/otn-pub/java'

# Mirror location for JDK download (e.g. https://example.com/provisioning/files)
java_jdk_redis_mirror: '{{ java_mirror_base }}/{{ java_otn_jdk_path }}'


### The following only apply to Oracle Java versions prior to 9 ###

# Timeout for JDK download response in seconds
java_jce_download_timeout_seconds: 30

# Mirror location for JCE download (e.g. https://example.com/provisioning/files)
java_jce_redis_mirror: '{{ java_mirror_base }}/{{ java_otn_jce_path }}'


### The following only apply to AdoptOpenJDK ###

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

JDK vendor specific configuration
---------------------------------

You can view the JDK vendor specific configuration by clicking on the following
links:

* [AdoptOpenJDK](https://github.com/gantsign/ansible-role-java/blob/master/docs/AdoptOpenJDK.md)
* [Oracle JDK](https://github.com/gantsign/ansible-role-java/blob/master/docs/OracleJDK.md)

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
      java_version: '8u192'
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

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.java.general.version`

    * e.g. `1.8.0_102`

* `ansible_local.java.general.home`

    * e.g. `/opt/java/jdk1.8.0_102`

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
