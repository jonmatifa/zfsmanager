BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

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
#zpool list
#my @table=();
my %hash=();
#expecting NAME SIZE ALLOC FREE CAP DEDUP HEALTH ALTROOT
$list=`zpool list -H`;

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
#zfs list -t snapshot
#my @table=();
my %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list -t snapshot -H`;

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
	} elsif (($line =~ "config:") || ($line =~ /NAME/) || ($line =~ /status/) || ($line =~ /action/))
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

		} elsif (($name =~ /mirror/) || ($name =~ /raidz/))
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
my $get=`zfs get $zfs $property`;
return `zfs get $property $zfs`;
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

sub test_function
{
#zpool list
my @table=();
my %hash=();
#expecting NAME SIZE ALLOC FREE CAP DEDUP HEALTH ALTROOT
$list=`zpool list`;

open my $fh, "<", \$list;
my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $size, $alloc, $free, $cap, $dedup, $health, $altroot) = split(" ", $line);
    #$hash{$name} = [ $size, $alloc, $free, $cap, $dedup, $health, $altroot ];
	$hash{$name} = { size => $size, alloc => $alloc, free => $free, cap => $cap, dedup => $dedup, health => $health, altroot => $altroot };
}
return %hash;
}
