
var downArrow = document.getElementById("btn1");
var upArrow = document.getElementById("btn2");

downArrow.onclick = function () {
    'use strict';
    document.getElementById("first-list").style = "top:-620px";
    document.getElementById("second-list").style = "top:-620px";
    downArrow.style = "display:none";
    upArrow.style = "display:block";
};

upArrow.onclick = function () {
    'use strict';
    document.getElementById("first-list").style = "top:0";
    document.getElementById("second-list").style = "top:80px";
    upArrow.style = "display:none";
    downArrow.style = "display:block";
};


// creating my image link

var link = document.createElement("a");
document.body.appendChild(link);

link.href = "https://codepen.io/mo7hamed/pens/public";
link.target = "_blank";

var photo = document.createElement("img");
link.appendChild(photo);

photo.src =
  "https://s3-us-west-2.amazonaws.com/s.cdpn.io/1292524/profile/profile-80.jpg";
photo.alt = "mo7amed";

photo.style =
  "border-radius:50%;position:fixed;bottom:20px;right:20px;transition:all 0.5s ease";

photo.onmouseover = function() {
  this.style.transform = "scale(1.1,1.1)";
  this.style.boxShadow = "5px 5px 15px #000";
};

photo.onmouseout = function() {
  this.style.transform = "scale(1,1)";
  this.style.boxShadow = "none";
};