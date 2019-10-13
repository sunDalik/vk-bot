# cpan File::Slurp
use File::Slurp;
# this script extracts all messages by a particular user from VkOpt's message history and separates them with delimiter 
# customize these variables!
my $input_file = read_file("messagehistory.html");
my $username = "Your name";
my $delimiter = "<delimiter>";
my $output_file = "whatever.html";
###########################

my $messages_from_user = "";
my $i = 0;
while ($input_file =~ /<div.*?class="msg_item">.*?<div class="from">.*?<b>$username<\/b>.*?<div class="msg_body">(.*?)<\/div>/g){
	# print progress
	$i++;
	if ($i % 100 == 0) {
		print "$i\n";
	}
	
	$msg = $1;
	$msg =~ s/<img class="emoji".*?alt="(.*?)">/\1/g;
	$messages_from_user .= $msg . "<delimiter>";
}
write_file($output_file, $messages_from_user);
