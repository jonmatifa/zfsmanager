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
	   teristics.

	   When the "noauto" option is set, a dataset can only be mounted  and
	   unmounted explicitly. The dataset is not mounted automatically when
	   the dataset is created or imported, nor is it mounted by  the  "zfs
	   mount -a" command or unmounted by the "zfs unmount -a" command.

	   This property is not inherited.',
	   
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
	   
		'copies' => 'Controls the number of copies of  data  stored  for	this  dataset.
	   These  copies  are  in  addition  to any redundancy provided by the
	   pool, for example, mirroring or raid-z. The copies  are  stored  on
	   different  disks, if possible. The space used by multiple copies is
	   charged to the associated file and  dataset,  changing  the	"used"
	   property and counting against quotas and reservations.

	   Changing  this property only affects newly-written data. Therefore,
	   set this property at file system creation time  by  using  the  "-o
	   copies=" option.',
	   
	   'dedup' => 'Configures deduplication for a dataset. The default value is off.
	 The default deduplication checksum is sha256 (this may change in the
	 future).  When dedup is enabled, the checksum defined here overrides
	 the checksum property. Setting the value to verify has the same
	 effect as the setting sha256,verify.

	 If set to verify, ZFS will do a byte-to-byte comparsion in case of
	 two blocks having the same signature to make sure the block contents
	 are identical.',
	   
	   'devices' => 'Controls  whether  device  nodes can be opened on this file system.
	   The default value is "on".',
	   
	   'exec' => 'Controls whether processes can be executed from  within  this  file
	   system. The default value is "on".',
	   
	   'mounted' => 'For file systems, indicates whether the file system is currently
	 mounted. This property can be either yes or no.',
	   
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
	   
	   'utf8only' => 'Indicates whether the file system should reject file names that
	   include characters that are not present in the UTF-8 character code
	   set. If this property is explicitly set to off, the normalization
	   property must either not be explicitly set or be set to none.  The
	   default value for the utf8only property is off.  This property can-
	   not be changed after the file system is created.',
	   
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

