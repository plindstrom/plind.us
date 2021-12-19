/*
  File Name  fish-1.0.0.js
  Project    plind.us
  Version    1.0.0
  Author     Peter Lindstrom
  Purpose    Fish tank fun.  Any flying toasters around here?
  Copyright  2021, Peter Lindstrom
  Link       https://github.com/plindstrom/plind.us
*/

var fish0 = new Image();
var fish1 = new Image();
var fish2 = new Image();
var fish3 = new Image();
var fish4 = new Image();
var fish5 = new Image();

var fx = 50;
var fy = 50;

function init(){
	fish0.src = "/img/fish/fish0.png";
	fish1.src = "/img/fish/fish1.png";
	fish2.src = "/img/fish/fish2.png";
	fish3.src = "/img/fish/fish3.png";
	fish4.src = "/img/fish/fish4.png";
	fish5.src = "/img/fish/fish5.png";

	window.requestAnimationFrame(draw);
}

function draw(){
	var ctx = document.getElementById("desk").getContext("2d");
	
	ctx.globalCompositeOperation = "destination-over";
	ctx.clearRect(0,0, 300, 300);
	ctx.save();

	if(fy > 300 || fy < 0){
		fy = 0;
	} else {
		fy = 50;
	}
	if(fx > 300 || fx < 0){
		fx = 0;
	} else {
		fx += 1;
	}

	ctx.fillText("x: " + fx + " y: " + fy, 10, 50);
	ctx.drawImage(fish0, fx, fy);


	/*ball.draw();
	ball.x += ball.vx;
	ball.y += ball.vy;
  
	if (ball.y + ball.vy > canvas.height ||
		ball.y + ball.vy < 0) {
	  ball.vy = -ball.vy;
	}
	if (ball.x + ball.vx > canvas.width ||
		ball.x + ball.vx < 0) {
	  ball.vx = -ball.vx;
	}*/
  
	window.requestAnimationFrame(draw);
}

/*function draw(){
	var ctx = document.getElementById("desk").getContext("2d");

	ctx.globalCompositeOperation = "destination-over";
	ctx.clearRect(0, 0, 1024, 520);

	ctx.save();
	ctx.translate(150, 150);

	var time = new Date();
	ctx.rotate(((2 * Math.PI) / 60) * time.getSeconds() + ((2 * Math.PI) / 60000) * time.getMilliseconds());
	ctx.translate(105, 0);
	//ctx.fillRect(0, -12, 40, 24);
	ctx.drawImage(fish0, -12, -12);

	ctx.save();
	ctx.rotate(((2 * Math.PI) / 6) * time.getSeconds() + ((2 * Math.PI) / 6000) * time.getMilliseconds());
	ctx.translate(0, 28.5);
	ctx.drawImage(fish1, -3.5, -3.5);
	ctx.restore();
  
	ctx.restore();
  
	ctx.beginPath();
	ctx.arc(150, 150, 105, 0, Math.PI * 2, false);
	ctx.stroke();
  
	//ctx.drawImage(fish2, 0, 0, 1024, 520);
  
	window.requestAnimationFrame(draw);
}*/

init();