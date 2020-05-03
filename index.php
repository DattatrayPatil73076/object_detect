
<html>
<head>
<title>YOLO - Image Detector</title>
</head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>
<center>
   <body><br><br>
   <h1>Object Detection With YOLO</h1>
   <br><br>
      <form action="" method="POST" enctype="multipart/form-data">
         <input type="file" name="image" />
         <input type="submit"/>
      </form>
      
   </body>
</html>
</center>
<?php
   if(isset($_FILES['image'])){
      $file_tmp =$_FILES['image']['tmp_name'];
      $err = "";
         move_uploaded_file($file_tmp,"./api/img/"."test.jpg");
         echo "<br><center>Success<br><br>";		 
		 $api_endpoint = "http://127.0.0.1:5000/api/"; #$_ENV["API_ENDPOINT"] ?: "http://localhost:5000/api/";
		 $json = @file_get_contents($api_endpoint ."test.jpg");

		if($json == false) {
			$err = "Something is Wrong ";
		} else {
			$err = "0";
			$datas = json_decode($json, true);
		}
		      if ($err == "0"){
              #print_r($datas);
			  echo "<img src=./api/img/opimg.jpg height=360 width=240 /><br><br>";
			  echo "<table border=1 width=44% > ";
				echo "<tr>";
					echo "<th>Object</th>";
					echo "<th>Label</th>";
					echo "<th>Confidence</th>";
			   echo "</tr>";
			   for ( $row = 0; $row < count($datas); $row++ )
			  {
				echo "<tr>";
				echo "<td>" . $datas[$row]['object'] . "</td>";
				echo "<td>" . $datas[$row]['label'] . "</td>";
				echo "<td>" . $datas[$row]['confidence'] . "</td>";
				echo "</tr>";
			  }
			  echo "</table>";
			  echo "<br><br>Total Objects : ".count($datas);
			  echo "</center>";
			  }
			  else 
				{ echo "$err"; }
			  
      }
?>
