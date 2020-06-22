# UniFi Protect for Docker (ARM)

This build provides UniFi Protect for ARM as a self-hosted docker image.
Normally it is only available for the Cloud Key Gen2.

This image was self-created, but then cloned an [existing image](https://github.com/iamjamestl/docker-unifi-protect)
even though they are for different purposes and slightly different goals.

While many other images exist using the 1.12.5 x86_64 leak, that deb
has since been removed, meaning people now modify the existing docker images
or pull the certain files from an existing Cloud Key. The point of this
is simply to self host and with the availability of RPi 4 or newer, this
is easy.

**WARNING**: This is a wholly unsupported build and it may stop working at any
time depending on where Ubiquiti takes things. Use at your own risk.

## Usage

### Host Configuration

This image should work out-of-the-box on a Linux ARM Docker host (like an RPi).

### Storage

To ensure your UniFi Protect configs and recordings persist across restarts,
prepare a Docker volume to map into the container.  Do not simply map a host
directory into the container!  Docker won't initialize it properly and UniFi
Protect almost certainly won't have permission to write to it.

```
docker volume create unifi-protect
docker volume create unifi-protect-postgresql
```

On a typical Docker installation, you will have access to this volume from the
host at `/var/lib/docker/volumes/unifi-protect/_data`.

Optionally, if you want to store the bulk video data on a larger device, create
the volume like:

```
docker volume create -o type=none -o o=bind -o device=/path/to/some/empty/dir unifi-protect
```

Note: if using a network store for data, make sure to have the correct permissions
for the folder, otherwise the volume will fail to mount or the image won't
be able to read the folder contents. If you want to map the postgres library,
it requires the folders have the proper access control (which eliminates SMB, NFS, etc.)

### Execution

Finally, run the container as follows:

```
docker run \
  --name unifi-protect \
  --net host \
  -v unifi-protect:/srv/unifi-protect \
  -v unifi-protect-postgresql:/var/lib/postgresql \
  --tmpfs /tmp \
  ??/unifi-protect
```

NOTE: this hasn't been published anywhere yet, so you will need to build the image
yourself at this point.

After a minute or so for the service to start, visit
`http://<ip-of-the-container>:7443/`.

### Tips

The container must have outbound access to the internet.  UniFi Protect employs
STUN to poke a holes in your NAT.  Firewalls like pfSense can break STUN by
using different UDP ports on either side of the NAT.  Create a static port rule
for the UniFi Protect container to work around this.  Instructions for pfSense
can be found at
https://docs.netgate.com/pfsense/en/latest/nat/static-port.html.

The Cloud Key2 that this is typically installed on is running the following:
- APQ8053 8 Core with 3 GB RAM
- 1TB HDD
- 32GB OS/firmware eMMC
so if you want to buy or rent ARM-based software, know that's what it's being
developed for.

### Versions
- 1.12.5 - In progress (not all features functioning right now, other components, folder mappings, etc.)
- 1.13.1 - Looking for .deb file to make multiple releases instead of large jumps
- 1.13.2 - .deb in hand, will need to look into more
- 1.13.3 - .deb in hand, but online and checking the contents reveal that Ubiquiti now forces ubnt-tool to be installed otherwise it forces closes
    - Previous versions simply looked for ubnt-tool and went "oh, this is a software install"
    - This version says "if we can't find ubnt-tool, and this isn't the dev mode for NodeJS, we're force-closing"
    - It indicates that Ubiqiti is semi-actively working to prevent self-installs
    - It also presents a slight worry because there is already a "if a failure happens, contact Ubiquiti with a IP and mac address" and the force-close is "unregistered device" which could mean that in the future, if you contact them with an "unregistered" device, the weblinks may not work.