# cpan File::Slurp
use File::Slurp;
# this script extracts all messages by a particular user from VkOpt's message history and separates them with delimiter 
# customize these variables!
my $input_file = read_file("messagehistory.html");
my $username = "Your Name";
my $delimiter = "<delimiter>";
my $output_file = "whatever.html";
###########################

my $messages_from_user = "";
my $i = 0;
while ($input_file =~ /<div id="msg\d+?" class="msg_item">.*?<div class="from"> <b>$username<\/b>.*?<div class="msg_body">(.*?)<\/div>/g){
	# print progress
	$i++;
	if ($i % 1000 == 0) {
		print "$i messages found\n";
	}
	
	$msg = $1;
	$msg =~ s/<img class="emoji".*?alt="(.*?)">/\1/g;
	$msg =~ s/<a href=.*?>(.*?)<\/a>/\1/g;
	$msg =~ s/<br \/>/\n/g;
	$msg =~ s/&quot;/"/g;
	$msg =~ s/&gt;/>/g;
	$msg =~ s/&lt;/</g;
	$msg =~ s/&amp;/&/g;
	$messages_from_user .= $msg . $delimiter;
}
print "Total: $i messages found\n";
write_file($output_file, $messages_from_user);
