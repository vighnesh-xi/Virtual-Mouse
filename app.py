import streamlit as st
import streamlit.components.v1 as components

st.title("🖱️ Virtual Mouse Demo")
st.write("Allow camera access. Your hand controls a **virtual cursor** on screen.")

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #0e1117; color: white; font-family: sans-serif; }
  #container { position: relative; width: 640px; height: 480px; margin: auto; }
  #video { width: 640px; height: 480px; transform: scaleX(-1); border-radius: 8px; }
  #canvas { position: absolute; top: 0; left: 0; width: 640px; height: 480px; transform: scaleX(-1); }
  #cursor {
    position: absolute; width: 24px; height: 24px;
    border-radius: 50%; background: rgba(255, 0, 255, 0.85);
    border: 3px solid white; pointer-events: none;
    transform: translate(-50%, -50%); transition: background 0.1s; z-index: 10;
  }
  #cursor.click { background: rgba(0,255,100,0.95); transform: translate(-50%,-50%) scale(1.4); }
  #status { text-align:center; padding:8px; font-size:18px; font-weight:bold; color:#ccc; min-height:32px; }
  #fps { position:absolute; top:8px; left:8px; color:lime; font-size:14px; z-index:20; }
</style>
</head>
<body>
<div id="status">⏳ Loading MediaPipe...</div>
<div id="container">
  <video id="video" autoplay playsinline></video>
  <canvas id="canvas"></canvas>
  <div id="cursor"></div>
  <div id="fps">FPS: --</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
<script>
const video=document.getElementById('video'),canvas=document.getElementById('canvas'),
      ctx=canvas.getContext('2d'),cursor=document.getElementById('cursor'),
      status=document.getElementById('status'),fpsEl=document.getElementById('fps');
canvas.width=640; canvas.height=480;
const FR=100; let smoothX=320,smoothY=240,prevX=320,prevY=240,lastTime=performance.now();
const SMOOTH=5;

const hands=new Hands({locateFile:f=>`https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}`});
hands.setOptions({maxNumHands:1,modelComplexity:1,minDetectionConfidence:0.7,minTrackingConfidence:0.6});

hands.onResults(results=>{
  const now=performance.now();
  fpsEl.textContent=`FPS: ${Math.round(1000/(now-lastTime))}`; lastTime=now;
  ctx.clearRect(0,0,640,480);
  ctx.strokeStyle='rgba(255,0,255,0.5)'; ctx.lineWidth=2;
  ctx.strokeRect(FR,FR,640-FR*2,480-FR*2);

  if(!results.multiHandLandmarks||!results.multiHandLandmarks.length){
    status.textContent='🖐 Show your hand'; return;
  }
  const lm=results.multiHandLandmarks[0];
  drawConnectors(ctx,lm,HAND_CONNECTIONS,{color:'#00FF00',lineWidth:2});
  drawLandmarks(ctx,lm,{color:'#FF00FF',lineWidth:1,radius:3});

  const ix=(1-lm[8].x)*640, iy=lm[8].y*480;
  const mx=(1-lm[12].x)*640, my=lm[12].y*480;
  const indexUp=lm[8].y<lm[6].y, middleUp=lm[12].y<lm[10].y;

  smoothX=prevX+(ix-prevX)/SMOOTH; smoothY=prevY+(iy-prevY)/SMOOTH;
  prevX=smoothX; prevY=smoothY;

  cursor.style.left=(640-smoothX)+'px'; cursor.style.top=smoothY+'px';

  if(indexUp&&!middleUp){
    status.textContent='☝️ MOVE MODE'; cursor.className='';
    ctx.beginPath(); ctx.arc(ix,iy,12,0,2*Math.PI);
    ctx.fillStyle='rgba(255,0,255,0.7)'; ctx.fill();
  } else if(indexUp&&middleUp){
    const dist=Math.hypot(ix-mx,iy-my);
    ctx.beginPath(); ctx.moveTo(ix,iy); ctx.lineTo(mx,my);
    ctx.strokeStyle='#00FF88'; ctx.lineWidth=3; ctx.stroke();
    if(dist<40){
      status.textContent='✌️ CLICKED! 🟢'; cursor.className='click';
      ctx.beginPath(); ctx.arc((ix+mx)/2,(iy+my)/2,20,0,2*Math.PI);
      ctx.fillStyle='rgba(0,255,100,0.5)'; ctx.fill();
    } else {
      status.textContent=`✌️ CLICK READY — closer! (${Math.round(dist)}px)`; cursor.className='';
    }
  } else {
    status.textContent='🖐 Raise index finger'; cursor.className='';
  }
});

const camera=new Camera(video,{
  onFrame:async()=>{await hands.send({image:video});},
  width:640,height:480
});
camera.start()
  .then(()=>{status.textContent='🖐 Show your hand';})
  .catch(err=>{status.textContent='❌ Camera error: '+err.message;});
</script>
</body>
</html>
""", height=560)
