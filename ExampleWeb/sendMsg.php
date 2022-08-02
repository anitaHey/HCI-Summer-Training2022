<?php
	header('Access-Control-Allow-Origin: *');
	$conn=mysqli_connect("localhost","root","","example_web");
	mysqli_query($conn,"set names utf8");

    $msg = $_POST['msg'];

    date_default_timezone_set("Asia/Taipei"); 
    $timestamp = date('Y-m-d H:i:s');

    $sql = "INSERT INTO `message`(`id`, `message`, `timestamp`) VALUES (0, '$msg','$timestamp')";
    if(!$send = mysqli_query($conn, $sql)) {
        echo mysqli_error($conn);
    } else {
        echo "success";
    }
?>