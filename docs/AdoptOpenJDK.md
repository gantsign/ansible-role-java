# Configuration for AdoptOpenJDK

The configuration for AdoptOpenJDK is quite different to that for Oracle JDK.
Since AdoptOpenJDK provides a REST API that provides information on the
available release, we use that rather keeping that information in the role.

With [curl](https://curl.haxx.se) and [jq](https://stedolan.github.io/jq) you
can view the available versions by running the following command:

```bash
for ((i = 8; i <= 11; i++)) do (curl --silent http \
  "https://api.adoptopenjdk.net/v2/info/releases/openjdk$i?openjdk_impl=hotspot" \
  | jq --raw-output '.[].release_name'); done
```

For example to install AdoptOpenJDK `8u172` you would use the following
configuration:

```yaml
- hosts: servers
  roles:
    - role: gantsign.java
      java_version: jdk8u172-b11
      # You need to specify java_vendor to use AdoptOpenJDK with Java < 11
      java_vendor: adoptopenjdk
```

## Offline Install

It's still possible to perform an offline install, but you need to specify a
bit more information (i.e. `java_redis_filename` and
`java_redis_sha256sum`). E.g. to perform an offline install of `jdk-11.0.2+9`:

```yaml
# Before performing the offline install, download
# `OpenJDK11U-jdk_x64_linux_hotspot_11.0.2_9.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: gantsign.java
      java_version: 'jdk-11.0.2+9'
      java_redis_filename: 'OpenJDK11U-jdk_x64_linux_hotspot_11.0.2_9.tar.gz'
      java_redis_sha256sum: 'd02089d834f7702ac1a9776d8d0d13ee174d0656cf036c6b68b9ffb71a6f610e'
```
