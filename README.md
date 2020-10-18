# MergerFS

This addon is for pooling disks and managing all docker containers with yacht.

It will mount all disks mounted in `/var/media/` into a merged disk pool at `/storage/pool`.

This addon is also able to handle Docker mounts. It will ensure the mergerFS is mounted prior to Docker daemon starting.


## Manual configuration processes:

### * Adding a new disk
It is recommended to use a Linux filesystem for the mounts. Use the `parted` tool to manually setup new disks.
Take a look at the [partitioning guide](docs/NEW_DISK.md) (requires SSH).

