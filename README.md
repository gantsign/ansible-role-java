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

* Ansible >= 2.8

* Linux Distribution

    * Debian Family

        * Debian

            * Stretch (9)
            * Buster (10)
            * Bullseye (11)

        * Ubuntu

            * Bionic (18.04)
            * Focal (20.04)

    * RedHat Family

        * Rocky Linux

            * 8

        * Fedora

            * 35

    * SUSE Family

        * openSUSE

            * 15.2

    * Note: other versions are likely to work but have not been tested.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
# Specify '8', '11', '16' or '17' to get the latest patch version of that
# release.
java_version: '11.0.14+9'

# The Java vendor
# Must be either 'adoptopenjdk' or 'adoptium'.
# Note: while the default is currently adoptopenjdk, this will change to
# adoptium at a later point and adoptopenjdk will be removed when the service is
# discontinued.
java_vendor: adoptopenjdk

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
# Note: support for openj9 is deprecated. Openj9 is not available from Eclipse
# Adoptium.
java_implementation: hotspot

# Timeout for JDK download response in seconds
java_download_timeout_seconds: 600

# The timeout for the AdoptOpenJDK/Adoptium API
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
      java_version: '8.0.322+6'
```

**Note:** with [curl](https://curl.haxx.se) and
[jq](https://stedolan.github.io/jq) you can view the available versions by
running the following commands:

**AdoptOpenJDK**

```bash
for i in 8 11 16 17; do (curl --silent http \
  "https://api.adoptopenjdk.net/v3/assets/feature_releases/$i/ga?\
architecture=x64&heap_size=normal&image_type=jdk&jvm_impl=hotspot&\
os=linux&project=jdk&sort_order=DESC&vendor=adoptopenjdk" \
   | jq --raw-output '.[].version_data.semver'); done
```

**Eclipse Adoptium**

```bash
for i in 8 11 16 17; do (curl --silent http \
  "https://api.adoptium.net/v3/assets/feature_releases/$i/ga?\
architecture=x64&heap_size=normal&image_type=jdk&jvm_impl=hotspot&\
os=linux&project=jdk&sort_order=DESC&vendor=adoptium" \
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
`java_redis_sha256sum`). E.g. to perform an offline install of `11.0.14+9`:

```yaml
# Before performing the offline install, download
# `OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: gantsign.java
      java_major_version: '11'
      java_version: '11.0.14+9'
      java_release_name: 'jdk-11.0.14+9'
      java_redis_filename: 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.14_9.tar.gz'
      java_redis_sha256sum: '1189bee178d11402a690edf3fbba0c9f2ada1d3a36ff78929d81935842ef24a9'
```

Role Facts
----------

This role exports the following Ansible facts for use by other roles:

* `ansible_local.java.general.version`

    * e.g. `8u312`

* `ansible_local.java.general.home`

    * e.g. `/opt/java/jdk8u312`

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
