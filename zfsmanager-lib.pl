BEGIN { push(@INC, ".."); };
use WebminCore;
use POSIX qw(strftime);
init_config();
foreign_require("mount", "mount-lib.pl");
my %access = &get_module_acl();

sub properties_list
#return hash of properties that can be set manually and their data type
{
my %list = ('atime' => 'boolean', 'canmount' => 'boolean', 'devices' => 'boolean', 'exec' => 'boolean', 'nbmand' => 'boolean', 'readonly' => 'boolean', 'setuid' => 'boolean', 'shareiscsi' => 'boolean', 'utf8only' => 'boolean', 'vscan' => 'boolean', 'zoned' => 'boolean', 'relatime' => 'boolean', 'overlay' => 'boolean',
			'aclinherit' => 'discard, noallow, restricted, pasthrough, passthrough-x', 'aclmode' => 'discard, groupmaks, passthrough', 'casesensitivity' => 'sensitive, insensitive, mixed', 'checksum' => 'on, off, fletcher2, fletcher4, sha256', 'compression' => 'on, off, lzjb, lz4, gzip, gzip-1, gzip-2, gzip-3, gzip-4, gzip-5, gzip-6, gzip-7, gzip-8, gzip-9, zle', 'copies' => '1, 2, 3', 'dedup' => 'on, off, verify, sha256', 'logbias' => 'latency, throughput', 'normalization' => 'none, formC, formD, formKC, formKD', 'primarycache' => 'all, none, metadata', 'secondarycache' => 'all, none, metadata', 'snapdir' => 'hidden, visible', 'snapdev' => 'hidden, visible', 'sync' => 'standard, always, disabled', 'xattr' => 'on, off, sa', 'com.sun:auto-snapshot' => 'true, false', 'acltype' => 'noacl, posixacl', 'redundant_metadata' => 'all, most',
			'mountpoint' => 'special', 'sharesmb' => 'special', 'sharenfs' => 'special', 'mounted' => 'special', 'volsize' => 'special', 'context' => 'special', 'defcontext' => 'special', 'fscontext' => 'special', 'rootcontext' => 'special');
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
			'failmode' => 'wait, continue, panic', 'feature@async_destroy' => 'enabled, disabled', 'feature@empty_bpobj' => 'enabled, disabled', 'feature@lz4_compress' => 'enabled, disabled', 'feature@embedded_data' => 'enabled, disabled', 'feature@enabled_txg' => 'enabled, disabled', 'feature@bookmarks' => 'enabled, disabled', 'feature@hole_birth' => 'enabled, disabled', 'feature@spacemap_histogram' => 'enabled, disabled', 'feature@extensible_dataset' => 'enabled, disabled',
			'altroot' => 'special', 'bootfs' => 'special', 'cachefile' => 'special', 'comment' => 'special');
return %list;
}

sub create_opts #options and defaults when creating new pool or filesystem
{
my %list = ( 'atime' => 'on', 'compression' => 'off', 'dedup' => 'off', 'readonly' => 'off', 'utf8only' => 'off', 'xattr' => 'on' );
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
#expecting NAME SIZE ALLOC FREE FRAG CAP DEDUP HEALTH ALTROOT
$list=`zpool list -o name,size,alloc,free,frag,cap,dedup,health,altroot -H $pool`;

open my $fh, "<", \$list;
#my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $size, $alloc, $free, $frag, $cap, $dedup, $health, $altroot) = split(" ", $line);
    #$hash{$name} = [ $size, $alloc, $free, $frag, $cap, $dedup, $health, $altroot ];
	$hash{$name} = { size => $size, alloc => $alloc, free => $free, frag => $frag, cap => $cap, dedup => $dedup, health => $health, altroot => $altroot };
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
$list=`zfs list -o name,used,avail,refer,mountpoint -H $zfs`;

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
		if (true) { $out .= "pool \'".$key."\' is ".$status{$key}{state}." with ".$status{$key}{errors}."<br />";}
	}
	$out .= "</b>";
	return $out;
}
}

#zpool_status($pool)
sub zpool_status
{
my ($pool)=@_;
my $parent = "pool";
my %status = ();
my $cmd=`zpool status $pool`;
(undef, $cmdout) = split(/  pool: /, $cmd);
($status{0}{pool}, $cmdout) = split(/ state: /, $cmdout);
chomp $status{0}{pool};
if (index($cmd, "status: ") != -1) { 
	($status{0}{state}, $cmdout) = split("status: ", $cmdout); 
	($status{0}{status}, $cmdout) = split("action: ", $cmdout); 
	if (index($cmd, "  see: ") != -1) { 
		($status{0}{action}, $cmdout) = split("  see: ", $cmdout); 
		($status{0}{see}, $cmdout) = split("  scan: ", $cmdout); 
	} else { ($status{0}{action}, $cmdout) = split("  scan: ", $cmdout); }
} else {
	($status{0}{state}, $cmdout) = split("  scan: ", $cmdout); 
}
($status{0}{scan}, $cmdout) = split("config:", $cmdout); 
($status{0}{config}, $status{0}{errors}) = split("errors: ", $cmdout); 

$fh= $status{0}{config};
@array = split("\n", $fh);
foreach $line (@array) #while (my $line =<$fh>) 
{
    chomp ($line);
	my($name, $state, $read, $write, $cksum) = split(" ", $line);

	if ($name =~ "NAME") { #do nothing 
	} elsif (($name =~ $status{0}{pool}) && (length($name) == length($status{0}{pool}))) {
		$status{0}{name} = $name;
		$status{0}{read} = $read;
		$status{0}{write} = $write;
		$status{0}{cksum} = $cksum;
		$devs++;
		
	#check if vdev is a log or cache vdev
	} elsif (($name =~ /log/) || ($name =~ /cache/))
	{
		$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => "pool",};
		$parent = $name;
		$devs++;
		
	#check if vdev is a log or cache vdev
	} elsif (($name =~ /mirror/) || ($name =~ /raidz/) || ($name =~ /spare/))
	{
		$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
		$parent = $name;
		$devs++;

	#for all other vdevs, should be actual devices at this point
	} elsif ($name)
	{
		$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent,};
		$devs++;
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
	#$hash->{$name->{$property->{'value'}}} = $value;
	#$hash->{$name->{$property->{'source'}}} = $source;
}
return %hash;
}

#zpool_get($pool, $property)
sub zpool_get
{
my ($pool, $property) = @_;
if (~$property) {my $property="all";}
my %hash=();
my $get=`zpool get -H $property $pool`;

open my $fh, "<", \$get;
#expecting NAME PROPERTY VALUE SOURCE
#my $junk = <$fh>;
while (my $line =<$fh>)
{
    chomp ($line);
	my($name, $property, $value, $source) = split(/\t/, $line);
	$hash{$name}{$property} = { value => $value, source => $source };
}
return %hash;
}

sub zpool_imports
{
my ($dir, $destroyed) = @_;
if ($dir) { $dir = '-d '.$dir; }
my %status = ();
#my $parent = 'pool';
#my $cmd = `zpool import $dir`;
my @array = split("\n", `zpool import $dir $destroyed`);
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

sub cmd_create_zfs
#deprecated
{
my ($zfs, $options)  = @_;
my $opts = ();
my %createopts = create_opts();
$createopts{'volblocksize'} = '8k';
#$createopts{'sparse'} = '0';
if (${$options}{'sparse'}) { $opts .= "-s "; }
delete ${$options}{'sparse'};
if (${$options}{'zvol'}) { 
	$zfs = "-V ".${$options}{'zvol'}." ".$zfs; 
	delete ${$options}{'zvol'};
}
foreach $key (sort(keys %${options}))
{
	$opts = (($createopts{$key}) && (${$options}{$key} =~ 'default')) ? $opts : $opts.' -o '.$key.'='.${$options}{$key};
}
my $cmd="zfs create $opts $zfs";
#my @result = ($cmd, `$cmd 2>&1`);
return $cmd;
}

sub cmd_create_zpool
#deprecated
{
my ($pool, $dev, $options, $poolopts, $force) = @_;
my $opts = ();
#my %createopts = create_opts();
#if ( $options{'version'} ) { $opts .= "-o version=".$options{'version'}; }
foreach $key (sort(keys %{$poolopts}))
{
	$opts = (${$poolopts}{$key} =~ 'default') ? $opts : $opts.' -o '.$key.'='.${$poolopts}{$key};
}
foreach $key (sort(keys %{$options}))
{
	$opts = (${$options}{$key} =~ 'default') ? $opts : $opts.' -O '.$key.'='.${$options}{$key};
}
#if ($opts) { $opts = '-O '.$opts; }
#$mount = ($mount) ? '-m '.$mount : ();
my $cmd="zpool create $force $opts $pool $dev";
#my @result = ($cmd, `$cmd 2>&1`);
return $cmd;
}

sub ui_zpool_status
{
my ($pool, $action) = @_;
if ($action eq undef) { $action = "status.cgi?pool="; }
my %zpool = list_zpools($pool);
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Frag", "Cap", "Dedup", "Health"]);
foreach $key (keys %zpool)
{
    print ui_columns_row(["<a href='$action$key'>$key</a>", $zpool{$key}{size}, $zpool{$key}{alloc}, $zpool{$key}{free}, $zpool{$key}{frag}, $zpool{$key}{cap}, $zpool{$key}{dedup}, $zpool{$key}{health} ]);
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
foreach $key (sort(keys %{$hash{$pool}}))
{
	if (($properties{$key}) || ($props{$key}))
	{
		print ui_table_row('<a href="property.cgi?pool='.$pool.'&property='.$key.'">'.$key.'</a>', $hash{$pool}{$key}{value});
	} else {
	print ui_table_row($key, $hash{$pool}{$key}{value});
	#print ui_table_row($key, $hash{$pool}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_zfs_list
{
my ($zfs, $action)=@_;
my %zfs = list_zfs($zfs);
if ($action eq undef) { $action = "status.cgi?zfs="; }
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
	print ui_columns_row([ "<a href='$action$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();
}

sub ui_zfs_properties
{
my ($zfs)=@_;
require './property-list-en.pl';
my %hash = zfs_get($zfs, "all");
if (!$hash{$zfs}{'com.sun:auto-snapshot'}) { $hash{$zfs}{'com.sun:auto-snapshot'}{'value'} = '-'; }
my %props =  property_desc();
my %properties = properties_list();
print ui_table_start("Properties", "width=100%", undef);
foreach $key (sort(keys %{$hash{$zfs}}))
{		
	if (($properties{$key}) || ($props{$key}))
	{		
		if ($key =~ 'origin') { print ui_table_row('<a href="property.cgi?zfs='.$zfs.'&property='.$key.'">'.$key.'</a>', "<a href='status.cgi?snap=$hash{$zfs}{$key}{value}'>$hash{$zfs}{$key}{value}</a>");
		} else { print ui_table_row('<a href="property.cgi?zfs='.$zfs.'&property='.$key.'">'.$key.'</a>', $hash{$zfs}{$key}{value}); }
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
	print ui_form_start('cmd.cgi', 'post');
	#print ui_hidden('multisnap', 1);
	print ui_hidden('cmd', 'multisnap');
	}
#if ($admin =~ /1/) { print select_all_link('snap', '', "Select All"), " | ", select_invert_link('snap', '', "Invert Selection") }
print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
my $num = 0;
foreach $key (sort(keys %snapshot))
{
	#print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	if ($admin =~ /1/) {
		print ui_columns_row([ui_checkbox("select", $key.";", "<a href='status.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
		$num ++;
	} else {
		print ui_columns_row([ "<a href='status.cgi?snap=$key'>$key</a>", $snapshot{$key}{used}, $snapshot{$key}{refer} ]);
	}
	#if ($zfs =~ undef) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	#else {
	#	if ($key =~ ($zfs."@")) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	#}
}
print ui_columns_end();
if ($admin =~ /1/) { print select_all_link('select', '', "Select All"), " | ", select_invert_link('select', '', "Invert Selection") }
if (($admin =~ /1/) && ($conf{'snap_destroy'} =~ /1/)) { print " | ".ui_submit("Destroy selected snapshots"); }
if ($admin =~ /1/) { print ui_form_end(); }

}

sub ui_create_snapshot
{
my ($zfs) = @_;
$rv = ui_form_start('cmd.cgi', 'post')."\n";
$rv .= "Create new snapshot based on filesystem: ".$zfs."<br />\n";
my $date = strftime "zfs_manager_%Y-%m-%d-%H%M", localtime;
$rv .= $zfs."@ ".ui_textbox('snap', $date, 28)."\n";
$rv .= ui_hidden('zfs', $zfs)."\n";
$rv .= ui_hidden('cmd', "snapshot")."\n";
$rv .= ui_submit("Create");
$rv .= ui_form_end();
return $rv;
}

sub ui_cmd
{
#my ($message, @result) = @_;
my ($message, $cmd) = @_;
$rv = "Attempting to $message with command... <br />\n";
$rv .= "<i># ".$cmd."</i><br /><br />\n";
if (!$in{'confirm'}) {
	$rv .= ui_form_start('cmd.cgi', 'post');
	foreach $key (keys %in) {
			$rv .= ui_hidden($key, $in{$key});
	}
	$rv .= "<h3>Would you lke to continue?</h3>\n";
	$rv .= ui_submit("yes", "confirm", 0)."<br />";
	#$rv .= ui_submit("yes", "confirm", 0, "style='background-color: transparent;border: none;color: blue;cursor: pointer;'")." | <a href='status.cgi?zfs=".$in{'zfs'}."'>no</a>";
	$rv .= ui_form_end();
	#$rv .= "confirm=".$confirm."</br>";
} else {
	@result = (`$cmd 2>&1`);
	if (!$result[0])
	{
		#$rv .= $result[1]."<br />\n";
		$rv .= "Success! <br />\n";
	} else	{
	#$result[1] =~ s/\R/ /g;
	$rv .= "<b>error: </b>".$result[0]."<br />\n";
	foreach $key (@result[1..@result]) {
		$rv .= $key."<br />\n";
	}
	#print Dumper(@result);
	}
}

return $rv;
}

sub ui_popup_link
#deprecated
{
my ($name, $url)=@_;
return "<a onClick=\"\window.open('$url', 'cmd', 'toolbar=no,menubar=no,scrollbars=yes,width=600,height=400,resizable=yes'); return false\"\ href='$url'>$name</a>";
}

sub test_function
{

}
