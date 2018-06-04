BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

sub property_desc
#deprecated, migrate all to lang/en
{
my %hash = ( 'aclmode' => 'Controls how an ACL is modified during chmod(2). A file system with
	   an  "aclmode" property of "discard" deletes all ACL entries that do
	   not represent the mode  of  the  file.  An  "aclmode"  property  of
	   "groupmask"	(the  default)	reduces user or group permissions. The
	   permissions are reduced, such that they are	no  greater  than  the
	   group  permission bits, unless it is a user entry that has the same
	   UID as the owner of the file or directory. In this  case,  the  ACL
	   permissions are reduced so that they are no greater than owner per-
	   mission  bits.  A  file  system  with  an  "aclmode"  property   of
	   "passthrough"  indicates  that no changes are made to the ACL other
	   than generating the necessary ACL entries to represent the new mode
	   of the file or directory.',
           
	 'dedupditto' => 'Threshold for the number of block ditto copies. If the reference
	 count for a deduplicated block increases above this number, a new
	 ditto copy of this block is automatically stored. Default setting is
	 0.',
	 
	 'dedupratio' => 'The deduplication ratio specified for a pool, expressed as a
		 multiplier.  For example, a dedupratio value of 1.76 indi-
		 cates that 1.76 units of data were stored but only 1 unit of
		 disk space was actually consumed. See zfs(8) for a descrip-
		 tion of the deduplication feature.',
		 
	'defer_destroy' => 'This property is on if the snapshot has been marked for deferred destroy by using the zfs destroy -d command. Otherwise, the property is off.',
	
	'defcontext' => 'This flag sets the SELinux context for unlabeled files.  See selinux(8) for more information.',
		 
	'delegation' => 'Controls whether a non-privileged user is granted access based on the
	 dataset permissions defined on the dataset. See zfs(8) for more
	 information on ZFS delegated administration.',
	   
	   'devices' => 'Controls  whether  device  nodes can be opened on this file system.
	   The default value is "on".',
	   
	   'exec' => 'Controls whether processes can be executed from  within  this  file
	   system. The default value is "on".',
	   
	   'expandsize' => 'Amount of uninitialized space within the pool or device that can be used to increase the  total  capacity  of  the
                           pool.   Uninitialized  space  consists of any space on an EFI labeled vdev which has not been brought online (i.e.
                           zpool online -e).  This space occurs when a LUN is dynamically expanded.',
	   
	   'failmode' => 'Controls the system behavior in the event of catastrophic pool fail-
	 ure. This condition is typically a result of a loss of connectivity
	 to the underlying storage device(s) or a failure of all devices
	 within the pool. The behavior of such an event is determined as fol-
	 lows:',
	 
	 'feature@async_destroy' => 'GUID                   com.delphix:async_destroy
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           none

           Destroying  a file system requires traversing all of its data in order to return its used space to the pool. Without async_destroy
           the file system is not fully removed until all space has been reclaimed. If the destroy operation is interrupted by  a  reboot  or
           power outage the next attempt to open the pool will need to complete the destroy operation synchronously.

           When  async_destroy is enabled the file system\'s data will be reclaimed by a background process, allowing the destroy operation to
           complete without traversing the entire file system. The background process is able to resume interrupted destroys after  the  pool
           has  been opened, eliminating the need to finish interrupted destroys as part of the open operation. The amount of space remaining
           to be reclaimed by the background process is available through the freeing property.

           This feature is only active while freeing is non-zero.',
		   
	 'feature@empty_bpobj' => 'GUID                   com.delphix:empty_bpobj
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           none

           This feature increases the performance of creating and using a large number of snapshots of a single  filesystem  or  volume,  and
           also reduces the disk space required.

           When  there are many snapshots, each snapshot uses many Block Pointer Objects (bpobj\'s) to track blocks associated with that snap
           shot.  However, in common use cases, most of these bpobj\'s are empty.  This feature allows us to create each bpobj on-demand, thus
           eliminating the empty bpobjs.

           This feature is active while there are any filesystems, volumes, or snapshots which were created after enabling this feature.', 
		   
	 'feature@lz4_compress' => 'GUID                   org.illumos:lz4_compress
           READ-ONLY COMPATIBLE   no
           DEPENDENCIES           none

           lz4 is a high-performance real-time compression algorithm that features significantly faster compression and decompression as well
           as a higher compression ratio than the older lzjb compression.  Typically, lz4 compression is approximately  50%  faster  on  compressible  
		   data and 200% faster on incompressible data than lzjb. It is also approximately 80% faster on decompression, while giving 
		   approximately 10% better compression ratio.

           When the lz4_compress feature is set to enabled, the administrator can turn on lz4 compression on any dataset on  the  pool  using
           the  zfs(8)  command.  Please  note  that doing so will immediately activate the lz4_compress feature on the underlying pool (even
           before any data is written). Since this feature is not read-only compatible, this operation will render the pool  unimportable  on
           systems  without  support  for the lz4_compress feature. At the moment, this operation cannot be reversed. Booting off of lz4-compressed root pools is supported.', 
           
	  'feature@spacemap_histogram' => 'GUID                   com.delphix:spacemap_histogram
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           none

           This features allows ZFS to maintain more information about how free space is organized within the  pool.  If
           this  feature  is  enabled,  ZFS will set this feature to active when a new space map object is created or an
           existing space map is upgraded to the new format. Once the feature is active, it will remain  in  that  state
           until the pool is destroyed.',
           
		'feature@extensible_dataset' => 'GUID                   com.delphix:extensible_dataset
           READ-ONLY COMPATIBLE   no
           DEPENDENCIES           none

           This  feature  allows  more  flexible  use  of internal ZFS data structures, and exists for other features to
           depend on.

           This feature will be active when the first dependent feature uses it, and will be  returned  to  the  enabled
           state when all datasets that use this feature are destroyed.',
           
		'feature@bookmarks' => 'GUID                   com.delphix:bookmarks
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           extensible_dataset

           This feature enables use of the zfs bookmark subcommand.

           This  feature  is  active  while any bookmarks exist in the pool.  All bookmarks in the pool can be listed by
           running zfs list -t bookmark -r poolname.',
           
		'feature@enabled_txg' => 'GUID                   com.delphix:enabled_txg
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           none

           Once this feature is enabled ZFS records the transaction group number in which new features are enabled. This
           has no user-visible impact, but other features may depend on this feature.

           This feature becomes active as soon as it is enabled and will never return to being enabled.',
           
		'feature@hole_birth' => 'GUID                   com.delphix:hole_birth
           READ-ONLY COMPATIBLE   no
           DEPENDENCIES           enabled_txg

           This  feature  improves  performance  of incremental sends ("zfs send -i") and receives for objects with many
           holes. The most common case of hole-filled objects is zvols.

           An incremental send stream from snapshot A to snapshot B contains information about every block that  changed
           between  A  and B. Blocks which did not change between those snapshots can be identified and omitted from the
           stream using a piece of metadata called the ’block birth time’, but birth times are not  recorded  for  holes
           (blocks  filled  only  with  zeroes).  Since holes created after A cannot be distinguished from holes created
           before A, information about every hole in the entire filesystem or zvol is included in the send stream.

           For workloads where holes are rare this is not a problem. However, when incrementally replicating filesystems
           or  zvols  with many holes (for example a zvol formatted with another filesystem) a lot of time will be spent
           sending and receiving unnecessary information about holes that already exist on the receiving side.

           Once the hole_birth feature has been enabled the block birth times of all new holes will be recorded.  Incre-
           mental  sends  between  snapshots  created  after this feature is enabled will use this new metadata to avoid
           sending information about holes that already exist on the receiving side.

           This feature becomes active as soon as it is enabled and will never return to being enabled.',
           
		'feature@embedded_data' => 'GUID                   com.delphix:embedded_data
           READ-ONLY COMPATIBLE   no
           DEPENDENCIES           none

           This feature improves the performance and compression ratio of highly-compressible blocks.  Blocks whose con-
           tents can compress to 112 bytes or smaller can take advantage of this feature.

           When  this  feature  is enabled, the contents of highly-compressible blocks are stored in the block "pointer"
           itself (a misnomer in this case, as it contains the compresseed data, rather than a pointer to  its  location
           on  disk).   Thus the space of the block (one sector, typically 512 bytes or 4KB) is saved, and no additional
           i/o is needed to read and write the data block.

           This feature becomes active as soon as it is enabled and will never return to being enabled.',
	 
	 'feature@large_blocks' => 'GUID                   org.open-zfs:large_block
           READ-ONLY COMPATIBLE   no
           DEPENDENCIES           extensible_dataset

           The large_block feature allows the record size on a dataset to be set larger than 128KB.

           This feature becomes active once a recordsize property has been set larger than 128KB, and will return to being enabled once all
           filesystems that have ever had their recordsize larger than 128KB are destroyed.',
           
     'feature@filesystem_limits' => 'GUID                   com.joyent:filesystem_limits
           READ-ONLY COMPATIBLE   yes
           DEPENDENCIES           extensible_dataset

           This  feature  enables filesystem and snapshot limits. These limits can be used to control how many filesystems and/or snapshots
           can be created at the point in the tree on which the limits are set.

           This feature is active once either of the limit properties has been set on a dataset. Once activated the feature is never  deac‐
           tivated.',      
	 
	 'filesystem_count' => 'The  total  number of filesystems and volumes that exist under this
           location in the dataset tree.  This value is only available when  a
           filesystem_limit has been set somewhere in the tree under which the
           dataset resides.',
	 
	 'filesystem_limit' => 'Limits  the  number of filesystems and volumes that can exist under
           this point in the dataset tree.  The limit is not enforced  if  the
           user  is allowed to change the limit. Setting a filesystem_limit on
           a descendent of a filesystem that already  has  a  filesystem_limit
           does  not  override  the  ancestor\'s  filesystem_limit,  but rather
           imposes an additional limit. This feature must  be  enabled  to  be
           used (see zpool-features(5)).',
	 
	 'fragmentation' => 'The amount of fragmentation in the pool.',
	 
	 'free' => 'Number of blocks within the pool that are not allocated.',
	 
	 'freeing' => 'After a file system or snapshot is destroyed, the space it was using is returned to the pool asynchronously. freeing is the 
	 amount of space remaining to be reclaimed. Over time freeing will decrease while free increases.',
	 
	 'fscontext' => 'This flag sets the SELinux context for the filesytem being mounted.  See selinux(8) for more information.',
	 
	 'guid' => 'A unique identifier for the pool.',
	 
	 'health' => 'The current health of the pool. Health can be "ONLINE",
		 "DEGRADED", "FAULTED", "OFFLINE", "REMOVED", or "UNAVAIL".',
		 
	'listsnapshots' => 'Controls whether information about snapshots associated with this
	 pool is output when "zfs list" is run without the -t option. The
	 default value is off.',
	   
	   'logbias' => 'Provide a hint to ZFS about handling of synchronous requests in this
	 dataset.  If logbias is set to latency (the default), ZFS will use
	 pool log devices (if configured) to handle the requests at low
	 latency. If logbias is set to throughput, ZFS will not use configured
	 pool log devices.  ZFS will instead optimize synchronous operations
	 for global pool throughput and efficient use of resources.',
	 
	 'logicalreferenced' => 'The amount of space that is "logically" accessible by this dataset.  See the referenced property.  The  logical 
	        space ignores the effect of the compression and copies properties, giving a quantity closer to the amount
           of data that applications see.  However, it does include space consumed by metadata.<br />
			<br />
           This property can also be referred to by its shortened column name, lrefer.',
           
		'logicalused' => 'The amount of space that is "logically" consumed by this dataset and all its descendents.  See the used property.   
		    The  logical  space  ignores  the  effect of the compression and copies properties, giving a quantity
           closer to the amount of data that applications see.  However, it does include space consumed by metadata.<br />
			<br />
           This property can also be referred to by its shortened column name, lused.',
	   
	   'mounted' => 'For file systems, indicates whether the file system is currently
	 mounted. This property can be either yes or no.',
	 
	 'mlslabel' => 'The mlslabel property is a sensitivity label that determines if a dataset  can be mounted in a
           zone  on  a system with Trusted Extensions enabled. If the labeled dataset matches the labeled
           zone, the dataset can be mounted  and accessed from the labeled zone.<br />
			<br />
           When the mlslabel property is not set, the default value is none. Setting the  mlslabel  prop‐
           erty to none is equivalent to removing the property.<br />
			<br />
           The  mlslabel  property  can be modified only when Trusted Extensions is enabled and only with
           appropriate privilege. Rights to modify it cannot be delegated. When changing  a  label  to  a
           higher  label  or  setting  the initial dataset label, the {PRIV_FILE_UPGRADE_SL} privilege is
           required. When changing a label to a lower label or the default (none),  the  {PRIV_FILE_DOWN‐
           GRADE_SL}  privilege is required. Changing the dataset to labels other than the default can be
           done only when the dataset is not mounted. When a dataset with the default  label  is  mounted
           into a labeled-zone, the mount operation automatically sets the mlslabel property to the label
           of that zone.<br />
			<br />
           When Trusted Extensions is not enabled, only datasets with the default  label  (none)  can  be
           mounted.<br />
			<br />
           Zones are a Solaris feature and are not relevant on Linux.',
		   
		'mountpoint' => 'Controls the mount point used for this file system. See the "Mount
		Points" section for more information on how this property is used.<br />
		<br />
		When the mountpoint property is changed for a file system, the file
		system and any children that inherit the mount point are unmounted.
		If the new value is legacy, then they remain unmounted. Otherwise,
		they are automatically remounted in the new location if the property
		was previously legacy or none, or if they were mounted before the
		property was changed. In addition, any shared file systems are
		unshared and shared in the new location.',
		
		'normalization' => 'Indicates whether the file system should perform a unicode normal-
	   ization of file names whenever two file names are compared, and
	   which normalization algorithm should be used. File names are always
	   stored unmodified, names are normalized as part of any comparison
	   process. If this property is set to a legal value other than none,
	   and the utf8only property was left unspecified, the utf8only prop-
	   erty is automatically set to on.  The default value of the
	   normalization property is none.  This property cannot be changed
	   after the file system is created.',
	   
	   'nbmand' => 'Controls  whether  the  file system should be mounted with "nbmand"
	   (Non Blocking mandatory locks). This  is  used  for	CIFS  clients.
	   Changes  to	this property only take effect when the file system is
	   umounted and remounted.  See  mount(1M)  for  more  information  on
	   "nbmand" mounts.',
	   
	   'origin' => 'For cloned file systems or volumes, the snapshot from which the clone
	 was created. See also the clones property.',
	 
	 'overlay' => 'Allow  mounting  on  a  busy  directory  or a directory which already contains files/directories. This is the
           default mount behavior for Linux filesystems.  However, for consistency with ZFS on other  platforms  overlay
           mounts are disabled by default.  Set overlay=on to enable overlay mounts.',
	   
	   'primarycache' => 'Controls  what  is cached in the primary cache (ARC). If this prop-
	   erty is set to "all", then both user data and metadata  is  cached.
	   If this property is set to "none", then neither user data nor meta-
	   data is cached. If this property is set to  "metadata",  then  only
	   metadata is cached. The default value is "all".',

	   'referenced' => 'The amount of data that is accessible by this dataset, which may or
	 may not be shared with other datasets in the pool. When a snapshot or
	 clone is created, it initially references the same amount of space as
	 the file system or snapshot it was created from, since its contents
	 are identical.<br />
	<br />
	 This property can also be referred to by its shortened column name,
	 refer.',
	 
	 'refquota' => 'Limits the amount of space a dataset can consume. This property enforces a hard limit  on  the
           amount  of  space  used. This hard limit does not include space used by descendents, including
           file systems and snapshots.',
		   
		'refreservation' => 'The minimum amount of space guaranteed to a dataset, not including
	 its descendents. When the amount of space used is below this value,
	 the dataset is treated as if it were taking up the amount of space
	 specified by refreservation.  The refreservation reservation is
	 accounted for in the parent datasets\' space used, and counts against
	 the parent datasets\' quotas and reservations.<br />
	<br />
	 If refreservation is set, a snapshot is only allowed if there is
	 enough free pool space outside of this reservation to accommodate the
	 current number of "referenced" bytes in the dataset.<br />
	<br />
	 This property can also be referred to by its shortened column name,
	 refreserv.',
	 
	 'reservation' => 'The minimum amount of space guaranteed to a dataset and its descen-
	 dents. When the amount of space used is below this value, the dataset
	 is treated as if it were taking up the amount of space specified by
	 its reservation. Reservations are accounted for in the parent
	 datasets\' space used, and count against the parent datasets\' quotas
	 and reservations.<br />
	<br />
	 This property can also be referred to by its shortened column name,
	 reserv.',
	 
	 'rootcontext' => 'This flag sets the SELinux context for the root inode of the filesystem.  See selinux(8)  for  more  information.',
	   
	   'secondarycache' => 'Controls what is cached in the secondary  cache  (L2ARC).  If  this
	   property  is  set  to  "all",  then	both user data and metadata is
	   cached. If this property is set to "none", then neither  user  data
	   nor metadata is cached. If this property is set to "metadata", then
	   only metadata is cached. The default value is "all".',
	   
	   'shareiscsi' => 'Like  the "sharenfs" property, "shareiscsi" indicates whether a ZFS
	   volume is exported as an iSCSI target. The  acceptable  values  for
	   this  property  are "on", "off", and "type=disk". The default value
	   is "off". In the future, other target types might be supported. For
	   example, "tape".

	   You might want to set "shareiscsi=on" for a file system so that all
	   ZFS volumes within the file system are shared by  default.  Setting
	   this property on a file system has no direct effect, however.',
	   
	   'sharenfs' => 'Controls whether the file system is shared via NFS, and what options
	 are used. A file system with a sharenfs property of off is managed
	 the traditional way via exports(5).  Otherwise, the file system is
	 automatically shared and unshared with the "zfs share" and "zfs
	 unshare" commands. If the property is set to on no NFS export options
	 are used. Otherwise, NFS export options are equivalent to the con-
	 tents of this property. The export options may be comma-separated.
	 See exports(5) for a list of valid options.<br />
	<br />
	 When the sharenfs property is changed for a dataset, the mountd(8)
	 daemon is reloaded.',
	 
	 'sharesmb' => 'Controls whether the file system is shared by using Samba USERSHARES, and what options are  to
           be  used.  Otherwise,  the file system is automatically shared and unshared with the zfs share
           and zfs unshare commands. If the property is set to on, the net(8) command is invoked to  cre‐
           ate a USERSHARE.<br />
			<br />
           Because  SMB  shares  requires a resource name, a unique resource name is constructed from the
           dataset name. The constructed name is a copy of the dataset name except that the characters in
           the  dataset  name,  which would be illegal in the resource name, are replaced with underscore
           (_) characters. The ZFS On Linux driver does not (yet) support additional options which  might
           be availible in the Solaris version.<br />
			<br />
           If the sharesmb property is set to off, the file systems are unshared.<br />
			<br />
           In Linux, the share is created with the ACL (Access Control List) "Everyone:F" ("F" stands for
           "full permissions", ie. read and write permissions) and no guest  access  (which  means  samba
           must  be  able  to authenticate a real user, system passwd/shadow, ldap or smbpasswd based) by
           default. This means that any additional access control (dissalow specific user specific access
           etc) must be done on the underlaying filesystem.<br />
			<br />
             Example  to  mount  a  SMB  filesystem  shared through ZFS (share/tmp): Note that a user and
             his/her password must be given!<br />
			<br />
               smbmount //127.0.0.1/share_tmp /mnt/tmp -o user=workgroup/turbo,password=obrut,uid=1000<br />
			<br />
           Minimal /etc/samba/smb.conf configuration<br />
			<br />
             * Samba will need to listen to \'localhost\' (127.0.0.1) for the zfs utilities to communitate
             with samba.  This is the default behavior for most Linux distributions.<br />
			<br />
             * Samba must be able to authenticate a user. This can be done in a number of ways, depending
             on if using the system password file, LDAP or the Samba specific smbpasswd file. How to do
             this is outside the scope of this manual. Please refer to the smb.conf(5) manpage for more
             information.<br />
			<br />
             * See the USERSHARE section of the smb.conf(5) man page for all configuration options in
             case you need to modify any options to the share afterwards. Do note that any changes done
             with the \'net\' command will be undone if the share is every unshared (such as at a reboot
             etc). In the future, ZoL will be able to set specific options directly using
             sharesmb=&#60;option&#62;.',
			 
	'size' => 'Total size of the storage pool.',

		'snapdir' => 'Controls  whether  the ".zfs" directory is hidden or visible in the
	   root of the file system as discussed in  the  "Snapshots"  section.
	   The default value is "hidden".',
	   
	   'snapdev' => 'Controls whether the snapshots devices of zvol\'s are hidden or visible. The default value is hidden.',
	   
	   'snapshot_count' => 'The total number of snapshots that exist under this location in the
           dataset tree.  This value is only available when  a  snapshot_limit
           has been set somewhere in the tree under which the dataset resides.',
	   
	   'snapshot_limit' => '  Limits the number of snapshots that can be created on a dataset and
           its descendents. Setting a snapshot_limit  on  a  descendent  of  a
           dataset  that  already  has  a snapshot_limit does not override the
           ancestor\'s snapshot_limit, but rather imposes an additional  limit.
           The  limit  is  not  enforced  if the user is allowed to change the
           limit. For example, this means that recursive snapshots taken  from
           the global zone are counted against each delegated dataset within a
           zone. This feature must be  enabled  to  be  used  (see  zpool-fea‐
           tures(5)).',
	   
	   'setuid' => 'Controls whether the set-UID bit is respected for the file  system.
	   The default value is "on".',
	   
	   'sync' => 'Controls the behavior of synchronous requests (e.g.  fsync(2),
	 O_DSYNC). This property accepts the following values:

	     standard  This is the POSIX specified behavior of ensuring all
		       synchronous requests are written to stable storage and
		       all devices are flushed to ensure data is not cached by
		       device controllers (this is the default).

	     always    All file system transactions are written and flushed
		       before their system calls return. This has a large per-
		       formance penalty.

	     disabled  Disables synchronous requests. File system transactions
		       are only committed to stable storage periodically. This
		       option will give the highest performance.  However, it
		       is very dangerous as ZFS would be ignoring the synchro-
		       nous transaction demands of applications such as data-
		       bases or NFS.  Administrators should only use this
		       option when the risks are understood.',
	
		'type' => 'The type of dataset: filesystem, volume, or snapshot.',
		
		'used' => 'The amount of space consumed by this dataset and all its descendents.
	 This is the value that is checked against this dataset\'s quota and
	 reservation. The space used does not include this dataset\'s reserva-
	 tion, but does take into account the reservations of any descendent
	 datasets. The amount of space that a dataset consumes from its par-
	 ent, as well as the amount of space that are freed if this dataset is
	 recursively destroyed, is the greater of its space used and its
	 reservation.<br />
	<br />
	 When snapshots (see the "Snapshots" section) are created, their space
	 is initially shared between the snapshot and the file system, and
	 possibly with previous snapshots. As the file system changes, space
	 that was previously shared becomes unique to the snapshot, and
	 counted in the snapshot\'s space used. Additionally, deleting snap-
	 shots can increase the amount of space unique to (and used by) other
	 snapshots.<br />
	<br />
	 The amount of space used, available, or referenced does not take into
	 account pending changes. Pending changes are generally accounted for
	 within a few seconds. Committing a change to a disk using fsync(2) or
	 O_SYNC does not necessarily guarantee that the space usage informa-
	 tion is updated immediately.',
		
		'usedbychildren' => 'The amount of space used by children of this dataset, which would be
	 freed if all the dataset\'s children were destroyed.',
	 
		'usedbydataset' => 'The amount of space used by this dataset itself, which would be freed
	 if the dataset were destroyed (after first removing any
	 refreservation and destroying any necessary snapshots or descen-
	 dents).',
	 
		'usedbysnapshots' => 'The amount of space consumed by snapshots of this dataset. In partic-
	 ular, it is the amount of space that would be freed if all of this
	 dataset\'s snapshots were destroyed. Note that this is not simply the
	 sum of the snapshots\' used properties because space can be shared by
	 multiple snapshots.',
	 
		'usedbyrefreservation' => 'The amount of space used by a refreservation set on this dataset,
	 which would be freed if the refreservation was removed.',
	 
	 'userrefs' => 'This property is set to the number of user holds on this snapshot. User holds are set by using the zfs hold command.
groupused@group
The amount of space consumed by the specified group in this dataset. Space is charged to the group of each file, as displayed by ls -l. See the userused@user property for more information.
Unprivileged users can only access their own groups\' space usage. The root user, or a user who has been granted the groupused privilege with zfs allow, can access all groups\' usage.',
	   
	   'utf8only' => 'Indicates whether the file system should reject file names that
	   include characters that are not present in the UTF-8 character code
	   set. If this property is explicitly set to off, the normalization
	   property must either not be explicitly set or be set to none.  The
	   default value for the utf8only property is off.  This property can-
	   not be changed after the file system is created.',
	   
	   'version' => 'The current on-disk version of the pool. This can be increased, but
	 never decreased. The preferred method of updating pools is with the
	 "zpool upgrade" command, though this property can be used when a spe-
	 cific version is needed for backwards compatibility.  Once feature
	 flags is enabled on a pool this property will no longer have a value.',
	 
	 'volblocksize' => 'For volumes, specifies	the block size of the volume. The blocksize
	 cannot	be changed once	the volume has been written, so	it should be
	 set at	volume creation	time. The default blocksize for	volumes	is 8
	 Kbytes. Any power of 2	from 512 bytes to 128 Kbytes is	valid.

	 This property can also	be referred to by its shortened	column name,
	 volblock.',
	 
	 'volsize' => 'For volumes, specifies	the logical size of the	volume.	By default,
	 creating a volume establishes a reservation of	equal size. For	storage 
	 pools with	a version number of 9 or higher, a refreservation is
	 set instead. Any changes to volsize are reflected in an equivalent
	 change	to the reservation (or refreservation).	 The volsize can only
	 be set	to a multiple of volblocksize, and cannot be zero.

	 The reservation is kept equal to the volume\'s logical size to prevent
	 unexpected behavior for consumers. Without the	reservation, the volume 
	 could run out of space, resulting in undefined behavior or	data
	 corruption, depending on how the volume is used. These	effects	can
	 also occur when the volume size is changed while it is	in use (particularly 
	 when	shrinking the size). Extreme care should be used when
	 adjusting the volume size.

	 Though	not recommended, a "sparse volume" (also known as "thin	provisioning") 
	 can be created by specifying	the -s option to the "zfs
	 create	-V" command, or	by changing the	reservation after the volume
	 has been created. A "sparse volume" is	a volume where the reservation
	 is less then the volume size.	Consequently, writes to	a sparse volume 
	 can fail with ENOSPC when the pool	is low on space. For a sparse
	 volume, changes to volsize are	not reflected in the reservation.',
	   
	   'vscan' => 'Controls whether regular files should be scanned for viruses when a
	   file  is  opened and closed. In addition to enabling this property,
	   the virus scan service must also be enabled for virus  scanning  to
	   occur. The default value is "off".',
	   
	   'written' => 'The amount of referenced space	written	to this	dataset	since the previous snapshot.',
	   
	   'xattr' => 'Controls whether extended attributes are enabled for this file system. The default value is on.',
	   
	   'zoned' => 'Controls whether the dataset is managed from a non-global zone. See
	   the	"Zones"  section  for  more  information. The default value is
	   "off".<br /><br />
	   
	   <h4>Zones</h4>
	   A  ZFS file system can be added to a non-global zone by using zonecfg\'\s
       "add fs" subcommand. A ZFS file system that is added  to  a  non-global
       zone must have its mountpoint property set to legacy.

       The  physical  properties of an added file system are controlled by the
       global administrator. However, the zone administrator can create,  mod-
       ify,  or  destroy  files within the added file system, depending on how
       the file system is mounted.

       A dataset can also be delegated to a non-global zone by using zonecfg\'\s
       "add dataset" subcommand. You cannot delegate a dataset to one zone and
       the children of the same dataset to another zone. The zone  administra-
       tor  can  change properties of the dataset or any of its children. How-
       ever, the "quota" property is controlled by the global administrator.

       A ZFS volume can be added as a device to a  non-global  zone  by  using
       zonecfg\'\s "add device" subcommand. However, its physical properties can
       only be modified by the global administrator.

       For more information about zonecfg syntax, see zonecfg(1M).

       After a dataset is delegated to a non-global zone, the "zoned" property
       is  automatically  set.	A  zoned  file system cannot be mounted in the
       global zone, since the zone administrator might have to set  the  mount
       point to an unacceptable value.

       The  global  administrator  can	forcibly  clear  the "zoned" property,
       though this should be done with extreme care. The global  administrator
       should  verify that all the mount points are acceptable before clearing
       the property.');
return %hash;
}

