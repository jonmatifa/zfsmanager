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
    $hash{$name} = [ $size, $alloc, $free, $cap, $dedup, $health, $altroot ];
}
return %hash;
}

sub list_zfs
{
#zfs list
my @table=();
my %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list`;

open my $fh, "<", \$list;
my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $used, $avail, $refer, $mount) = split(" ", $line);
    $hash{$name} = [ $used, $avail, $refer, $mount ];
}
return %hash;
}

sub list_snapshots
{
#zfs list -t snapshot
my @table=();
my %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list -t snapshot`;

open my $fh, "<", \$list;
my @table = split("", $firstline=<$fh>);
while (my $line =<$fh>)
{
    chomp ($line);
    my($name, $used, $avail, $refer, $mount) = split(" ", $line);
    $hash{$name} = [ $used, $avail, $refer, $mount ];
}
return %hash;
}

#zpool_status($pool)
sub zpool_status
{
my ($pool)=@_;
my @table=();
#my %hash=();
my $count=0;
#my $junk=();
my $status=`zpool status $pool`;
open my $fh, "<", \$status;
while (my $line =<$fh>)
{
    chomp ($line);
	if ($count == 0) 
	{
		local($junk, $hash{ 'pool' }) = split(": ", $line);
	}
	if ($count == 1) 
	{
		local($junk, $hash{ 'state' }) = split(": ", $line);
	}
	if ($count == 2) 
	{
		local($junk, $hash{ 'scan' }) = split(": ", $line);
	}
	if ($count == 3 || $count == 4 || $count == 5) 
	{
		$junk = <$fh>;
	}
	$count++;
    my($name, $state, $read, $write, $cksum) = split(" ", $line);
    $hash{ 'config' } = [ $name, $state, $read, $write, $cksum ];
}

return $status;
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

sub test_function
{
my ($pool)=@_;
my $parent = "pool";
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
	} elsif (($line =~ "config:") || ($line =~ /NAME/))
	{
		#do nothing
	} else
	{
		my($name, $state, $read, $write, $cksum) = split(" ", $line);
		#$name =~ s/^\s*(.*?)\s*$/$1/;
		#$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum};
		#$devs++;
		#check if vdev is the pool itself
		
		if ($name =~ $status{pool}{pool})
		{
			$status{pool}{name} = $name;
			$status{pool}{read} = $read;
			$status{pool}{write} = $write;
			$status{pool}{cksum} = $cksum;
			
		#check if vdev is a mirror, raid, log or cache vdev
		} elsif (($name =~ /mirror/) || ($name =~ /raidz/) || ($name =~ /log/) || ($name =~ /cache/))
		{
			$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
			$parent = $name;
			$devs++;
		
		#for all other vdevs, should be actual devices at this point
		} elsif ($name)
		{
			$status{$devs} = {name => $name, state => $state, read => $read, write => $write, cksum => $cksum, parent => $parent};
			#$status{$devs}{name} = $name;
			#$status{$devs}{state} = $state;
			#$status{$devs}{read} = $read;
			#$status{$devs}{write} = $write;
			#$status{$devs}{cksum} = $cksum;
			#$status{$devs}{parent} = $parent;
			#$status{$devs}{data} = "fucking hell";
			$devs++;
		}
	}
}
return %status;
}
