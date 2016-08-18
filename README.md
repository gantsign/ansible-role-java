Ansible Role: Java
==================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-java.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-java)

Role to install the [Oracle Java JDK](http://www.oracle.com/technetwork/java/index.html).

Requirements
------------

* Ubuntu
* Ansible >= 2.0

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Java version number
java_version: '8u102'

# Base installation directory for any Java distribution
java_install_dir: /opt/java

# The root folder of this Java installation
java_home: "{{ java_install_dir }}/jdk{{ java_version }}"

# Path for Ansible to store downloaded files
local_ansible_data_path: '/tmp/ansible/data'

# SHA256 sum for the redistributable JDK package
java_redis_sha256sum: 7cfbe0bc0391a4abe60b3e9eb2a541d2315b99b9cb3a24980e618a89229e04b7

# The build number for this JDK version
java_version_build: 14

# SHA256 sum for the redistributable JCE Policy Files
java_jce_redis_sha256sum: f3020a3922efd6626c2fff45695d527f34a8020e938a49292561f18ad1320b59

# Directory on remote mirror where JCE redistributable can be found
java_jce_redis_mirror: "{{ java_mirror_base }}/jce/8"

# The JCE redistributable file name
java_jce_redis_filename: jce_policy-8.zip

# The root folder name inside the JCE redistributable 
java_jce_redis_folder: UnlimitedJCEPolicyJDK8
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
     - { role: gantsign.java }
```

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
