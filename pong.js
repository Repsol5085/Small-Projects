var canvas;
var canvasContext;
var ballposX=400;
var ballposY=300;
var plusOrMinus = Math.random() < 0.5 ? -1 : 1;
var plusOrMinus2 = Math.random() < 0.5 ? -1 : 1;
var ballSpeedX=plusOrMinus*5;
var ballSpeedY=plusOrMinus2*(Math.floor(Math.random() * 5+1)) ;
var playerY=200;
var botY=200;
var playerdir=0;
var botdir=0;
var playerlast=200;
var botlast=200;
var stuck = 0;
var playerScore=0;
var botScore=0;
var botSpeed = 7;

const TOPSPEED=7;
const BAR_WIDTH = 10;
const BAR_LENGHT = 100;
const BOT_SPEED=7;

window.onload = function()
{
    canvas = document.getElementById('gameCan');
    canvasContext = canvas.getContext('2d');
    setInterval(function() {
                    movement();
                    drawing();},
                    1000/90);
    
    canvas.addEventListener('mousemove',
                            function(evt) 
                            {
                                var mousePoss = mousePos(evt);
                                playerY=mousePoss.y;
                            });
}

function botmovement()
{
    if(ballposX>400 && ballSpeedX>0)
    {
        if(botY>ballposY && ballposX > botY+BAR_LENGHT)
            botY-=botSpeed;
        else if(botY+BAR_LENGHT<ballposY) 
            botY+=botSpeed;
    }
}

function mousePos(evt)
{
    var rect = canvas.getBoundingClientRect();
    var root = document.documentElement;
    var mouseX = evt.clientX - rect.left;
    var mouseY = evt.clientY - rect.top;
    playerdir=mouseY-playerlast;
    playerlast=mouseY;
    return {x:mouseX,y:mouseY};
}

function drawing()
{   
    
    field(0,0,canvas.width,canvas.height,'rgb(34, 34, 34)','rgb(52, 119, 219)');
    canvasContext.fillStyle = 'rgb(52, 119, 219)';
    canvasContext.fillRect(30,playerY-50,BAR_WIDTH,BAR_LENGHT);
    canvasContext.fillRect(canvas.width-40,botY,BAR_WIDTH,BAR_LENGHT);
    drawBall();
}

function drawBall()
{
    canvasContext.fillStyle = ' rgb(80, 219, 52)';
    canvasContext.beginPath();
    canvasContext.arc(ballposX,ballposY,10,0,Math.PI*2, true);
    canvasContext.fill();
}

function resettingBall()
{
    if(ballposX>400)
        playerScore++;
    else botScore++; 
    stuck=0;
    plusOrMinus = Math.random() < 0.5 ? -1 : 1;
    plusOrMinus2 = Math.random() < 0.5 ? -1 : 1;
    ballSpeedX=plusOrMinus*5;
    ballSpeedY=plusOrMinus2*(Math.floor(Math.random() * 5+1)) ;
    ballposX=400;
    ballposY=300;
}
//
function movement()
{
    var  balllast = ballposX;
    ballposX+=ballSpeedX;
    ballposY+=ballSpeedY;
    if(ballposX>canvas.width)
        ballSpeedX=-ballSpeedX;
    
    if((balllast<=40&&ballposX>=30) || (balllast>=canvas.width-40 && ballposX<=canvas.width-30))
        stuck++;
    
    if(stuck>10)
        resettingBall();

    botmovement();

    if(ballposX<0 || ballposX>canvas.width-5)
        resettingBall();
    
    if((ballposX-5<=40 && ballposX-5>=30 )
        && ballposY+5 >= playerY-52 
        && ballposY-5 <= playerY+52)
            playerhitsspecial();

    if(ballposY<0)
        ballSpeedY=-ballSpeedY;
    
    if(ballposY>canvas.height)
        ballSpeedY=-ballSpeedY;

        if((ballposX+5<=canvas.width-30 && ballposX+5>=canvas.width-40 )
        && ballposY+5 >= botY-2 
        && ballposY-5 <= botY+102)
            bothitsspecial();
    


    topspeed();
    
        
}

function playerhitsspecial()
{
    if(ballposY-5>=playerY+45 && ballposY-5 <=playerY+52)
        ballSpeedY=ballSpeedY +2.5;
    if(ballposY+5>=playerY-52 && ballposY+5 <=playerY-45)
        ballSpeedY=ballSpeedY -2.5;
    if(playerdir<0)
        ballSpeedY = ballSpeedY - playerdir%5 -1;
    if(playerdir>0)
        ballSpeedY = ballSpeedY +playerdir%5 +1;

    ballSpeedX=-ballSpeedX;
}

function bothitsspecial()
{
    if(ballposY+7>=botY-2 && ballposY+7 <=botY+5)
        ballSpeedY=ballSpeedY -2.5;
    if(ballposY-7>=botY+95 && ballposY-7 <=playerY+102)
        ballSpeedY=ballSpeedY +2.5;
    if(botdir<0)
        ballSpeedY = ballSpeedY - botdir%5 -1;
    if(botdir>0)
        ballSpeedY = ballSpeedY + botdir%5 +1;

    ballSpeedX=-ballSpeedX;
}

function topspeed()
{
    if(ballSpeedX>TOPSPEED)
        ballSpeedX=TOPSPEED;
    if(-ballSpeedX>TOPSPEED)
        ballSpeedX=-TOPSPEED;
    if(ballSpeedY>TOPSPEED)
        ballSpeedY=TOPSPEED;
    if(-ballSpeedY>TOPSPEED)
        ballSpeedY=-TOPSPEED;
}

function tips()
{
    if(botScore-playerScore <= -10 && botScore-playerScore > -12)
        return "Tip: Watch out we've got a badass over here!";
    
    if(botScore-playerScore <= -15)
    {   
        botSpeed = 10;
        return "Tip: Omae wa mou shindeiru!";
    }
    
    if(botScore-playerScore == 10)
        return "Tip: Be better!";

    if(botScore-playerScore >= 15 && botScore-playerScore <17)
        return "Tip: Wow, just... wow...";

    if(botScore-playerScore == 20)
    {   
        botSpeed=4;
        return "Tip: Bot speed lowered! Damn, you suck...";
    }
    
    if(botScore-playerScore == 500)
    {
        botSpeed=0;
        ballposX=400;
        ballposY=300;
        ballSpeedX=0;
        ballSpeedY=0;
        return "You lose! I'm sorry I can't take this anymore... Just get out!!!"
    }
    return "";
    
}

function field(x,y,width,height,color,color2)
{

    canvasContext.fillStyle = color;
    canvasContext.fillRect(x,y,width,height);
    canvasContext.fillStyle = color2;
    for(var i=0; i<10;i++)
        canvasContext.fillRect(canvas.width/2-1.5,15+i*60,3,30);
    canvasContext.font = "20px Tahoma, Geneva, sans-serif";
    canvasContext.fillText(playerScore,50,50);
    canvasContext.fillText(botScore,canvas.width-70,50);
    canvasContext.fillText(tips(),100,50);
    
}
