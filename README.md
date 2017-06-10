Ansible Role: Java
==================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-java.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-java)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.java-blue.svg)](https://galaxy.ansible.com/gantsign/java)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-java/master/LICENSE)

Role to install the [Oracle Java JDK](http://www.oracle.com/technetwork/java/index.html).

Requirements
------------

* Ansible >= 2.0

* Linux Distribution

    * Debian Family

        * Debian

            * Wheezy (7)
            * Jessie (8)

        * Ubuntu

            * Trusty (14.04)
            * Wily (15.10)
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
java_version: '8u131'

# Base installation directory for any Java distribution
java_install_dir: '/opt/java'

# The root folder of this Java installation
java_home: '{{ java_install_dir }}/jdk{{ java_version }}'

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

# Timeout for JDK download response in seconds
java_jce_download_timeout_seconds: 30
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

* 8u131

**Archived versions** As of 23 May 2017 all the archived Java versions (i.e.
everything but the latest release) have been moved from the Oracle public
download area to behind the Oracle Technology Network login.

This Ansible role is no longer able to download archived versions of Java from
Oracle; to workaround this limitation you should manually download the
`jdk-VERSION-linux-x64.tar.gz` file from Oracle and put it into
`java_local_archive_dir`.

* 8u121
* 8u112
* 8u111
* 8u102
* 8u101
* 7u80
* 7u79

Advanced Configuration
----------------------

The following role variables are dependent on the Java version; to use a
Java version **not pre-configured by this role** you must configure the
variables below.

### Minor Version Configuration

The below has to be configured for every minor release of Java.

```yaml
# SHA256 sum for the redistributable JDK package (i.e. jdk-{{ java_version }}-linux-x64.tar.gz)
java_redis_sha256sum: '7cfbe0bc0391a4abe60b3e9eb2a541d2315b99b9cb3a24980e618a89229e04b7'

# The build number for this JDK version
java_version_build: 14

# ID in JDK download URL (introduced in 8u121)
java_jdk_download_id: ''
```

### Major Version Configuration

The below only has to be configured for a new major release of Java.

**Warning:** this role is incompatible with Java 6 and earlier due to the
different way the JDK was packaged for those releases.

```yaml
# SHA256 sum for the redistributable JCE Policy Files (i.e. jce_policy-8.zip)
java_jce_redis_sha256sum: 'f3020a3922efd6626c2fff45695d527f34a8020e938a49292561f18ad1320b59'

# Directory on remote mirror where JCE redistributable can be found
java_jce_redis_mirror: '{{ java_mirror_base }}/jce/8'

# The JCE redistributable file name
java_jce_redis_filename: 'jce_policy-8.zip'

# The root folder name inside the JCE redistributable
java_jce_redis_folder: 'UnlimitedJCEPolicyJDK8'
```

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
      java_version: '8u121'
```

You can install the multiple versions of the Oracle JDK by using this role more
than once:

```yaml
- hosts: servers
  roles:
    - role: ansible-role-java
      java_version: '8u121'
      java_is_default_installation: yes
      java_fact_group_name: java

    - role: ansible-role-java
      java_version: '7u80'
      java_is_default_installation: no
      java_fact_group_name: java_7
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
