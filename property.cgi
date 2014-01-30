#!/usr/bin/perl

require './zfsmanager-lib.pl';
require './property-list-en.pl';
ReadParse();
use Data::Dumper;
#ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
popup_header($text{'property_title'}." ".$in{'property'}." on ".$in{'zfs'});
%conf = get_zfsmanager_config();
%props =  property_desc();
%pool_proplist = pool_properties_list();
%proplist = properties_list();

print "<h3>$text{'property_title'}: $in{'property'}</h3>";
if ($props{$in{'property'}})
{
	print $props{$in{'property'}};
	print "<br />";
	print "<br />";
}

if ($in{'zfs'}) { 
	%get = zfs_get($in{'zfs'}, $in{'property'}); 
	print "File system:  ".$in{'zfs'}."<br /> ";
	print "Property: ", $in{'property'}, " is currently: ", $get{$in{'zfs'}}{$in{'property'}}{value}, "<br />";
	print "Source: ", $get{$in{'zfs'}}{$in{'property'}}{source};
	print "<br />";
	print "<br />";
} elsif ($in{'pool'}) { 
	%get = zpool_get($in{'pool'}, $in{'property'}); 
	print "Pool:  ".$in{'pool'}."<br /> ";
	print "Property: ", $in{'property'}, " is currently: ", $get{$in{'pool'}}{$in{'property'}}{value}, "<br />";
	print "Source: ", $get{$in{'pool'}}{$in{'property'}}{source};
	print "<br />";
	print "<br />";
}

if (can_edit($in{'zfs'}, $in{'property'}) =~ 1) {
print ui_form_start('cmd.cgi', 'get');
print ui_hidden('property', $in{'property'});
print ui_hidden('zfs', $in{'zfs'});
print ui_hidden('pool', $in{'pool'});
if ($in{'property'} =~ 'mountpoint') {
	print ui_filebox('set', $get{$in{'zfs'}}{$in{'property'}}{value}, 0, undef, undef, 1);
	print ui_submit('submit'), "<br />";
} elsif ($in{'property'} =~ 'mounted') {
	if ($get{$in{'zfs'}}{$in{'property'}}{value} =~ 'yes') {
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&mount=unmount'>Unmount this file system</a>";
	} else {
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&mount=mount'>Mount this file system</a>";
	}
} elsif ($in{'property'} =~ 'sharesmb') {

} elsif ($in{'property'} =~ 'sharenfs') {

} elsif ($in{'property'} =~ 'utf8only') {

} elsif ($proplist{$in{'property'}} =~ 'special' || $pool_proplist{$in{'property'}} =~ 'special') {

} else {

if ($in{'zfs'}) { 
	my @select = [ split(", ", $proplist{$in{'property'}}), 'inherit' ];
	if ($proplist{$in{'property'}} eq 'boolean') { @select = [ 'on', 'off', 'inherit' ]; }
	print "Change to: ";
	print ui_select('set', $get{$in{'zfs'}}{$in{'property'}}{value}, @select, 1, 0, 1); 
}
elsif ($in{'pool'}) { 
	my @select = [ split(", ", $pool_proplist{$in{'property'}}) ];
	if ($pool_proplist{$in{'property'}} eq 'boolean') { @select = [ 'on', 'off' ]; }
	print ui_select('set', $get{$in{'pool'}}{$in{'property'}}{value}, @select, 1, 0, 1); 
}
print ui_submit('submit');
print "<br />";
}}

print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
popup_footer();
