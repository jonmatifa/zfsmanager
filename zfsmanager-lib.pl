BEGIN { push(@INC, ".."); };
use WebminCore;
use POSIX qw(strftime);
init_config();
foreign_require("mount", "mount-lib.pl");
my %access = &get_module_acl();

sub properties_list
#return hash of properties that can be set manually and their data type
{
#my ($type)=@_;
#my %list = ( 'boolean' => [ "atime", "canmount", "devices", "exec", "readonly", "setuid", "xattr" ],
#			'string' => [ "aclinherit", "aclmode", "checksum", "compression", "primarycache", "secondarycache", "shareiscsi", "sharenfs", "snapdir" ],
#			'number' => [ "copies", "quota", "recordsize", "refquota", "refreservation", "reservation", "volblocksize" ] );
my %list = ('atime' => 'boolean', 'canmount' => 'boolean', 'devices' => 'boolean', 'exec' => 'boolean', 'nbmand' => 'boolean', 'readonly' => 'boolean', 'setuid' => 'boolean', 'shareiscsi' => 'boolean', 'xattr' => 'boolean', 'utf8only' => 'boolean', 'vscan' => 'boolean', 'zoned' => 'boolean',
			'aclinherit' => 'discard, noallow, restricted, pasthrough, passthrough-x', 'aclmode' => 'discard, groupmaks, passthrough', 'casesensitivity' => 'sensitive, insensitive, mixed', 'checksum' => 'on, off, fletcher2, fletcher4, sha256', 'compression' => 'on, off, lzjb, gzip, gzip-1, gzip-2, gzip-3, gzip-4, gzip-5, gzip-6, gzip-7, gzip-8, gzip-9, zle', 'copies' => '1, 2, 3', 'dedup' => 'on, off, verify, sha256', 'logbias' => 'latency, throughput', 'normalization' => 'none, formC, formD, formKC, formKD', 'primarycache' => 'all, none, metadata', 'secondarycache' => 'all, none, metadata', 'snapdir' => 'hidden, visible', 'snapdev' => 'hidden, visible', 'sync' => 'standard, always, disabled',   
			'mountpoint' => 'special', 'sharesmb' => 'special', 'sharenfs' => 'special', 'mounted' => 'special');
#if ($type != undef)
#{
#	return @list{$type};
#} else 
#{
return %list;
#}
}

sub pool_properties_list
{
my %list = ('autoexpand' => 'boolean', 'autoreplace' => 'boolean', 'delegation' => 'boolean', 'listsnaps' => 'boolean', 
			'failmode' => 'wait, continue, panic', 'feature@async_destroy' => 'enabled, disabled', 'feature@empty_bpobj' => 'enabled, disabled', 'feature@lz4_compress' => 'enabled, disabled', 
			'altroot' => 'special', 'bootfs' => 'special', 'cachefile' => 'special');
return %list;
}

sub create_opts #options and defaults when creating new pool or filesystem
{
my %list = ( 'atime' => 'on', 'compression' => 'off', 'exec' => 'on', 'readonly' => 'off', 'utf8only' => 'off');
return %list;
}

sub get_zfsmanager_config
{
#my ($setting)=@_;
my $lref = &read_file_lines($config{'zfsmanager_conf'});
my %rv;
my $lnum = 0;
foreach my $line (@$lref) {
    my ($n, $v) = split(/=/, $line, 2);
    if ($n) {
	  #$rv{$n} = { 'value' => $v, 'line' => $lnum };
	  $rv{$n} = $v;
      #push(@rv, { 'name' => $n, 'value' => $v, 'line' => $lnum });
      }
    $lnum++;
    }
return %rv;
}

#determine if a property can be edited
sub can_edit
{
my ($zfs, $property) = @_;
%conf = get_zfsmanager_config();
%zfs_props = properties_list();
%pool_props = pool_properties_list();
my %type = zfs_get($zfs, 'type');
if ($type{$zfs}{type}{value} =~ 'snapshot') { return 0; } 
elsif ((($zfs_props{$property}) && ($conf{'zfs_properties'} =~ /1/)) || (($pool_props{$property}) && ($conf{'pool_properties'} =~ /1/))) { return 1; }
}

sub list_zpools
{
my ($pool) = @_;
#zpool list
#my @table=();
my %hash=();
#expecting NAME SIZE ALLOC FREE CAP DEDUP HEALTH ALTROOT
$list=`zpool list -H $pool`;

open my $fh, "<", \$list;
#my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $size, $alloc, $free, $cap, $dedup, $health, $altroot) = split(" ", $line);
    #$hash{$name} = [ $size, $alloc, $free, $cap, $dedup, $health, $altroot ];
	$hash{$name} = { size => $size, alloc => $alloc, free => $free, cap => $cap, dedup => $dedup, health => $health, altroot => $altroot };
}
return %hash;
}

sub list_zfs
{
#zfs list
#my @table=();
my ($zfs) = @_;
my %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list -H $zfs`;

open my $fh, "<", \$list;
#my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $used, $avail, $refer, $mount) = split(" ", $line);
    #$hash{$name} = [ $used, $avail, $refer, $mount ];
	$hash{$name} = { used => $used, avail => $avail, refer => $refer, mount => $mount };
}
return %hash;
}

sub list_snapshots
{
my ($snap) = @_;
#zfs list -t snapshot
#my @table=();
my %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list -t snapshot $snap -H`;

open my $fh, "<", \$list;
#my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $used, $avail, $refer, $mount) = split(" ", $line);
    #$hash{$name} = [ $used, $avail, $refer, $mount ];
	$hash{$name} = { used => $used, avail => $avail, refer => $refer, mount => $mount };
}
return %hash;
}

sub get_alerts
{
my $alerts = `zpool status -x`;
my $alerts = `zpool status -x`;
my %status = ();
my $pool = ();
if ($alerts =~ /all pools are healthy/)
{
	return $alerts;
} else
{
	open my $fh, "<", \$alerts;
	while (my $line =<$fh>)
	{
		chomp ($line);
		$line =~ s/^\s*(.*?)\s*$/$1/;
		my($key, $value) = split(/:/, $line);
		$key =~ s/^\s*(.*?)\s*$/$1/;
		$value =~ s/^\s*(.*?)\s*$/$1/;
		if (($key =~ 'pool') && ($value))
		{
			$pool = $value;
			$status = ( $value );
		} elsif ((($key =~ 'state') || ($key =~ 'errors')) && ($value))
		{
			$status{$pool}{$key} = $value;
		}
	}
	my $out = "<b>";
	foreach $key (sort(keys %status))
	{
		if (true) { $out = $out."pool \'".$key."\' is ".$status{$key}{state}." with ".$status{$key}{errors}."<br />";}
	}
	$out = $out."</b>";
	return $out;
}
}

#zpool_status($pool)
sub zpool_status
{
my ($pool)=@_;
my $parent = "pool";
my %status = ();
my $devs = 0;
my $cmd=`zpool status $pool`;
open my $fh, "<", \$cmd;
while (my $line =<$fh>)
{
    chomp ($line);
	$line =~ s/^\s*(.*?)\s*$/$1/;
	my($key, $value) = split(/:/, $line);
	$key =~ s/^\s*(.*?)\s*$/$1/;
	$value =~ s/^\s*(.*?)\s*$/$1/;
	if (($key =~ 'pool') || ($key =~ 'state') || ($key =~ 'scan') || ($key =~ 'errors') || ($key =~ 'scrub'))
	{
		if ($key =~ 'scrub') { $key = 'scan'; }
		$status{pool}{$key} = $value;
	} elsif (($line =~ "config:") || ($line =~ /NAME/) || ($line =~ /status:/) || ($line =~ /action:/) || ($line =~ /see:/))
	{
		#do nothing
	} else
	{
		my($name, $state, $read, $write, $cksum) = split(" ", $line);
		if (($name =~ $status{pool}{pool}) && (length($name) == length($status{pool}{pool})))
		{
			$status{pool}{name} = $name;
			$status{pool}{read} = $read;
			$status{pool}{write} = $write;
			$status{pool}{cksum} = $cksum;
			
		#check if vdev is a log or cache vdev
		} elsif (($name =~ /log/) || ($name =~ /cache/))
		{
			$status{$name} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => "pool"};
			$parent = $name;
			$devs++;
			
		#check if vdev is a log or cache vdev

		} elsif (($name =~ /mirror/) || ($name =~ /raidz/) || ($name =~ /spare/))
		{
			$status{$name} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
			$parent = $name;
			$devs++;
			
		#for all other vdevs, should be actual devices at this point
		} elsif ($name)
		{
			$status{$name} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
			$devs++;
		}
	}
}
return %status;
}

#zfs_get($pool, $property)
sub zfs_get
{
my ($zfs, $property) = @_;
if (~$property) {my $property="all";}
my %hash=();
my $get=`zfs get $property $zfs -H`;
#return `zfs get $property $zfs -H`;
open my $fh, "<", \$get;
#expecting NAME PROPERTY VALUE SOURCE
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $property, $value, $source) = split(/\t/, $line);
	$hash{$name}{$property} = { value => $value, source => $source };
}
return %hash;
}

#zpool_get($pool, $property)
sub zpool_get
{
my ($pool, $property) = @_;
if (~$property) {my $property="all";}
my %hash=();
my $get=`zpool get $property $pool`;

open my $fh, "<", \$get;
#expecting NAME PROPERTY VALUE SOURCE
my $junk = <$fh>;
while (my $line =<$fh>)
{
    chomp ($line);
	my($name, $property, $value, $source) = split(/\s+/, $line);
	$hash{$name}{$property} = { value => $value, source => $source };
}
return %hash;
}

sub zpool_imports
{
my ($dir) = @_;
if ($dir) { $dir = '-d '.$dir; }
my %status = ();
#my $parent = 'pool';
#my $cmd = `zpool import $dir`;
my @array = split("\n", `zpool import $dir`);
#open my $fh, "<", \$cmd;
foreach $line (@array)
{
    chomp ($line);
	$line =~ s/^\s*(.*?)\s*$/$1/;
	my($key, $value) = split(/:/, $line);
	$key =~ s/^\s*(.*?)\s*$/$1/;
	$value =~ s/^\s*(.*?)\s*$/$1/;
	if (($key =~ 'pool') || ($key =~ 'state') || ($key =~ 'scan') || ($key =~ 'errors') || ($key =~ 'scrub') || ($key =~ 'status') || ($key =~ 'id'))
	{
		if ($key =~ 'pool') { $pool = $value; }
		if ($key =~ 'scrub') { $key = 'scan'; }
		$status{$pool}{$key} = $value;
	} elsif (($line =~ "config:") || ($line =~ /NAME/) || ($line =~ /action:/) || ($line =~ /see:/))
	{
		#do nothing
	} else
	{
		my($name, $state, $status) = split(" ", $line);
		if ($name == $status{$pool}{pool})
		{
			#$status{$pool}{name} = $name;
			#$status{$pool}{state} = $read;
			#$status{$pool}{write} = $write;
			#$status{$pool}{cksum} = $cksum;
			$status{$pool}{vdevs} = ();
			$parent = 'pool';
			
		#check if vdev is a log or cache vdev
		} elsif (($name =~ /log/) || ($name =~ /cache/))
		{
			$status{$pool}{vdevs}{$name} = {name => $name, state => $state, status => $status, parent => "pool"};
			$parent = $name;
			#$devs++;
			
		#check if vdev is a mirror, raidz or spare
		} elsif (($name =~ /mirror/) || ($name =~ /raidz/) || ($name =~ /spare/))
		{
			$status{$pool}{vdevs}{$name} = {name => $name, state => $state, status => $status, parent => $parent};
			$parent = $name;
			#$devs++;
			
		#for all other vdevs, should be actual devices at this point
		} elsif ($name)
		{
			$status{$pool}{vdevs}{$name} = {name => $name, state => $state, status => $status, parent => $parent};
			#$devs++;
		}
	}
}
return %status;
}

sub zpool_list
{
#TODO massage data into something better
my $list=`zpool list`;
return $list;
}

sub list_disk_ids
{
#use Cwd 'abs_path';
my $byid = '/dev/disk/by-id'; #for linux
my $byuuid = '/dev/disk/by-uuid';
opendir (DIR, $byid);
%hash = ();
while (my $file = readdir(DIR)) 
{
	if (!-d $byid."/".$file ) { $hash{'byid'}{$file} = readlink($byid."/".$file); }
}
opendir (DIR, $byuuid);
while (my $file = readdir(DIR)) 
{
	if (!-d $byuuid."/".$file ) { $hash{'byuuid'}{$file} = readlink($byuuid."/".$file); }
}
return %hash;
}

#cmd_online($pool, $vdev)
sub cmd_online
{
my ($pool, $vdev) = @_;
my $cmd = "zpool online $pool $vdev";
my @result = ($cmd, `$cmd`);
return @result;
}

#cmd_offline($pool, $vdev)
sub cmd_offline
{
my ($pool, $vdev) = @_;
my $cmd = "zpool offline $pool $vdev";
my @result = ($cmd, `$cmd`);
return @result;
}

#cmd_remove($pool, $vdev)
sub cmd_remove
{
my ($pool, $vdev) = @_;
my $cmd="zpool remove $pool $vdev";
@result = ($cmd, `$cmd`);
return @result;
}

#cmd_snapshot($snap)
sub cmd_snapshot
{
my ($snap)  = @_;
my $cmd="zfs snapshot $snap";
@result = ($cmd, `$cmd`);
return @result;
}

sub cmd_create_zfs
{
my ($zfs, $options)  = @_;
my $opts = ();
my %createopts = create_opts();
foreach $key (sort(keys %options))
{
	$opts = (($createopts{$key}) && ($options{$key} =~ 'default')) ? $opts : $opts.' -o '.$key.'='.$options{$key};
}
my $cmd="zfs create $opts $zfs";
my @result = ($cmd, `$cmd`);
return @result;
}

sub cmd_create_zpool
{
my ($pool, $dev, $options, $mount, $force) = @_;
my $opts = ();
my %createopts = create_opts();
foreach $key (sort(keys %options))
{
	$opts = ($options{$key} =~ 'default') ? $opts : $opts.' -O '.$key.'='.$options{$key};
}
#if ($opts) { $opts = '-O '.$opts; }
$mount = ($mount) ? '-m '.$mount : ();
my $cmd="zpool create $force $opts $mount $pool $dev";
my @result = ($cmd, `$cmd`);
return @result;
}

sub cmd_zfs_mount
{
my ($zfs, $value, $confirm) = @_;
my $cmd="zfs $value $zfs";
if ($confirm =~ /yes/) 
	{ 
		@result = ($cmd, `$cmd`);
	} else 
	{ 
		@result = ($cmd, "" ); 
	}
return @result;
}

sub cmd_zfs_send
{
my ($snap, $dest, $opts, $confirm) = @_;
my $cmd="zfs send $opts $snap | $dest";
if ($confirm =~ /yes/) 
	{ 
		@result = ($cmd, backquote_logged($cmd));
	} else 
	{ 
		@result = ($cmd, "" ); 
	}
return @result;
}

#cmd_zfs_set($zfs, $property $value, $confirm)
sub cmd_zfs_set
{
my ($zfs, $property, $value, $confirm) = @_;
my $cmd = ($value =~ 'inherit') ? "zfs inherit $property $zfs" : "zfs set $property=$value $zfs";
if ($confirm =~ /yes/) 
	{ 
		@result = ($cmd, `$cmd`);
	} else 
	{ 
		@result = ($cmd, "" ); 
	}
return @result;
}

#cmd_destroy_zfs($zfs, $confirm)
sub cmd_destroy_zfs
{
my ($zfs, $force, $confirm) = @_;
my $cmd="zfs destroy $force $zfs";
if ($confirm =~ /yes/) 
	{ 
		$out =  backquote_logged($cmd);
		chomp $out;
		@result = ( $cmd, $out, 2 );
	} else 
	{ 
		@result = ($cmd, undef ); 
	}
return @result;
}

#cmd_destroy_zpool($zpool, $confirm)
sub cmd_destroy_zpool
{
my ($zpool, $force, $confirm) = @_;
my $cmd="zpool destroy $force $zpool";
if ($confirm =~ /yes/) { @result = ($cmd, (`$cmd`))} else { @result = ($cmd, "" ) };
return @result;
}

sub cmd_zpool
{
my ($pool, $action, $options, $dev, $confirm) = @_;
my $cmd="zpool $action $options $pool $dev";
if ($confirm =~ /yes/) { @result = ($cmd, (backquote_logged($cmd)))} else { @result = ($cmd, "" ) };
return @result;
}

sub cmd_zfs
{
my ($zfs, $action, $options, $confirm) = @_;
my $cmd="zfs $action $options $zfs";
if ($confirm =~ /yes/) { @result = ($cmd, (`$cmd`))} else { @result = ($cmd, "" ) };
return $result;
}


sub ui_zpool_status
{
my ($pool, $action) = @_;
if ($action eq undef) { $action = "status.cgi?pool="; }
my %zpool = list_zpools($pool);
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Cap", "Dedup", "Health"]);
foreach $key (keys %zpool)
{
    print ui_columns_row(["<a href='$action$key'>$key</a>", $zpool{$key}{size}, $zpool{$key}{alloc}, $zpool{$key}{free}, $zpool{$key}{cap}, $zpool{$key}{dedup}, $zpool{$key}{health} ]);
}
print ui_columns_end();
}

sub ui_zpool_properties
{
my ($pool) = @_;
require './property-list-en.pl';
my %hash = zpool_get($pool, "all");
my %props =  property_desc();
my %properties = pool_properties_list();
print ui_table_start("Properties", "width=100%", undef);
foreach $key (sort(keys $hash{$pool}))
{
	if (($properties{$key}) || ($props{$key}))
	{
		print ui_table_row(ui_popup_link($key,'property.cgi?pool='.$pool.'&property='.$key), $hash{$pool}{$key}{value});
	} else {
	print ui_table_row($key, $hash{$pool}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_zfs_list
{
my ($zfs, $action)=@_;
%zfs = list_zfs($zfs);
if ($action eq undef) { $action = "status.cgi?zfs="; }
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
	print ui_columns_row(["<a href='$action$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();
}

sub ui_zfs_properties
{
my ($zfs)=@_;
require './property-list-en.pl';
my %hash = zfs_get($zfs, "all");
my %props =  property_desc();
my %properties = properties_list();
print ui_table_start("Properties", "width=100%", undef);
foreach $key (sort(keys $hash{$zfs}))
{		
	if (($properties{$key}) || ($props{$key}))
	{		
		if ($key =~ 'origin') { print ui_table_row(ui_popup_link($key,'property.cgi?zfs='.$zfs.'&property='.$key), "<a href='snapshot.cgi?snap=$hash{$zfs}{$key}{value}'>$hash{$zfs}{$key}{value}</a>");
		} else { print ui_table_row(ui_popup_link($key,'property.cgi?zfs='.$zfs.'&property='.$key), $hash{$zfs}{$key}{value}); }
	} else {
	print ui_table_row($key, $hash{$zfs}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_list_snapshots
{
my ($zfs, $admin) = @_;
%snapshot = list_snapshots($zfs);
%conf = get_zfsmanager_config();
if ($admin =~ /1/) { 
	#print ui_form_start('cmd.cgi', 'get', 'cmd'); 
	print ui_form_start('cmd.cgi', 'get');
	print ui_hidden('multisnap', 1);
	}
#if ($admin =~ /1/) { print select_all_link('snap', '', "Select All"), " | ", select_invert_link('snap', '', "Invert Selection") }
print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
foreach $key (sort(keys %snapshot))
{
	#print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	if ($admin =~ /1/) {
		print ui_columns_row([ui_checkbox("select", $key.';', "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	} else {
		print ui_columns_row([ "<a href='snapshot.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	#if ($zfs =~ undef) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	#else {
	#	if ($key =~ ($zfs."@")) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	#}
}
print ui_columns_end();
if ($admin =~ /1/) { print select_all_link('select', '', "Select All"), " | ", select_invert_link('select', '', "Invert Selection") }
if (($admin =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print " | ".ui_submit("Destroy selected snapshots"); }
#if (($admin =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print " | Destroy selected snapshots".popup_window_button("cmd.cgi?multisnap=1", 600, 400, ('select', 'select', 'select')); }
if ($admin =~ /1/) { print ui_form_end(); }

}

sub ui_create_snapshot
{
my ($zfs) = @_;
$rv = ui_form_start('cmd.cgi', 'get')."\n";
$rv .= "Create new snapshot based on filesystem: ".$zfs."<br />\n";
my $date = strftime "zfs_manager_%Y-%m-%d-%H%M", localtime;
$rv .= $zfs."@ ".ui_textbox('snap', $date, 28)."\n";
$rv .= ui_hidden('zfs', $zfs)."\n";
#print ui_form_end(["<input type='submit' value='submit'>"]);
$rv .= popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'snap', 'snap', 'snap'], ['zfs', 'zfs', 'zfs'] ] )."\n";
#print ui_form_end([ [popup_window_button('cmd.cgi', '400', '400', '1', [[ 'snap', 'snap', 'snap'], ['zfs', 'zfs', 'zfs']]), "submit" ]]);
return $rv;
}

sub ui_cmd_zpool
{
my ($message, $pool, @params) = @_;
$rv = "Attempting to $message $pool with command... <br />\n";
my $result = cmd_zpool(@params);
$rv .= $result[0]."<br />\n";
if (!$in{'confirm'})
{
	$rv .= "<h3>Would you lke to continue?</h3>\n";
	$rv .= "<a href='$ENV{REQUEST_URI}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>\n";
} else {
	if (($result[1] == //))
	{
		$rv .= "Success! <br />\n";
		$rv .= "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>\n";
	} else
	{
	$rv .= "error: ".$result[1]."<br />\n";
	}
}
return $rv;
}

sub ui_cmd_zfs
{
my ($message, $zfs, @params) = @_;
$rv = "Attempting to $message $zfs with command... <br />\n";
my $result = cmd_zfs(@params);
$rv .= $result[0]."<br />\n";
if (!$params[3])
{
	$rv .= "<h3>Would you lke to continue?</h3>\n";
	$rv .= "<a href='$ENV{REQUEST_URI}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>\n";
} else {
	if (($result[1] == //))
	{
		$rv .= "Success! <br />\n";
		$rv .= "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>\n";
	} else
	{
	$rv .= "error: ".$result[1]."<br />\n";
	}
}
return $rv;
}

sub ui_cmd
{
my ($message, $subject, $result, $confirm) = @_;
$rv = "Attempting to $message $subject with command... <br />\n";
#my $result = cmd_zfs(@params);
$rv .= $result[0]."<br />\n";
if (!$confirm)
{
	$rv .= "<h3>Would you lke to continue?</h3>\n";
	$rv .= "<a href='$ENV{REQUEST_URI}&confirm=yes'>Yes</a> | <a onClick=\"\window.close('cmd')\"\ href=''>No</a>\n";
} else {
	if (($result[1] == //))
	{
		$rv .= "Success! <br />\n";
		$rv .= "<a onClick=\"\window.close('cmd')\"\ href=''>Close</a>\n";
	} else
	{
	$rv .= "error: ".$result[1]."<br />\n";
	}
}
return $rv;
}

sub ui_popup_link
{
my ($name, $url)=@_;
return "<a onClick=\"\window.open('$url', 'cmd', 'toolbar=no,menubar=no,scrollbars=yes,width=600,height=400,resizable=yes'); return false\"\ href='$url'>$name</a>";
}

sub test_function
{

}
