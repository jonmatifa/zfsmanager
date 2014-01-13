=head1 foobar-lib.pl

Functions for managing the Foobar webserver configuration file.

  foreign_require("zfsmanager", "zfsmanager-lib.pl");
  @sites = zfsmanager::list_foobar_websites()

=cut

BEGIN { push(@INC, ".."); };
use WebminCore;
init_config();

=head2 get_foobar_config()

Returns the Foobar Webserver configuration as a list of hash references with name and value keys.

=cut

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
local @table=();
local %hash=();
#expecting NAME SIZE ALLOC FREE CAP DEDUP HEALTH ALTROOT
$list=`zpool list`;

open local $fh, "<", \$list;
local @table = split("", $firstline=<$fh>);
while (local $line =<$fh>)
{
    chomp ($line);
    local($name, $size, $alloc, $free, $cap, $dedup, $health, $altroot) = split(" ", $line);
    $hash{$name} = [ $size, $alloc, $free, $cap, $dedup, $health, $altroot ];
}
return %hash;
}

sub list_zfs
{
#zfs list
local @table=();
local %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list`;

open local $fh, "<", \$list;
local @table = split("", $firstline=<$fh>);
while (local $line =<$fh>)
{
    chomp ($line);
    local($name, $used, $avail, $refer, $mount) = split(" ", $line);
    $hash{$name} = [ $used, $avail, $refer, $mount ];
}
return %hash;
}

sub list_snapshots
{
#zfs list -t snapshot
local @table=();
local %hash=();
#expecting NAME USED AVAIL REFER MOUNTPOINT
$list=`zfs list -t snapshot`;

open local $fh, "<", \$list;
local @table = split("", $firstline=<$fh>);
while (local $line =<$fh>)
{
    chomp ($line);
    local($name, $used, $avail, $refer, $mount) = split(" ", $line);
    $hash{$name} = [ $used, $avail, $refer, $mount ];
}
return %hash;
}

#zpool_status($pool)
sub zpool_status
{
local ($pool)=@_;
local @table=();
local %hash=();
local $count=0;
local $junk=();
local $status=`zpool status $pool`;
open local $fh, "<", \$status;
while (local $line =<$fh>)
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
		local $junk = <$fh>;
	}
	$count++;
    local($name, $state, $read, $write, $cksum) = split(" ", $line);
    $hash{ 'config' } = [ $name, $state, $read, $write, $cksum ];
}

return $status;
}

#zfs_get($pool, $property)
sub zfs_get
{
local ($zfs, $property) = @_;
local $get=`zfs get $zfs $property`;
return `zfs get $property $zfs`;
}

sub zpool_list
{
#TODO massage data into something better
local $list=`zpool list`;
return $list;
}



