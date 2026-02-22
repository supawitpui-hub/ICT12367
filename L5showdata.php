<?php
require('L5dbconnect.php');
$sql ="SELECT * FROM employees";
$result=mysqli_query($connect,$sql);

while($row=mysqli_fetch_assoc($result)){
    echo "รหัสพนักงาน = ".$row["id"]."<dr>";
    echo "ชื่อ = ".$row["fname"]."<dr>";
    echo "นามสกุล = ".$row["lname"]."<dr>";
    echo "เพศ = ".$row["gender"]."<dr>";
    echo "ทักษะ = ".$row["skills"]."<dr>";
}
?>