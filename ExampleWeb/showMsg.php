<?php
	header('Access-Control-Allow-Origin: *');

	$conn=mysqli_connect("localhost","root","","example_web");
	mysqli_query($conn,"set names utf8");

    $sql = "SELECT * FROM `message`";
    $send = mysqli_query($conn, $sql);
        
    $rs = mysqli_fetch_row($send);
    $num = mysqli_num_rows($send);
    $json_arr =array();

    for($i = 0;$i<$num;$i++){
        $json_arr[$i] = $rs;
        $rs = mysqli_fetch_row($send);
    }

    echo json_encode($json_arr);
?>