BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

sub property_desc
{
my %hash = ( 'aclinherit' => 'Controls how ACL entries are inherited when files  and  directories
	   are	created.  A file system with an "aclinherit" property of "dis-
	   card" does not inherit any ACL  entries.  A	file  system  with  an
	   "aclinherit"  property value of "noallow" only inherits inheritable
	   ACL entries that specify "deny"  permissions.  The  property  value
	   "restricted"    (the   default)   removes   the   "write_acl"   and
	   "write_owner" permissions when the ACL entry is inherited.  A  file
	   system  with an "aclinherit" property value of "passthrough" inher-
	   its all inheritable ACL entries without any modifications  made  to
	   the	ACL  entries  when  they  are inherited. A file system with an
	   "aclinherit" property value of "passthrough-x" has the same meaning
	   as  "passthrough",  except  that  the owner@, group@, and everyone@
	   ACEs inherit the execute permission only if the file creation  mode
	   also requests the execute bit.

	   When  the property value is set to "passthrough," files are created
	   with a mode determined by the inheritable ACEs. If  no  inheritable
	   ACEs exist that affect the mode, then the mode is set in accordance
	   to the requested mode from the application.',
	   
	   'aclmode' => 'Controls how an ACL is modified during chmod(2). A file system with
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
	   
	   'allocated' => 'Amount of storage space within the pool that has been physi-
		 cally allocated.',
		 
	   'altroot' => 'Alternate root directory. If set, this directory is prepended to any
	 mount points within the pool. This can be used when examining an
	 unknown pool where the mount points cannot be trusted, or in an
	 alternate boot environment, where the typical paths are not valid.
	 altroot is not a persistent property. It is valid only while the sys-
	 tem is up.  Setting altroot defaults to using cachefile=none, though
	 this may be overridden using an explicit setting.',
	 
	   'autoexpand' => 'Controls automatic pool expansion when the underlying LUN is grown.
	 If set to "on", the pool will be resized according to the size of the
	 expanded device. If the device is part of a mirror or raidz then all
	 devices within that mirror/raidz group must be expanded before the
	 new space is made available to the pool. The default behavior is
	 "off".  This property can also be referred to by its shortened column
	 name, expand.',
	 
	 'autoreplace' => 'Controls automatic device replacement. If set to "off", device
	 replacement must be initiated by the administrator by using the
	 "zpool replace" command. If set to "on", any new device, found in the
	 same physical location as a device that previously belonged to the
	 pool, is automatically formatted and replaced. The default behavior
	 is "off".  This property can also be referred to by its shortened
	 column name, "replace".',
	   
	   'available' => 'The	amount of space available to the dataset and all its children,
	   assuming that there is no other activity in the pool. Because space
	   is  shared within a pool, availability can be limited by any number
	   of factors, including physical pool size, quotas, reservations,  or
	   other datasets within the pool.

	   This property can also be referred to by its shortened column name,
	   "avail".',
	   
	   'bootfs' => 'Identifies the default bootable dataset for the root pool. This prop-
	 erty is expected to be set mainly by the installation and upgrade
	 programs.',
	 
	 'cachefile' => 'Controls the location of where the pool configuration is cached. Dis-
	 covering all pools on system startup requires a cached copy of the
	 configuration data that is stored on the root file system. All pools
	 in this cache are automatically imported when the system boots. Some
	 environments, such as install and clustering, need to cache this
	 information in a different location so that pools are not automati-
	 cally imported. Setting this property caches the pool configuration
	 in a different location that can later be imported with "zpool import
	 -c".  Setting it to the special value "none" creates a temporary pool
	 that is never cached, and the special value \'\' (empty string) uses
	 the default location',
	 
	 'capacity' => 'Percentage of pool space used. This property can also be
		 referred to by its shortened column name, "cap".',
	   
	   'checksum' => 'Controls  the  checksum  used to verify data integrity. The default
	   value is "on", which automatically selects an appropriate algorithm
	   (currently, fletcher2, but this may change in future releases). The
	   value "off" disables integrity checking  on	user  data.  Disabling
	   checksums is NOT a recommended practice.',
	   
		'atime' => 'Controls whether the access time for files is updated when they are
	   read. Turning this property off avoids producing write traffic when
	   reading  files  and	can  result  in significant performance gains,
	   though it might confuse mailers and other  similar  utilities.  The
	   default value is "on".',
	   
	   'canmount' => 'If  this  property  is  set	to  "off",  the  file system cannot be
	   mounted, and is ignored by "zfs mount -a". Setting this property to
	   "off"  is  similar  to setting the "mountpoint" property to "none",
	   except that the dataset still has a normal  "mountpoint"  property,
	   which  can  be  inherited.  Setting	this  property to "off" allows
	   datasets to be used solely as a mechanism  to  inherit  properties.
	   One	example  of  setting canmount=off is to have two datasets with
	   the same mountpoint, so that the children of both  datasets	appear
	   in  the  same directory, but might have different inherited charac-
	   teristics.<br />
		<br />
	   When the "noauto" option is set, a dataset can only be mounted  and
	   unmounted explicitly. The dataset is not mounted automatically when
	   the dataset is created or imported, nor is it mounted by  the  "zfs
	   mount -a" command or unmounted by the "zfs unmount -a" command.<br />
	<br />
	   This property is not inherited.',
	   
	   'casesensitivity' => 'Indicates whether the file name matching algorithm used by the file system should be case-sensitive, 
		case-insensitive, or allow a combination of both styles of matching. The default value
		for the casesensitivity property is sensitive. Traditionally, UNIX and POSIX file systems have
		case-sensitive file names.<br />
		<br />
		The mixed value for the casesensitivity property indicates that the file  system  can  support
		requests  for  both  case-sensitive  and  case-insensitive matching behavior. Currently, case-
		insensitive matching behavior on a file system that supports mixed behavior is limited to  the
		Solaris  CIFS  server  product.  For  more information about the mixed value behavior, see the
		Solaris ZFS Administration Guide.',
	   
		'compression' => 'Controls  the  compression  algorithm  used	for  this dataset. The
	   "lzjb" compression algorithm is  optimized  for  performance  while
	   providing decent data compression. Setting compression to "on" uses
	   the "lzjb" compression algorithm. The "gzip" compression  algorithm
	   uses  the  same compression as the gzip(1) command. You can specify
	   the "gzip" level by using the value "gzip-N" where N is an  integer
	   from  1  (fastest) to 9 (best compression ratio). Currently, "gzip"
	   is equivalent to "gzip-6" (which is also the default for  gzip(1)).

	   This  property can also be referred to by its shortened column name
	   "compress".',
	   
	   'compressratio' => 'The compression ratio achieved for this  dataset,  expressed  as  a
	   multiplier.	Compression  can be turned on by running "zfs set com-
	   pression=on dataset". The default value is "off".',
	   
		'copies' => 'Controls the number of copies of  data  stored  for	this  dataset.
	   These  copies  are  in  addition  to any redundancy provided by the
	   pool, for example, mirroring or raid-z. The copies  are  stored  on
	   different  disks, if possible. The space used by multiple copies is
	   charged to the associated file and  dataset,  changing  the	"used"
	   property and counting against quotas and reservations.

	   Changing  this property only affects newly-written data. Therefore,
	   set this property at file system creation time  by  using  the  "-o
	   copies=" option.',
	   
	   'creation' => 'The time this dataset was created.',
	   
	   'dedup' => 'Configures deduplication for a dataset. The default value is off.
	 The default deduplication checksum is sha256 (this may change in the
	 future).  When dedup is enabled, the checksum defined here overrides
	 the checksum property. Setting the value to verify has the same
	 effect as the setting sha256,verify.

	 If set to verify, ZFS will do a byte-to-byte comparsion in case of
	 two blocks having the same signature to make sure the block contents
	 are identical.',
	 
	 'dedupditto' => 'Threshold for the number of block ditto copies. If the reference
	 count for a deduplicated block increases above this number, a new
	 ditto copy of this block is automatically stored. Default setting is
	 0.',
	 
	 'dedupratio' => 'The deduplication ratio specified for a pool, expressed as a
		 multiplier.  For example, a dedupratio value of 1.76 indi-
		 cates that 1.76 units of data were stored but only 1 unit of
		 disk space was actually consumed. See zfs(8) for a descrip-
		 tion of the deduplication feature.',
		 
	'delegation' => 'Controls whether a non-privileged user is granted access based on the
	 dataset permissions defined on the dataset. See zfs(8) for more
	 information on ZFS delegated administration.',
	   
	   'devices' => 'Controls  whether  device  nodes can be opened on this file system.
	   The default value is "on".',
	   
	   'exec' => 'Controls whether processes can be executed from  within  this  file
	   system. The default value is "on".',
	   
	   'failmode' => 'Controls the system behavior in the event of catastrophic pool fail-
	 ure. This condition is typically a result of a loss of connectivity
	 to the underlying storage device(s) or a failure of all devices
	 within the pool. The behavior of such an event is determined as fol-
	 lows:',
	 
	 'free' => 'Number of blocks within the pool that are not allocated.',
	 
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
	   
	   'primarycache' => 'Controls  what  is cached in the primary cache (ARC). If this prop-
	   erty is set to "all", then both user data and metadata  is  cached.
	   If this property is set to "none", then neither user data nor meta-
	   data is cached. If this property is set to  "metadata",  then  only
	   metadata is cached. The default value is "all".',
	   
	   'quota' => 'Limits  the	amount of space a dataset and its descendents can con-
	   sume. This property enforces a hard limit on the  amount  of  space
	   used.  This	includes  all space consumed by descendents, including
	   file systems and snapshots. Setting a quota on a  descendent  of  a
	   dataset  that  already has a quota does not override the ancestor\'\s
	   quota, but rather imposes an additional limit.

	   Quotas cannot be set on volumes, as the "volsize" property acts  as
	   an implicit quota.',
	   
	   'recordsize' => 'Specifies a suggested block size for files in the file system. This
	   property is designed solely for use with  database  workloads  that
	   access  files  in fixed-size records. ZFS automatically tunes block
	   sizes according to internal algorithms optimized for typical access
	   patterns.

	   For databases that create very large files but access them in small
	   random chunks, these algorithms may	be  suboptimal.  Specifying  a
	   "recordsize"  greater than or equal to the record size of the data-
	   base can result in significant performance gains. Use of this prop-
	   erty  for general purpose file systems is strongly discouraged, and
	   may adversely affect performance.

	   The size specified must be a power of two greater than or equal  to
	   512 and less than or equal to 128 Kbytes.

	   Changing  the  file	system\'\s recordsize only affects files created
	   afterward; existing files are unaffected.

	   This property can also be referred to by its shortened column name,
	   "recsize".',
	   
	   'readonly' => 'Controls whether this dataset can be modified. The default value is
	   "off".

	   This property can also be referred to by its shortened column name,
	   "rdonly".',
	   
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
	   
	   'vscan' => 'Controls whether regular files should be scanned for viruses when a
	   file  is  opened and closed. In addition to enabling this property,
	   the virus scan service must also be enabled for virus  scanning  to
	   occur. The default value is "off".',
	   
	   'xattr' => 'Controls whether regular files should be scanned for viruses when a
	   file  is  opened and closed. In addition to enabling this property,
	   the virus scan service must also be enabled for virus  scanning  to
	   occur. The default value is "off".',
	   
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

