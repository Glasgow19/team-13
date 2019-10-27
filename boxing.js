var imgTag = new Image();
var canvas = document.getElementById('boxing');
var ctx = canvas.getContext("2d");
var x = 0
var y = 0;

imgTag.onload = animate;
imgTag.src = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/4da7ebca-186f-412e-8aa4-d7fcf4fde7b9/d63qbks-58358696-2e62-47e2-854c-0d8cb89759ab.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzRkYTdlYmNhLTE4NmYtNDEyZS04YWE0LWQ3ZmNmNGZkZTdiOVwvZDYzcWJrcy01ODM1ODY5Ni0yZTYyLTQ3ZTItODU0Yy0wZDhjYjg5NzU5YWIuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.XN0hy9gT1r9yHF7wIs1mXzMEYV_tiA4hb97KsdealAc";   // load image

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);  // clear canvas
  ctx.drawImage(imgTag, 256, 0,128,128,0,0,160,160);                       // draw image at current position
  /* x -= 4;
  if (x > 250){
    requestAnimationFrame(animate)        // loop
    } */
}
