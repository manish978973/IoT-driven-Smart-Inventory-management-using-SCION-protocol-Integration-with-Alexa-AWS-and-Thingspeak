<html>

<head>
<style type ="text/css">
body{
  background-color: black;
}

table, th, td{
  background-color:white;
  border: 1px solid black;
}

table{
  width: 70%;
}

th {
  height: 50px;
  font-size: 30px;
  background-color: #4CAF50;
  color: white;
}

td{
  font-size: 25px;
}

</style>
</head>
 <body>

<?php
$servername = "localhost";
$username = "productadmin";
$password = "raspberry";
$dbname = "productinfo";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT name,unitweight,rfid_uid  FROM products";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table border =1 align='center'><tr><th>ProductName</th><th>UnitWeight (gms)</th><th>RFID_UID</th></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td align='center'>".$row["name"]."</td><td align='center'>".$row["unitweight"]."</td><td align='center'>".$row["rfid_uid"]."</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}
$conn->close();
?>
</body>
</html>
