#!/usr/bin/perl

require './zfsmanager-lib.pl';
require './property-list-en.pl';
ReadParse();
use Data::Dumper;
#ui_print_header(undef, $text{'cmd_title'}, "", undef, 1, 1);
popup_header($text{'property_title'}." ".$in{'property'}." on ".$in{'zfs'});
$conf = get_zfsmanager_config();
%props =  property_desc();

print "<h3>$text{'property_title'}: $in{'property'}</h3>";
if ($props{$in{'property'}})
{
	print $props{$in{'property'}};
	print "<br />";
	print "<br />";
}

%get = zfs_get($in{'zfs'}, $in{'property'});
print "File system:  ".$in{'zfs'}."<br /> ";
print "Property: ", $in{'property'}, " is currently set to: ", $get{$in{'zfs'}}{$in{'property'}}{value}, "<br />";
print "Source: ", $get{$in{'zfs'}}{$in{'property'}}{source};
print "<br />";
print "<br />";
print ui_form_start('cmd.cgi', 'get');
print ui_hidden('property', $in{'property'});
print ui_hidden('zfs', $in{'zfs'});
if ($in{'property'} =~ 'mountpoint') {
	print ui_filebox('set', $get{$in{'zfs'}}{$in{'property'}}{value}, 0, undef, undef, 1);
	print ui_submit('submit');
} elsif ($in{'property'} =~ 'sharenfs') {
	
} elsif ($in{'property'} =~ 'mounted') {
	if ($get{$in{'zfs'}}{$in{'property'}}{value} =~ 'yes') {
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&mount=unmount'>Unmount this file system</a>";
	} else {
		print "<a href='cmd.cgi?zfs=$in{'zfs'}&mount=mount'>Mount this file system</a>";
	}
} elsif ($in{'property'} =~ 'sharesmb') {

} else {
my %proplist = properties_list();
#print Dumper(\%proplist);
#print "<br />";
#print $proplist{$in{'property'}};
my @select = [ split(", ", $proplist{$in{'property'}}) ];
if ($proplist{$in{'property'}} eq 'boolean') { @select = [ 'on', 'off' ]; }
#print Dumper (@select);
#my @select = [[['1', '2'], ['1', '2']]];
print "Change to: ";
print ui_select('set', $get{$in{'zfs'}}{$in{'property'}}{value}, @select, 1, 0, 1);
print ui_submit('submit');
}

print "<br />";
print "<a onClick=\"\window.close('cmd')\"\ href=''>Cancel</a>";
popup_footer();