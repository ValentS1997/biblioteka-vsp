# Шпаргалка: storage stack, LVM, RAID, filesystems, ZFS и Btrfs

## 1. Storage stack

~~~text
physical media
→ interface/controller
→ kernel block device
→ partition table
→ LVM / RAID / pool
→ filesystem
→ mount point
→ application data
→ backup
~~~

Every lower-layer mistake propagates upward.

## 2. Rule zero: identify the disk

Linux:

~~~bash
lsblk
lsblk -o +MODEL,SERIAL
~~~

FreeBSD:

~~~bash
geom disk list
~~~

Physical-host detail:

~~~bash
hdparm -I <device>
camcontrol devlist
~~~

Never partition, format or erase until model/serial/size match the intended device.

## 3. Stable identity

Avoid persistent references to transient names such as /dev/sdX.

Prefer source-supported stable identities:
- filesystem LABEL;
- filesystem UUID;
- GPT partition label;
- PARTUUID/PARTLABEL;
- /dev/disk/by-* links.

For fstab, labels/UUID are preferable to mutable device names.

## 4. New Linux disk

~~~text
lsblk + model/serial
→ fdisk: GPT + partition
→ mkfs -t ext4 -L label
→ mkdir mountpoint
→ mount LABEL=label mountpoint
→ verify mount
→ add stable fstab entry
~~~

## 5. New FreeBSD disk

~~~text
geom disk list
→ gpart create -s GPT
→ gpart add ... freebsd-ufs
→ newfs -L label
→ mount
→ fstab
~~~

## 6. Destructive boundary

High-risk operations:
- fdisk write;
- gpart create/modify;
- mkfs/newfs;
- secure erase;
- RAID/pool creation;
- zpool destroy/zfs destroy.

For these, rollback may not exist.

Secure erase from the chapter:

~~~bash
hdparm --user-master u --security-set-pass ...
hdparm --user-master u --security-erase ...
camcontrol security ...
~~~

Effect: data destruction.

## 7. SMART

smartmontools:
- smartd = continuous monitoring;
- smartctl = interactive/scripted queries.

Interpret SMART as evidence/trend, not certainty.

The chapter highlights several non-zero error/reallocation-related attributes as warning signals.

## 8. GPT vs MBR

MBR:
- historical;
- limited;
- avoid unless compatibility requires it.

GPT:
- modern;
- GUID-based partition types;
- many partitions;
- protective MBR.

Use tools that actually support GPT.

## 9. LVM2 model

~~~text
physical volume (PV)
→ volume group (VG)
→ logical volume (LV)
→ filesystem
~~~

Core names:
- pvcreate / pvdisplay;
- vgcreate / vgdisplay / vgextend;
- lvcreate / lvdisplay / lvresize.

## 10. LVM example

~~~bash
pvcreate /dev/partition
vgcreate DEMO /dev/partition
vgdisplay DEMO
lvcreate -L 100G -n web DEMO
mkfs /dev/DEMO/web
mount /dev/DEMO/web /mnt/web
~~~

Verification:
- VG free extents;
- LV state;
- filesystem mounted.

## 11. LVM snapshots

~~~bash
lvcreate -L <size> -s -n <snap> <VG>/<LV>
lvdisplay
~~~

Risk:
- snapshot has fixed allocated space;
- if that space is exhausted, snapshot becomes unusable.

Use snapshots as short-lived backup sources unless sized appropriately.

## 12. Resize ordering

Grow:

~~~text
verify VG free space
→ grow LV
→ grow filesystem
→ mount/df verification
~~~

Shrink:

~~~text
shrink filesystem first
→ shrink LV second
~~~

Do not reverse the order.

For ext: resize2fs.
For XFS: xfs_growfs.
For UFS: growfs.

XFS/UFS growth is one-way in the chapter context.

## 13. RAID mental model

RAID 0:
- striping;
- performance;
- no redundancy.

RAID 1:
- mirroring;
- redundancy.

RAID 5/6:
- distributed parity;
- more efficient capacity;
- rebuild/parity complexity.

RAID 1+0 / 0+1 combine striping and mirroring.

RAID is not backup.

## 14. mdadm operational flow

Create:

~~~bash
mdadm --create /dev/md/name --level=5 --raid-devices=3 ...
cat /proc/mdstat
~~~

Document:

~~~bash
mdadm --detail --scan
~~~

Failure exercise:

~~~text
-f → mark failed
-r → remove
-a → re-add
→ monitor rebuild in /proc/mdstat
~~~

Rebuild can take hours/days.

## 15. Filesystem model

Traditional:
- UFS;
- ext4;
- XFS.

Common concepts:
- inode;
- superblock;
- free block map;
- journaling;
- mount point.

Journaling protects filesystem consistency around interrupted updates.

## 16. fsck

fsck checks/repairs filesystem structures.

It can modify metadata.

Operational rule:
- identify exact filesystem;
- understand whether it is mounted;
- know repair impact;
- verify afterwards.

Universal rollback: [Needs confirmation].

## 17. mount / fstab

~~~text
device-or-stable-ID  mountpoint  type  options  dump  pass
~~~

Commands:
- mount;
- umount;
- mount -a;
- mount -a -t ext4.

Incorrect fstab can affect boot.

## 18. Swap

Linux:

~~~bash
mkswap <device>
swapon <device>
swapon -s
~~~

FreeBSD active state:

~~~bash
swapctl -l
~~~

Swap is a workload/design decision, not a universal tuning rule.

## 19. ZFS/Btrfs shared ideas

Both integrate:
- filesystem;
- volume management;
- RAID-like storage;
- copy-on-write;
- block checksums;
- snapshots.

Checksums detect silent corruption; redundant pools may repair from a good copy.

## 20. ZFS hierarchy

~~~text
zpool
→ vdevs
→ datasets / zvols
→ snapshots / clones
~~~

Main tools:
- zpool;
- zfs.

## 21. ZFS pool checks

~~~bash
zpool list
zpool status <pool>
~~~

Look for:
- HEALTH/state;
- READ;
- WRITE;
- CKSUM;
- vdev topology.

Do not mix redundant and non-redundant vdevs casually.

## 22. ZFS datasets/properties

~~~bash
zfs create pool/dataset
zfs list -r pool
zfs get all pool/dataset
zfs set property=value pool/dataset
~~~

Properties can inherit through the dataset hierarchy.

quota limits growth.
reservation reserves pool capacity.

## 23. ZFS snapshots/clones

~~~bash
zfs snapshot dataset@snap
zfs rollback dataset@snap
zfs clone dataset@snap pool/clone
~~~

Snapshot:
- read-only.

Clone:
- writable.

Rollback has dependency/time-order constraints. Newer snapshots may need destructive removal first.

## 24. Btrfs pool model

Create mirrored filesystem:

~~~bash
mkfs.btrfs -L demo -d raid1 /dev/a /dev/b
mount LABEL=demo /mnt/demo
btrfs filesystem usage /mnt/demo
~~~

Unlike ZFS, Btrfs remains integrated with ordinary mount/fstab behavior.

## 25. Btrfs online reconfiguration

~~~bash
btrfs device add /dev/new /mnt/demo
btrfs balance start --full-balance /mnt/demo
~~~

RAID profile conversion:

~~~bash
btrfs balance start -dconvert=<profile> -mconvert=<profile> /mnt/demo
~~~

Balance relocates data and generates significant I/O.

## 26. Btrfs subvolumes/snapshots

~~~bash
btrfs subvolume create /mnt/demo/sub
btrfs subvolume snapshot /mnt/demo/sub /mnt/demo/sub_snap
btrfs subvolume snapshot -r /mnt/demo/sub /mnt/demo/sub_ro
~~~

Snapshots are writable by default; -r creates read-only snapshots.

## 27. ZFS vs Btrfs operational distinction in the chapter

ZFS:
- rich hierarchical properties;
- strong pool/vdev architecture;
- SSD read-cache integration;
- topology changes are more constrained.

Btrfs:
- simpler mount model;
- flexible online device changes;
- balance can redistribute/convert layouts.

Do not transfer commands or mental models between them.

## 28. Backup is a separate layer

Replication/RAID protects hardware availability.

Backup protects against broader loss:
- operator error;
- compromise;
- malware;
- logical corruption;
- destructive replication.

A written backup plan must answer:
- what;
- where;
- how often;
- retention;
- encryption;
- key ownership;
- who verifies;
- how often restore tests occur;
- how backups are protected from modification/deletion.

## 29. Operational sequence

~~~text
read-only discovery
→ confirm device identity
→ confirm backup/rollback boundary
→ one layer change
→ verify that layer
→ verify next upper layer
→ record state
~~~

Never batch partitioning, RAID, filesystem and mount changes without intermediate checks.
