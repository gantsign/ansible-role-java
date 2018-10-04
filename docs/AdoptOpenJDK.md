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
`java_redis_sha256sum`). E.g. to perform an offline install of `jdk-11+28`:

```yaml
# Before performing the offline install, download
# `OpenJDK11-jdk_x64_linux_hotspot_11_28.tar.gz` to
# `{{ playbook_dir }}/files/` on the local machine.
- hosts: servers
  roles:
    - role: gantsign.java
      java_version: 'jdk-11+28'
      java_redis_filename: 'OpenJDK11-jdk_x64_linux_hotspot_11_28.tar.gz'
      java_redis_sha256sum: 'e1e18fc9ce2917473da3e0acb5a771bc651f600c0195a3cb40ef6f22f21660af'
```
