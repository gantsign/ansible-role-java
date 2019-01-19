# Configuration for the Oracle JDK

## Oracle Binary Code License Agreement

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

## Supported Java Versions

The following versions of Java are supported without any additional
configuration (for other versions follow the Advanced Configuration
instructions):

**Current releases**

* 8u201

**Caution:** the current versions will be moved to Oracle's archives when a
newer version is released; if you don't want your provisioning to break when
that happens, you should follow the advice for archived versions below.

**Archived versions**

* 10.0.2
* 10.0.1
* 10.0.0
* 9.0.4
* 9.0.1
* 9.0.0
* 8u192
* 8u191
* 8u181
* 8u172
* 8u171
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

## Advanced Configuration

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
