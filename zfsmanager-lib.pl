BEGIN { push(@INC, ".."); };
use WebminCore;
use POSIX qw(strftime);
init_config();
foreign_require("mount", "mount-lib.pl");

sub get_zfsmanager_config
{
my $lref = &read_file_lines($config{'zfsmanager_conf'});
my @rv;
my $lnum = 0;
foreach my $line (@$lref) {
    my ($n, $v) = split(/\s+/, $line, 2);
    if ($n) {
      push(@rv, { 'name' => $n, 'value' => $v, 'line' => $lnum });
      }
    $lnum++;
    }
return @rv;
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
	if (($key =~ 'pool') || ($key =~ 'state') || ($key =~ 'scan') || ($key =~ 'errors'))
	{
		$status{pool}{$key} = $value;
	} elsif (($line =~ "config:") || ($line =~ /NAME/) || ($line =~ /status:/) || ($line =~ /action:/) || ($line =~ /see:/))
	{
		#do nothing
	} else
	{
		my($name, $state, $read, $write, $cksum) = split(" ", $line);
		if ($name =~ $status{pool}{pool})
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

sub properties_list
#return hash of properties that can be set manually and their data type
{
my ($type)=@_;
#my %list = ( 'boolean' => [ "atime", "canmount", "devices", "exec", "readonly", "setuid", "xattr" ],
#			'string' => [ "aclinherit", "aclmode", "checksum", "compression", "primarycache", "secondarycache", "shareiscsi", "sharenfs", "snapdir" ],
#			'number' => [ "copies", "quota", "recordsize", "refquota", "refreservation", "reservation", "volblocksize" ] );
my %list2 = ('atime' => 'boolean', 'canmount' => 'boolean', 'devices' => 'boolean', 'exec' => 'boolean', 'nbmand' => 'boolean', 'readonly' => 'boolean', 'setuid' => 'boolean', 'shareiscsi' => 'boolean', 'xattr' => 'boolean', 'utf8only' => 'boolean', 'vscan' => 'boolean', 'zoned' => 'boolean',
			'aclinherit' => 'discard, noallow, restricted, pasthrough, passthrough-x', 'aclmode' => 'discard, groupmaks, passthrough', 'casesensitivity' => 'sensitive, insensitive, mixed', 'checksum' => 'on, off, fletcher2, fletcher4, sha256', 'compression' => 'on, off, lzjb, gzip, gzip-1, gzip-2, gzip-3, gzip-4, gzip-5, gzip-6, gzip-7, gzip-8, gzip-9', 'copies' => '1, 2, 3', 'dedup' => 'on, off, verify, sha256', 'primarycache' => 'all, none, metadata', 'secondarycache' => 'all, none, metadata', 'snapdir' => 'hidden, visible', 'sync' => 'standard, always, disabled',   
			'mountpoint' => 'special', 'sharesmb' => 'special', 'sharenfs' => 'special', 'mounted' => 'special');
#if ($type != undef)
#{
#	return @list{$type};
#} else 
#{
return %list2;
#}
}

sub zpool_list
{
#TODO massage data into something better
my $list=`zpool list`;
return $list;
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

#cmd_snapshot($snap)
sub cmd_create_zfs
{
my ($zfs)  = @_;
my $cmd="zfs create $zfs";
@result = ($cmd, `$cmd`);
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

#cmd_zfs_set($zfs, $property $value, $confirm)
sub cmd_zfs_set
{
my ($zfs, $property, $value, $confirm) = @_;
my $cmd="zfs set $property=$value $zfs";
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
my ($zfs, $confirm) = @_;
my $cmd="zfs destroy $zfs";
if ($confirm =~ /yes/) 
	{ 
		@result = ($cmd, `$cmd`);
	} else 
	{ 
		@result = ($cmd, "" ); 
	}
return @result;
}

#cmd_destroy_zpool($zpool, $confirm)
sub cmd_destroy_zpool
{
my ($zpool, $confirm) = @_;
my $cmd="zpool destroy $zpool";
if ($confirm =~ /1/) { @result = ($cmd, `$cmd`)} else { @result = ($cmd, "" ) };
return @result;
}

sub ui_zpool_status
{
my ($pool, $action) = @_;
if ($action eq undef) { $action = "status.cgi?pool="; }
my %zpool = list_zpools($pool);
print ui_columns_start([ "Pool Name", "Size", "Alloc", "Free", "Cap", "Dedup", "Health"]);
foreach $key (sort(keys %zpool))
{
    print ui_columns_row(["<a href='$action$key'>$key</a>", $zpool{$key}{size}, $zpool{$key}{alloc}, $zpool{$key}{free}, $zpool{$key}{cap}, $zpool{$key}{dedup}, $zpool{$key}{health} ]);
}
print ui_columns_end();
}

sub ui_zpool_properties
{
my ($pool) = @_;
my %hash = zpool_get($pool, "all");
my %properties = properties_list();
print ui_table_start("Properties", "width=100%", "10");
foreach $key (sort(keys $hash{$pool}))
{
	if ($properties{$key} =~ 'boolean')
	{
		if ($hash{$in{'pool'}}{$key}{value} =~ "on") {
			print ui_table_row($key, $hash{$pool}{$key}{value});
		} else {
			print ui_table_row($key, $hash{$pool}{$key}{value});
		}
	} else {
	print ui_table_row($key, $hash{$pool}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_zfs_list
{
my ($zfs)=@_;
%zfs = list_zfs($zfs);
print ui_columns_start([ "File System", "Used", "Avail", "Refer", "Mountpoint" ]);
foreach $key (sort(keys %zfs)) 
{
	print ui_columns_row(["<a href='status.cgi?zfs=$key'>$key</a>", $zfs{$key}{used}, $zfs{$key}{avail}, $zfs{$key}{refer}, $zfs{$key}{mount} ]);
}
print ui_columns_end();
}

sub ui_zfs_properties
{
my ($zfs)=@_;
my %hash = zfs_get($zfs, "all");
my %properties = properties_list();
print ui_table_start("Properties", "width=100%", "10");
foreach $key (sort(keys $hash{$zfs}))
{		
	if ($properties{$key})
	{		
		print ui_table_row(ui_popup_link($key,'property.cgi?zfs='.$zfs.'&property='.$key), $hash{$zfs}{$key}{value});
	} else {
	print ui_table_row($key, $hash{$zfs}{$key}{value});
	}
}
print ui_table_end();
}

sub ui_list_snapshots
{
my ($zfs) = @_;
%snapshot = list_snapshots();
print ui_columns_start([ "Snapshot", "Used", "Refer" ]);
foreach $key (sort(keys %snapshot)) 
{
	if ($zfs =~ undef) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	else {
		if ($key =~ ($zfs."@")) { print ui_columns_row([ui_checkbox("snap", $key, "<a href='snapshot.cgi?snap=$key'>$key</a>"), $snapshot{$key}{used}, $snapshot{$key}{refer} ]); }
	}
} 
print ui_columns_end();

}

sub ui_create_snapshot
{
my ($zfs) = @_;
print ui_form_start('cmd.cgi', 'get');
print "Create new snapshot based on filesystem: ", $zfs, "<br />";
my $date = strftime "zfs_manager_%Y-%m-%d-%H%M", localtime;
print $zfs, "@ ", ui_textbox('snap', $date, 28);
print ui_hidden('zfs', $zfs);
#print ui_form_end(["<input type='submit' value='submit'>"]);
print popup_window_button( 'cmd.cgi', '600', '400', '1', [ [ 'snap', 'snap', 'snap'], ['zfs', 'zfs', 'zfs'] ] );
#print ui_form_end([ [popup_window_button('cmd.cgi', '400', '400', '1', [[ 'snap', 'snap', 'snap'], ['zfs', 'zfs', 'zfs']]), "submit" ]]);
}

sub ui_popup_link
{
my ($name, $url)=@_;
return "<a onClick=\"\window.open('$url', 'cmd', 'toolbar=no,menubar=no,scrollbars=yes,width=600,height=400,resizable=yes'); return false\"\ href='$url'>$name</a>";
}

sub test_function
{

}
