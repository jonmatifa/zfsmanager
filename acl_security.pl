
require 'zfsmanager-lib.pl';

# acl_security_form(&options)
sub acl_security_form
{
my ($access)=@_;

print ui_table_row("Desctructive pool features",
  ui_yesno_radio("upool_destroy", $access->{'upool_destroy'}));
print ui_table_row("Desctructive file system features",
  ui_yesno_radio("uzfs_destroy", $access->{'uzfs_destroy'}));
print ui_table_row("Desctructive snapshot features",
  ui_yesno_radio("usnap_destroy", $access->{'usnap_destroy'}));
print ui_table_row("Pool property administration",
  ui_yesno_radio("upool_properties", $access->{'upool_properties'}));
print ui_table_row("File system property administration",
  ui_yesno_radio("uzfs_properties", $access->{'uzfs_properties'}));

}

sub acl_security_save
{
my ($access, $in) = @_;
$access->{'upool_destroy'} = $in->{'upool_destroy'};
$access->{'uzfs_destroy'} = $in->{'uzfs_destroy'};
$access->{'usnap_destroy'} = $in->{'usnap_destroy'};
$access->{'upool_properties'} = $in->{'upool_properties'};
$access->{'uzfs_properties'} = $in->{'uzfs_properties'};
}
