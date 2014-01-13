#!/usr/bin/perl

require './zfsmanager-lib.pl';
ReadParse();
ui_print_header(undef, $text{'status_title'}, "", undef, 1, 1);

if ($in{'pool'})
{
print zpool_status($in{'pool'});
}
if ($in{'zfs'})
{
print zfs_get($in{'zfs'}, "all");
}
if ($in{'snapshot'})
{
print snapshot_status($in{'snapshot'});
}

$conf = get_zfsmanager_config();

ui_print_footer('', $text{'index_return'});