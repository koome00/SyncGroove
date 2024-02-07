import time

now = int(time.time())

print(now)

resp.get

playlists = []

names = [item["name"] for item in resp["items"]]
    
    return jsonify(names)

flex-direction: column;
body {
    font-family: Arial, sans-serif;
    width: 100%; /* Full width */
    height: 100vh; /* Full height */
    margin: 0; /* Remove default margin */
    padding: 20px; /* Add padding to body */
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    background-color: gray;
}

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="..\static\images\icons8-music-16.png" sizes="16x16">
  <link rel="stylesheet" href="..\static\css\index.css" >
  <link rel="stylesheet" href="..\static\css\index_body.css" >
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <link rel="stylesheet" href="..\static\css\common.css" >
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Pacifico">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
  <title>SyncGroove</title>
</head>


<body>
  <header>  
    <div class="container">
      <h2 class="brand-text">Welcome {{ name }}</h2>   
      <button class="btn btn1" onclick="window.location.href='{{ url_for('logout') }}'">Log Out</button>
    </div>
  </header>
  
  <div class="container">
    <div class="sidebar">
      <div class="head">
        <div class="user-img">
          <img src="{{ p_pic}}" alt="profile picture">
        </div>
        <div class="user-details">
          <p class="name">{{ name }}</p>
          <p class="followers">{{ followers }}</p>
        </div>
      </div>
    </div>
  </div>

  <footer>
    <div class="footer-content">
      <h3>SyncGroove</h3>
      <ul class="socials">
        <li><a href="https://twitter.com/khvfv_" target="_blank"><i class="fa-brands fa-twitter fa-bounce" style="color: #162938;"></i></a></li>
        <li><a href="https://github.com/koome00" target="_blank"><i class="fa-brands fa-github-alt fa-bounce" style="color: #162938;"></i></a></li>
        <li><a href="https://www.linkedin.com/in/collins-koome-728544261/" target="_blank"><i class="fa-brands fa-linkedin-in fa-bounce" style="color: #162938;"></i></a></li>
      </ul>
    </div>
    <div class="footer-bottom">
      <p>copyright SyncGroove&copy; 2023 designed by <span>koome</span> </p>
    </div>
  </footer>

</body>
</html>