<html>
	<head>
		<title>Trick or Treat</title>
	</head>
	<body>
		<?php
    		exec('python /var/www/octoalert/halloween.py', $output);
			var_dump($output);
		?>
		<p>Halloween</p>
	</body>
</html>
