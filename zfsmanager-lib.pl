BEGIN { push(@INC, ".."); };
use WebminCore;
use POSIX qw(strftime);
init_config();
foreign_require("mount", "mount-lib.pl");
my %access = &get_module_acl();

sub properties_list
#return hash of properties that can be set manually and their data type
{
my %list = ('atime' => 'boolean', 'devices' => 'boolean', 'exec' => 'boolean', 'nbmand' => 'boolean', 'readonly' => 'boolean', 'setuid' => 'boolean', 'shareiscsi' => 'boolean', 'utf8only' => 'boolean', 'vscan' => 'boolean', 'zoned' => 'boolean', 'relatime' => 'boolean', 'overlay' => 'boolean',
			'aclinherit' => 'discard, noallow, restricted, passthrough, passthrough-x', 'aclmode' => 'discard, groupmaks, passthrough', 'casesensitivity' => 'sensitive, insensitive, mixed', 'checksum' => 'on, off, fletcher2, fletcher4, sha256', 'compression' => 'on, off, lzjb, lz4, gzip, gzip-1, gzip-2, gzip-3, gzip-4, gzip-5, gzip-6, gzip-7, gzip-8, gzip-9, zle', 'copies' => '1, 2, 3', 'dedup' => 'on, off, verify, sha256', 'logbias' => 'latency, throughput', 'normalization' => 'none, formC, formD, formKC, formKD', 'primarycache' => 'all, none, metadata', 'secondarycache' => 'all, none, metadata', 'snapdir' => 'hidden, visible', 'snapdev' => 'hidden, visible', 'sync' => 'standard, always, disabled', 'xattr' => 'on, off, sa', 'com.sun:auto-snapshot' => 'true, false', 'acltype' => 'noacl, posixacl', 'redundant_metadata' => 'all, most', 'recordsize' => '512, 1K, 2K, 4K, 8K, 16K, 32K, 64K, 128K, 256K, 512K, 1M', 'canmount' => 'on, off, noauto',
			'quota' => 'text', 'refquota' => 'text', 'reservation' => 'text', 'refreservation' => 'text', 'volsize' => 'text', 'filesystem_limit' => 'text', 'snapshot_limit' => 'text', 
			'mountpoint' => 'special', 'sharesmb' => 'special', 'sharenfs' => 'special', 'mounted' => 'special', 'context' => 'special', 'defcontext' => 'special', 'fscontext' => 'special', 'rootcontext' => 'special');
return %list;
}

sub pool_properties_list
{
my %list = ('autoexpand' => 'boolean', 'autoreplace' => 'boolean', 'delegation' => 'boolean', 'listsnapshots' => 'boolean', 
			'failmode' => 'wait, continue, panic', 'feature@async_destroy' => 'enabled, disabled', 'feature@empty_bpobj' => 'enabled, disabled', 'feature@lz4_compress' => 'enabled, disabled', 'feature@embedded_data' => 'enabled, disabled', 'feature@enabled_txg' => 'enabled, disabled', 'feature@bookmarks' => 'enabled, disabled', 'feature@hole_birth' => 'enabled, disabled', 'feature@spacemap_histogram' => 'enabled, disabled', 'feature@extensible_dataset' => 'enabled, disabled', 'feature@large_blocks' => 'enabled, disabled', 'feature@filesystem_limits' => 'enabled, disabled',
			'altroot' => 'special', 'bootfs' => 'special', 'cachefile' => 'special', 'comment' => 'special');
return %list;
}

sub create_opts #options and defaults when creating new pool or filesystem
{
my %list = ( 'atime' => 'on', 'compression' => 'off', 'canmount' => 'on', 'dedup' => 'off', 'exec' => 'on', 'readonly' => 'off', 'utf8only' => 'off', 'xattr' => 'on' );
return %list;
}

sub get_zfsmanager_config
{
my $lref = &read_file_lines($module_config_file);
my %rv;
my $lnum = 0;
foreach my $line (@$lref) {
    my ($n, $v) = split(/=/, $line, 2);
    if ($n) {
	  $rv{$n} = $v;
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
elsif ((($zfs_props{$property}) && ($config{'zfs_properties'} =~ /1/)) || (($pool_props{$property}) && ($config{'pool_properties'} =~ /1/))) { return 1; }
}

sub list_zpools
{
my ($pool) = @_;
my %hash=();
$list=`zpool list -H -o name,$config{'list_zpool'} $pool`;

open my $fh, "<", \$list;
while (my $line =<$fh>)
{
    chomp ($line);
	my @props = split(" ", $line);
        $ct = 1;
        foreach $prop (split(",", $config{'list_zpool'})) {
                $hash{$props[0]}{$prop} = $props[$ct];
                $ct++;
        }

}
return %hash;
}

sub list_zfs
{
#zfs list
my ($zfs) = @_;
my %hash=();
$list=`zfs list -H -o name,$config{'list_zfs'} $zfs`;

open my $fh, "<", \$list;
while (my $line =<$fh>)
{
	chomp ($line);
	my @props = split(" ", $line);
	$ct = 1;
	foreach $prop (split(",", $config{'list_zfs'})) { 
		$hash{$props[0]}{$prop} = $props[$ct];
		$ct++;
	}
}
return %hash;
}

sub list_snapshots
{
my ($snap) = @_;
$list=`zfs list -t snapshot -H -o name,$config{'list_snap'} -s creation $snap`;
$idx = 0;
open my $fh, "<", \$list;
while (my $line =<$fh>)
{
    chomp ($line);
    my @props = split("\x09", $line);
    $ct = 0;
    foreach $prop (split(",", "name,".$config{'list_snap'})) {
	    $hash{sprintf("%05d", $idx)}{$prop} = $props[$ct];
            $ct++;
    }
    $idx++;
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
		%zstat = zpool_status($key);
		$out .= "pool \'".$key."\' is ".$zstat{0}{state}." with ".$zstat{0}{errors}."<br />";
		if ($zstat{0}{status}) { $out .= "status: ".$zstat{0}{status}."<br />"; }
		$out .= "<br />";
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
		$parent = $devs;
		$devs++;
		
	#check if vdev is a log or cache vdev
	} elsif (($name =~ /mirror/) || ($name =~ /raidz/) || ($name =~ /spare/))
	{
		$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
		$parent = $devs;
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
my $get=`zfs get -H $property $zfs`;
open my $fh, "<", \$get;
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
my $get=`zpool get -H $property $pool`;

open my $fh, "<", \$get;
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
my $cmd = `zpool import $dir $destoryed`;
$count = 0;
@pools = split(/  pool: /, $cmd);
shift (@pools);
foreach $cmdout (@pools) {
	($status{$count}{pool}, $cmdout) = split(/ id: /, $cmdout);
	chomp $status{$count}{pool};
	($status{$count}{id}, $cmdout) = split(/ state: /, $cmdout);
	chomp $status{$count}{id};
	if (index($cmdout, "status: ") != -1) { 
		($status{$count}{state}, $cmdout) = split("status: ", $cmdout); 
		($status{$count}{status}, $cmdout) = split("action: ", $cmdout); 
		if (index($cmdout, "  see: ") != -1) { 
			($status{$count}{action}, $cmdout) = split("  see: ", $cmdout); 
			($status{$count}{see}, $cmdout) = split("config:\n", $cmdout); 
		} else { ($status{$count}{action}, $cmdout) = split("config:\n", $cmdout); }
	} else {
		($status{$count}{state}, $cmdout) = split("action: ", $cmdout); 
		($status{$count}{action}, $cmdout) = split("config:\n", $cmdout);
	}
	$status{$count}{config} = $cmdout;
$count++;
}
return %status;
}

sub diff
{
my ($snap, $parent) = @_;
my @array = split("\n", `zfs diff -FH $snap`);
return @array;
}


sub list_disk_ids
{
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
return $cmd;
}

sub cmd_create_zpool
#deprecated
{
my ($pool, $dev, $options, $poolopts, $force) = @_;
my $opts = ();
foreach $key (sort(keys %{$poolopts}))
{
	$opts = (${$poolopts}{$key} =~ 'default') ? $opts : $opts.' -o '.$key.'='.${$poolopts}{$key};
}
foreach $key (sort(keys %{$options}))
{
	$opts = (${$options}{$key} =~ 'default') ? $opts : $opts.' -O '.$key.'='.${$options}{$key};
}
my $cmd="zpool create $force $opts $pool $dev";
return $cmd;
}

sub find_parent
{
my ($filesystem) = @_;
my %parent = ();
($parent{'pool'}) = split(/[@\/]/g, $filesystem);
$null = reverse $filesystem =~ /[@\/]/g;
$parent{'filesystem'} = substr $filesystem, 0, $-[0];
return %parent;
}

sub ui_zpool_list
{
my ($pool, $action)=@_;
my %zpool = list_zpools($pool);
if ($action eq undef) { $action = "status.cgi?pool="; }
@props = split(/,/, $config{list_zpool});
print ui_columns_start([ "pool name", @props ]);
foreach $key (sort(keys %zpool))
{
     @vals = ();
     foreach $prop (@props) { push (@vals, $zpool{$key}{$prop}); }
     print ui_columns_row(["<a href='$action$key'>$key</a>", @vals ]);
}
print ui_columns_end();
}

sub ui_zpool_status
#deprecated
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
	if (($properties{$key}) || ($props{$key}) || ($text{'prop_'.$key}))
	{
		print ui_table_row('<a href="property.cgi?pool='.$pool.'&property='.$key.'">'.$key.'</a>', $hash{$pool}{$key}{value});
	} else {
	print ui_table_row($key, $hash{$pool}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_zfs_list
{
my ($zfs, $action)=@_;
my %zfs = list_zfs($zfs);
if ($action eq undef) { $action = "status.cgi?zfs="; }
@props = split(/,/, $config{list_zfs});
print ui_columns_start([ "file system", @props ]);
foreach $key (sort(keys %zfs)) 
{
	@vals = ();
	if ($zfs{$key}{'mountpoint'}) { $zfs{$key}{'mountpoint'} = "<a href='../filemin/index.cgi?path=".urlize($zfs{$key}{mountpoint})."'>$zfs{$key}{mountpoint}</a>"; }
	foreach $prop (@props) { push (@vals, $zfs{$key}{$prop}); }
    	print ui_columns_row(["<a href='$action$key'>$key</a>", @vals ]);
}
print ui_columns_end();
}

sub ui_zfs_properties
{
my ($zfs)=@_;
require './property-list-en.pl';
my %hash = zfs_get($zfs, "all");
if (!$hash{$zfs}{'com.sun:auto-snapshot'}) { $hash{$zfs}{'com.sun:auto-snapshot'}{'value'} = '-'; }
my %props = property_desc();
my %properties = properties_list();
print ui_table_start("Properties", "width=100%", undef);
foreach $key (sort(keys %{$hash{$zfs}}))
{		
	if (($properties{$key}) || ($props{$key}) || ($text{'prop_'.$key}))
	{		
		if ($key =~ 'origin') { print ui_table_row('<a href="property.cgi?zfs='.$zfs.'&property='.$key.'">'.$key.'</a>', "<a href='status.cgi?snap=$hash{$zfs}{$key}{value}'>$hash{$zfs}{$key}{value}</a>"); }
		elsif ($key =~ 'clones') { 
			$row = "";
			@clones = split(',', $hash{$zfs}{$key}{value});
			foreach $clone (@clones) { $row .= "<a href='status.cgi?zfs=$clone'>$clone</a> "; }
			print ui_table_row('<a href="property.cgi?zfs='.$zfs.'&property='.$key.'">'.$key.'</a>', $row);
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
@props = split(/,/, $config{list_snap});
if ($admin =~ /1/) { 
	print ui_form_start('cmd.cgi', 'post');
	print ui_hidden('cmd', 'multisnap');
	}
print ui_columns_start([ "snapshot", @props ]);
my $num = 0;
foreach $key (sort(keys %snapshot))
{
	@vals = ();
	foreach $prop (@props) { push (@vals, $snapshot{$key}{$prop}); }
	if ($admin =~ /1/) {
		print ui_columns_row([ui_checkbox("select", $snapshot{$key}{name}.";", "<a href='status.cgi?snap=$snapshot{$key}{'name'}'>$snapshot{$key}{'name'}</a>"), @vals ]);
		$num ++;
	} else {
		print ui_columns_row([ "<a href='status.cgi?snap=$snapshot{$key}{name}'>$snapshot{$key}{name}</a>", @vals ]);
	}
}
print ui_columns_end();
if ($admin =~ /1/) { print select_all_link('select', '', "Select All"), " | ", select_invert_link('select', '', "Invert Selection") }
if (($admin =~ /1/) && ($config{'snap_destroy'} =~ /1/)) { print " | ".ui_submit("Destroy selected snapshots"); }
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
my ($message, $cmd) = @_;
print "$text{'cmd_'.$in{'cmd'}} $message $text{'cmd_with'}<br />\n";
print "<i># ".$cmd."</i><br /><br />\n";
if (!$in{'confirm'}) {
	print ui_form_start('cmd.cgi', 'post');
	foreach $key (keys %in) {
		print ui_hidden($key, $in{$key});
	}
	print "<h3>Would you lke to continue?</h3>\n";
	print ui_submit("yes", "confirm", 0)."<br />";
	print ui_form_end();
} else {
	@result = (`$cmd 2>&1`);
	if (!$result[0])
	{
		print "Success! <br />\n";
	} else	{
	print "<b>error: </b>".$result[0]."<br />\n";
	foreach $key (@result[1..@result]) {
		print $key."<br />\n";
	}
	}
}
print "<br />";
}

sub ui_cmd_old
{
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
        $rv .= ui_form_end();
} else {
        @result = (`$cmd 2>&1`);
        if (!$result[0])
        {
                $rv .= "Success! <br />\n";
        } else  {
        $rv .= "<b>error: </b>".$result[0]."<br />\n";
        foreach $key (@result[1..@result]) {
                $rv .= $key."<br />\n";
        }
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
