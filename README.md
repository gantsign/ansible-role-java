Ansible Role: Java
==================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-java.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-java)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.java-blue.svg)](https://galaxy.ansible.com/gantsign/java)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-java/master/LICENSE)

Role to install the [Oracle Java JDK](http://www.oracle.com/technetwork/java/index.html).

Requirements
------------

* Ansible >= 2.2

* Linux Distribution

    * Debian Family

        * Debian

            * Wheezy (7)
            * Jessie (8)

        * Ubuntu

            * Trusty (14.04)
            * Xenial (16.04)

    * RedHat Family

        * CentOS

            * 6
            * 7

        * Fedora

            * 25

    * SUSE Family

        * OpenSUSE

            * 42.2

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# * Specify '8', '9' or '10' to get the latest patch version of that release
#   (from the supported versions below)
java_version: '8u171'

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

# Timeout for JDK download response in seconds
java_jdk_download_timeout_seconds: 600

# Base location for Java mirror
java_mirror_base: 'http://download.oracle.com/otn-pub/java'

# Mirror location for JDK download (e.g. https://example.com/provisioning/files)
java_jdk_redis_mirror: '{{ java_mirror_base }}/{{ java_otn_jdk_path }}'


### The following only apply to Java versions prior to 9 ###

# Timeout for JDK download response in seconds
java_jce_download_timeout_seconds: 30

# Mirror location for JCE download (e.g. https://example.com/provisioning/files)
java_jce_redis_mirror: '{{ java_mirror_base }}/{{ java_otn_jce_path }}'
```

### Oracle Binary Code License Agreement

To use this role you must accept the "Oracle Binary Code License Agreement
for the Java SE Platform Products and JavaFX"; you can do this by specifying
the following role variable:

```yaml
java_license_declaration: 'I accept the "Oracle Binary Code License Agreement for the Java SE Platform Products and JavaFX" under the terms at http://www.oracle.com/technetwork/java/javase/terms/license/index.html'
```

If you don't want to embed the declaration in your playbook it can be passed
by adding the following argument when running `ansible-playbook`:

```
--extra-vars '{"java_license_declaration": "I accept the \"Oracle Binary Code License Agreement for the Java SE Platform Products and JavaFX\" under the terms at http://www.oracle.com/technetwork/java/javase/terms/license/index.html"}'
```

### Supported Java Versions

The following versions of Java are supported without any additional
configuration (for other versions follow the Advanced Configuration
instructions):

**Current releases**

* 10.0.1
* 8u171
* 8u172

**Caution:** the current versions will be moved to Oracle's archives when a
newer version is released; if you don't want your provisioning to break when
that happens, you should follow the advice for archived versions below.

**Archived versions**

* 10.0.0
* 9.0.4
* 9.0.1
* 9.0.0
* 8u161
* 8u151
* 8u144
* 8u141
* 8u131
* 8u121
* 8u112
* 8u111
* 8u102
* 8u101
* 7u80
* 7u79

As of 23 May 2017 all the archived Java versions (i.e. everything but the latest
release) have been moved from the Oracle public download area to behind the
Oracle Technology Network login.

This Ansible role is no longer able to download archived versions of Java from
Oracle; to workaround this limitation you have 3 options:

1) Specify the `java_jdk_redis_mirror` (and optionally the
`java_jce_redis_mirror`) to point to a private mirror containing the
installation packages.

2) Copy the installation packages to the location specified by
`java_local_archive_dir` on the local machine before running this role.

3) Copy/restore the installation packages to the location specified by
`java_download_dir` on the remote machine before running this role.

If manually downloading the JDK, make sure you download the file matching
`jdk-VERSION-linux-x64.tar.gz`, other variants of the JDK/JRE will not work with
this role.

Advanced Configuration
----------------------

The following role variables are dependent on the Java version; to use a
Java version **not pre-configured by this role** you must configure the
variables below.

### Minor Version Configuration

The below has to be configured for every minor release of Java.

```yaml
# SHA256 sum for the redistributable JDK package (i.e. jdk-{{ java_full_version }}-linux-x64.tar.gz)
java_redis_sha256sum: '7cfbe0bc0391a4abe60b3e9eb2a541d2315b99b9cb3a24980e618a89229e04b7'

# The build number for this JDK version
java_version_build: 14

# ID in JDK download URL (introduced in 8u121)
java_jdk_download_id: ''
```

### Major Version Configuration

This role is incompatible with Java 6 and earlier due to the different way the
JDK was packaged for those releases.

Example Playbooks
-----------------

By default this role will install the latest version of the Oracle JDK supported
by this role:

```yaml
- hosts: servers
  roles:
    - role: gantsign.java
```

You can install a specific version of the Oracle JDK by specifying the
`java_version` (note: if the version is not currently supported by this role
then additional configuration will be required - see
[Advanced Configuration](#advanced-configuration)):

```yaml
- hosts: servers
  roles:
    - role: gantsign.java
      java_version: '8u171'
```

You can install the multiple versions of the Oracle JDK by using this role more
than once:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java
      java_version: '8'
      java_is_default_installation: yes
      java_fact_group_name: java

    - role: ansible-role-java
      java_version: '10'
      java_is_default_installation: no
      java_fact_group_name: java_10
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

To run the role (i.e. the `tests/test.yml` playbook), and test the results
(`tests/test_role.py`), execute the following command from the project root
(i.e. the directory with `molecule.yml` in it):

```bash
molecule test
```

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
