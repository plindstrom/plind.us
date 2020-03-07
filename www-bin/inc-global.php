<?php
/*
  File Name  inc-global.php
  Project    plind.us
  Version    8.1.3
  Author     Peter Lindstrom
  Purpose    Global PHP functions utilized throughout the site.
  Copyright  2003-2020, Peter Lindstrom
  Link       https://github.com/plindstrom/plind.us
*/

// Start timer ------------------------------------
$mTime = microtime();
$mTime = explode(" ",$mTime);
$mTime = $mTime[1] + $mTime[0];
$tStart = $mTime;


// Setup page -------------------------------------
function Setup_Page(){
}


// Page setup -------------------------------------
function Page_Init($pgTitle){
	print("<!DOCTYPE HTML>\n");
	print("<html lang=\"en\">\n");
	print("<head>\n");
	print("	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n");
	print("	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1\" />\n");
	print("	<title>Peter Lindstrom"); if(strlen($pgTitle) > 0){ print(" - $pgTitle"); } print("</title>\n");
	print("	<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/global.css\" />\n");
	print("	<script type=\"text/javascript\" src=\"/js/jquery-3.4.1.min.js\"></script>\n");
	print("	<script type=\"text/javascript\" src=\"/js/global.js\"></script>\n");
	print("	<script type=\"text/javascript\" src=\"/js/satori-1.0.1.js\"></script>\n");
	print("</head>\n");
}


// Page ending ------------------------------------
function Page_End(){
	// Stop the timer and get page generation time
    global $tStart;
	$mTime = microtime();
    $mTime = explode(" ",$mTime);
    $mTime = $mTime[1] + $mTime[0];
    $tEnd = $mTime;
    $ttlTime = ($tEnd - $tStart);
	print("</body>\n");
	print("</html>\n");
	printf("<!-- Page generated in %f seconds. -->",$ttlTime);
}


// Page header ------------------------------------
function Page_Header(){
	print("<body>\n");
	print("	<header>\n");
	print("		<h1>plind.us</h1>\n");
	print("	</header>\n");
}


// Page footer ------------------------------------
function Page_Footer(){
	print("	<footer>\n");
	print("	</footer>\n");
}


// Get current working directory -----------------
function Get_CWD(){
	$cwd = explode("/", getcwd());
	$cwd = $cwd[4];
	
	return $cwd;
}


// Get environment -------------------------------
function Get_Env(){
	$curUrl = $_SERVER['HTTP_HOST'];
	$curEnv = explode(".", $curUrl);
	$override = $_GET['runAs'];

	if($curEnv[0] == "dev" || $curEnv[0] == "test"){
		if($override == "prod"){
			$envProd = true;
		} else {
			$envProd = false;
		}
	} else {
		$envProd = true;
	}
	
	return $envProd;
}


// Get fact -------------------------------------
function Get_Fact(){
	$facts = array(
		"the average cost of a car was $6,116.00",
		"a Superbowl commercial cost $400,000",
		"Lotus 1-2-3 was released for the first time",
		"the first PC-compatible mouse was released",
		"Swatch introduced their first watches",
		"McNuggets became available nationwide",
		"the average cost of a new home was $82,600",
		"the world population was estimated to be 4.72 billion",
		"Microsoft Word was released for the first time",
		"the space shuttle Challenger went on its first flight",
		"IBM released the PC XT with 128KB of RAM"
	);
	
	return $facts[rand(0,10)];
}


// Output weather information from XML ----------
function Get_Wx(){
	// Load config from ini file
	$cfg = parse_ini_file("cfg-path.ini", true);

	// Parse weather xml file
	$wx = simplexml_load_file($cfg[weather][xmlpath]) or die("Error: Cannot retrieve the weather.");
	$weather = $wx->weather;
	$temp_f = $wx->temp_f;
	
	// Format output and return
	$output = "${temp_f}&deg; F, ${weather}";
	return $output;
}