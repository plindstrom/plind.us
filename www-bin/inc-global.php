<?php
/*
  File Name  inc-global.php
  Project    plind.us
  Version    8.1.5
  Author     Peter Lindstrom
  Purpose    Global PHP functions utilized throughout the site.
  Copyright  2003-2020, Peter Lindstrom
  Link       https://github.com/plindstrom/plind.us

  FUNCTIONS ------------------------------------------------------------------
    1. Page_Init
       Prints html required to start the page (html, head, body).

    2. Page_End
       Stops page gen timer and prints html required to end the page 
       (/body, /html).

    3. Page_Header
       Prints html required for page header (header).

    4. Page_Footer
       Prints html required for page footer (footer).

    5. Get_CWD
       Returns the current working directory as found in the url.

    6. Get_Env
       Returns if page is running in non-prod or prod based on the url.  Can
       also use an override to force prod on a non-prod url for testing.

    7. Get_LastModified
       Returns the date and time that the current file was last modified.

    8. Get_Fact
       Returns a random fact from an array of fun(ish) facts.

    9. Get_Wx
       Returns the current weather info using data from a weather xml file.
*/


// Load ini files ------------------------------------------------------------
$iniPath = parse_ini_file("cfg-path.ini", true);


// Start timer ---------------------------------------------------------------
$mTime = microtime();
$mTime = explode(" ",$mTime);
$mTime = $mTime[1] + $mTime[0];
$tStart = $mTime;


// Page setup ----------------------------------------------------------------
function Page_Init($pgTitle){
	// Print page beginning html
	print("<!DOCTYPE HTML>\n");
	print("<html lang=\"en\">\n");
	print("<head>\n");
	print("	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n");
	print("	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1\" />\n");
	print("	<title>Peter Lindstrom"); if(strlen($pgTitle) > 0){ print(" - $pgTitle"); } print("</title>\n");
	print("	<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/global.css\" />\n");
	print("	<link rel=\"icon\" type=\"image/png\" href=\"/favicon.ico\" sizes=\"16x16 32x32\" />\n");
	print("	<script type=\"text/javascript\" src=\"/js/jquery-3.4.1.min.js\"></script>\n");
	print("	<script type=\"text/javascript\" src=\"/js/global.js\"></script>\n");
	print("	<script type=\"text/javascript\" src=\"/js/satori-1.0.1.js\"></script>\n");
	print("</head>\n");
	print("<body>\n");
}


// Page ending ---------------------------------------------------------------
function Page_End(){
	// Stop the timer and get page generation time
    global $tStart;
	$mTime = microtime();
    $mTime = explode(" ",$mTime);
    $mTime = $mTime[1] + $mTime[0];
    $tEnd = $mTime;
    $ttlTime = ($tEnd - $tStart);

    // Print page end html
	print("</body>\n");
	print("</html>\n");
	print("<!-- (c) Copyright 2003-" . date("Y") . ". -->\n");
	printf("<!-- Page generated in %f seconds. -->",$ttlTime);
}


// Page header ---------------------------------------------------------------
function Page_Header(){
	// Print page header html
	print("	<header>\n");
	print("		<h1>plind.us</h1>\n");
	print("	</header>\n");
}


// Page footer ---------------------------------------------------------------
function Page_Footer(){
	// Print page footer html
	print("	<footer>\n");
	printf("		<p class=\"align-left\">Last updated: <em>%s</em>.</p>\n",Get_LastModified());
	print("		<p class=\"align-right\"><a href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 Int'l License</a></p>\n");
	print("	</footer>\n");
}


// Get current working directory ---------------------------------------------
function Get_CWD(){
	// Get the current working directory
	$cwd = explode("/", getcwd());
	$cwd = $cwd[4];
	
	// Return the current working directory
	return $cwd;
}


// Get environment -----------------------------------------------------------
function Get_Env(){
	// Get the current environment from the url (dev. or test.)
	$curUrl = $_SERVER['HTTP_HOST'];
	$curEnv = explode(".", $curUrl);

	// Get an override value if one is set
	$override = $_GET['env'];

	// Set to www if override exists on dev or test otherwise set to env
	if($curEnv[0] == "dev" || $curEnv[0] == "test"){
		if($override == "www"){
			$reqEnv = "www";
		} else {
			$reqEnv = $curEnv[0];
		}
	} else {
		$reqEnv = "www";
	}
	
	// Return the environment (dev | test | www)
	return $reqEnv;
}


// Get last modified ---------------------------------------------------------
function Get_LastModified(){
	// Check if that file exists and get the mod date
	global $iniPath;
	$fn = $iniPath[host][basepath] . Get_Env() . $_SERVER['SCRIPT_NAME'];
	if(file_exists($fn)){
		$modTime = date("F d Y H:i:s", filemtime($fn));
	} else {
		$modTime = "Not really sure";
	}

	// Return the modified date
	return $modTime;
}


// Get fact ------------------------------------------------------------------
function Get_Fact(){
	// Add the fun facts to the array
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
	
	// Return a random fact
	return $facts[rand(0,10)];
}


// Get wx from xml -----------------------------------------------------------
function Get_Wx(){
	// Parse weather xml file
	global $iniPath;
	$wx = simplexml_load_file($iniPath[weather][xmlpath]) or die("Error: Cannot retrieve the weather.");
	$weather = $wx->weather;
	$temp_f = $wx->temp_f;
	
	// Format output and return
	$output = "${temp_f}&deg; F, ${weather}";
	return $output;
}