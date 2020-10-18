# Follow these steps to add new data disk:


## 1) Stop processes that would be using the mounts:
```
systemctl stop docker
systemctl stop kodi
```


## 2) Check docker has stopped and is unmounted

Run the mount command to list the currently mounted partitions.
```
mount
```

This command should show an output that does not have these lines:
```
overlay on /storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/d02b90f626cd91224db39249bfb2a5b4d6ea64424899f13c548eee4054c2603e/merged type overlay (rw,relatime,lowerdir=/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/U7FGNL4SYZQ72D3IWFZOBKFL2H:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/MZE44CVZRD3W6A6F4CTKFC4HYF:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/FKMLS62G4LFMCUQIEI2U6UMI4G:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/NFESBAB5WLRUS2MKXCWRAPIHBI:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/5YIUMABVV5NXUKHZQZOORCCYYQ:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/OWEBHA7SVT4FM2DXFGXFNO7PUK:/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/l/LCSGLC43PK4LXENDUQNJ2IPQJJ,upperdir=/storage/.kodi/userdata/addon_data/service.system.docker/docker/overlay2/d02b90f626cd91224db39249bfb2a)
nsfs on /run/docker/netns/default type nsfs (rw)
shm on /storage/.kodi/userdata/addon_data/service.system.docker/docker/containers/927d6d5784e65797ca61f5816cb6fddf65de6e31c35e22a8854154b7a599fbf1/mounts/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=65536k)
```

If you see the above lines, then the docker daemon did not stop with `systemctl stop docker` go back to step one.

If you keep seeing this issue, reboot and start again...


## 3) Unmount the current data disks

```
umount /var/media/*

```

Run the mount command again to list the currently mounted partitions.
```
mount
```

This command should show an output that does not have any lines like this one mounting something to `/var/media/`:
```
/dev/sdaX on /var/media/XXXXXXXXX type ext4 (rw,nosuid,nodev,noexec,noatime)
```

If you see the above lines printed, then go back to step three and try the unmount process again..

If you keep seeing this issue, reboot and start again...


## 4) Partition the new disk

At this point it is important to know what disk is required to be partitioned. If you have already partitioned it, then move onto step #5 below.

Follow the below executed steps by running the command `parted /dev/sdX` where the *X* in the *sdX* is the disk number that you have identified to partition.

**Warning!** This will blow away all data on this disk. Make sure you have selected the correct disk before running the parted command!

```
Shuttle:~ # parted /dev/sdX                                               
GNU Parted 3.2
Using /dev/sdX
Welcome to GNU Parted! Type 'help' to view a list of commands.

------------------------------------------------------------------------------------------

(parted) print                                                            
print
Model: ATA WDC WD10EADS-00L (scsi)
Disk /dev/sdX: 1000GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start  End  Size  File system  Name  Flags

------------------------------------------------------------------------------------------

(parted) mklabel                                                          
mklabel
New disk label type? gpt                                                  
gpt
Warning: The existing disk label on /dev/sdX will be destroyed and all data on
this disk will be lost. Do you want to continue?
Yes/No? yes                                                               
yes

------------------------------------------------------------------------------------------

(parted) mkpart                                                           
mkpart
Partition name?  []? disk2                                                
disk2
File system type?  [ext2]? ext4                                           
ext4
Start? 0%                                                                 
0%
End? 100%                                                                 
100%

------------------------------------------------------------------------------------------

(parted) print                                                            
print
Model: ATA WDC WD10EADS-00L (scsi)
Disk /dev/sdX: 1000GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name   Flags
 1      1049kB  1000GB  1000GB  ext4         disk2

------------------------------------------------------------------------------------------

(parted) quit                                                             
quit
Information: You may need to update /etc/fstab.


```

Once you have created the partition, format it with the `mkfs.ext4 /dev/sdX1` command. You should see something like the below example output.
```
Shuttle:~ # mkfs.ext4 /dev/sdX1
mke2fs 1.45.3 (14-Jul-2019)
Creating filesystem with 244190208 4k blocks and 61054976 inodes
Filesystem UUID: 2c8efe92-c0c6-4aee-8f4f-64f29c002111
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
	102400000, 214990848

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (262144 blocks): done
Writing superblocks and filesystem accounting information: done     

```


