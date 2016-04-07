<?php
header('Content-type: text/plain; charset=utf-8');

function DBConnect(){
	/* 	
		Setup mysqli connection to atdove database
		RETURN: mysqli object
	 */
	$db = new mysqli('127.0.0.1','baseball','baseball');
	if($db->connect_errno > 0){
		die('Unable to connect to database [' . $db->connect_error . ']');
	}
	return $db;
}

function getFGKey($retroKey, $db){
	$sql = "SELECT key_fangraphs FROM baseball.people WHERE people.key_retro = '{$retroKey}' LIMIT 1";
	if(!$result = $db->query($sql)) die('There was an error running the sql query [' . $db->error . ']');
	if($row = $result->fetch_assoc()) {
		return $row['key_fangraphs'];
	}
	else return "";
}

function getWarG($fg, $table, $year, $db){
	$sql = "SELECT warg FROM {$table} WHERE playerid = '{$fg}' AND year = '{$year}' LIMIT 1";
	if(!$result = $db->query($sql)) die('There was an error running the sql query [' . $db->error . ']');
	if($row = $result->fetch_assoc()) {
		return $row['warg'];
	}
	else return "";
}

function printHead() {
	echo '"line","year","date","vteam","hteam","vscore","hscore","ballpark",';
	echo '"vpitcher","vpitcherWarG","hpitcher","hpitcherWarG",';
    for ($x = 1; $x <= 9; $x++) {
		echo '"vbatter'.$x.'",';
		echo '"vbatter'.$x.'WarG",';
	} 
	for ($x = 1; $x <= 9; $x++) {
		echo '"hbatter'.$x.'",';
		echo '"hbatter'.$x.'WarG"';
		if($x != 9) echo ",";
	} 

	echo "\n";
}

function printLine($array){
	/* Prints the array as a delimited line. */
	$qual = "\"";
	$len = count($array, 0)-1;
	foreach($array as $key => $val){
		if ($val != "") echo "{$qual}" . str_replace('"', "'", $val) . "{$qual}";
		else echo "{$qual}unknown{$qual}";
		
		if ($len > $key) echo ",";
	}
	echo "\n";
}

$db = DBConnect();

$sql = "SELECT * FROM baseball.mlb_2000_2015";
if(!$result = $db->query($sql)) die('There was an error running the sql query [' . $db->error . ']');

$btable = 'baseball.war_history_batters';
$ptable = 'baseball.war_history_pitchers';
printHead();
$linenum = 1;
while($row = $result->fetch_assoc()){
	$year = $row['year'];
	$vpitcher = getFGKey($row['vpitcher'], $db);
	$vpitcherwarg = getWarG($vpitcher, $ptable, $row['year'], $db);
	$hpitcher = getFGKey($row['hpitcher'], $db);
	$hpitcherwarg = getWarG($hpitcher, $ptable, $row['year'], $db);
	$vbatters = array();
	$hbatters = array();
	for ($x = 1; $x <= 9; $x++) {
		$batter = "vbatter".$x;
		$batterFG = getFGKey($row[$batter], $db);
		$vbatters[$batter] = getWarG($batterFG, $btable, $row['year'], $db); 
		$batter = "hbatter".$x;
		$batterFG = getFGKey($row[$batter], $db);
		$hbatters[$batter] = getWarG($batterFG, $btable, $row['year'], $db); 
	} 
	/* Debug code
	var_dump($vbatters);
	var_dump($hbatters);
	*/
		
	$line = array($linenum ,$year, $row['date'], $row['vteam'], $row['hteam'], $row['vscore'], $row['hscore'],
					$row['ballpark'], $row['vpitcher'], $vpitcherwarg, $row['hpitcher'], $hpitcherwarg);
				
	
	for ($x = 1; $x <= 9; $x++) {
		$batter = "vbatter".$x;
		array_push($line, $row[$batter]);
		array_push($line, $vbatters[$batter]);
	} 	
	for ($x = 1; $x <= 9; $x++) {
		$batter = "hbatter".$x;
		array_push($line, $row[$batter]);
		array_push($line, $hbatters[$batter]);
	} 
								
	printLine($line);
	$linenum++;
}

$db->close();
