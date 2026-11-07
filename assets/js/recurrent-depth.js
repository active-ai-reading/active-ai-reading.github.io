(()=>{
const root=document.getElementById('rd-explorer');if(!root)return;
const $=id=>root.querySelector('#'+id), svgNS='http://www.w3.org/2000/svg';
let mode='recurrent', raf=0, start=0, running=false, lastTick=-1;
const configs={recurrent:{min:1,max:32,value:8,label:'Recurrent passes'},parameters:{min:1,max:12,value:4,label:'Distinct Transformer blocks'},tokens:{min:0,max:12,value:4,label:'Intermediate reasoning tokens'}};
const state={recurrent:8,parameters:4,tokens:4};
const title={recurrent:['One block. Many passes.','The input is processed once, the recurrent core is reused, and the final state is decoded.'],parameters:['More blocks. More weights.','A schematic fixed-depth Transformer: increasing the number of distinct blocks also increases stored parameters.'],tokens:['More tokens. More forward passes.','A fixed model generates intermediate reasoning tokens sequentially before the final answer.']};
function svgEl(tag,attrs={},text){let el=document.createElementNS(svgNS,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text!==undefined)el.textContent=text;return el}
function append(parent,tag,attrs,text){const e=svgEl(tag,attrs,text);parent.appendChild(e);return e}
function box(parent,x,y,w,h,label,color,subtitle){append(parent,'rect',{x,y,width:w,height:h,rx:10,fill:color[0],stroke:color[1],'stroke-width':2});append(parent,'text',{x:x+w/2,y:y+24,'text-anchor':'middle',fill:'#eef4ff','font-size':16,'font-weight':700},label);if(subtitle)append(parent,'text',{x:x+w/2,y:y+44,'text-anchor':'middle',fill:'#b8cce1','font-size':12},subtitle)}
function line(parent,x1,y1,x2,y2){append(parent,'path',{d:`M${x1} ${y1} L${x2} ${y2}`,stroke:'#9cacc4','stroke-width':2.2,fill:'none','marker-end':'url(#rd-arrow)'})}
function otherDiagram(n){const g=$('rd-other-drawing');g.replaceChildren();if(mode==='parameters'){
 append(g,'text',{x:330,y:28,'text-anchor':'middle',fill:'#c3d4e9','font-size':15},'Each block has its own learned weights');
 const visible=Math.min(n,9),w=52,gap=10,total=visible*w+(visible-1)*gap,startX=(660-total)/2;
 for(let i=0;i<visible;i++){const x=startX+i*(w+gap);box(g,x,92,w,64,`B${i+1}`,['#1b354e','#76adf6'],'unique');if(i)line(g,x-gap+2,124,x-3,124)}
 if(n>visible)append(g,'text',{x:330,y:191,'text-anchor':'middle',fill:'#ffcc81','font-size':14},`+ ${n-visible} additional distinct blocks (not drawn)`);
 append(g,'text',{x:330,y:242,'text-anchor':'middle',fill:'#a9c1d6','font-size':14},'More blocks → more parameter storage and more computation');
 }else{
 append(g,'text',{x:330,y:25,'text-anchor':'middle',fill:'#c3d4e9','font-size':15},'The same fixed model is invoked for each generated token');
 box(g,28,92,125,68,'Fixed LLM',['#1b354e','#76adf6'],'same weights');
 line(g,153,126,196,126);
 const count=Math.min(n,5),startX=205,step=67;
 for(let i=0;i<count;i++){const x=startX+i*step;box(g,x,100,54,52,`t${i+1}`,['#3b3126','#ffcc81'],'CoT');if(i)line(g,x-12,126,x-3,126)}
 if(n>count)append(g,'text',{x:555,y:185,'text-anchor':'middle',fill:'#ffcc81','font-size':13},`+ ${n-count} more tokens`);
 if(n===0)append(g,'text',{x:280,y:128,fill:'#c3d4e9','font-size':14},'No intermediate tokens');
 box(g,539,100,105,52,'Answer',['#442c40','#e69cbd'],'output');
 append(g,'text',{x:330,y:242,'text-anchor':'middle',fill:'#a9c1d6','font-size':14},'More generated tokens → more sequential forward passes');
 }}

function setText(id,s){$(id).textContent=s}
function render(){const n=state[mode],cfg=configs[mode];setText('rd-title',title[mode][0]);setText('rd-subtitle',title[mode][1]);setText('rd-slider-label',cfg.label);setText('rd-rval',n);setText('rd-min',cfg.min);setText('rd-mid',Math.floor((cfg.min+cfg.max)/2));setText('rd-max',cfg.max);$('rd-depth').min=cfg.min;$('rd-depth').max=cfg.max;$('rd-depth').value=n;
 root.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
 $('rd-recurrent-drawing').style.display=mode==='recurrent'?'':'none';$('rd-other-drawing').style.display=mode==='recurrent'?'none':'';
 if(mode==='recurrent'){setText('rd-times',`× ${n} ${n===1?'pass':'passes'}`);setText('rd-depth-value',4*n+4);setText('rd-depth-caption','Effective layer applications');setText('rd-weights-value','8');setText('rd-weights-caption','Distinct Transformer layers');setText('rd-params-value','3.5B');setText('rd-params-caption','Stored model parameters');setText('rd-output-value','0');setText('rd-output-caption','Intermediate reasoning tokens');$('rd-callout').innerHTML=`<strong>Shared weights, not independent layers..</strong> At ${n} ${n===1?'pass':'passes'}, ${4*n+4} layer applications use only 8 distinct Transformer layers.`}
 else if(mode==='parameters'){otherDiagram(n);setText('rd-depth-value',n);setText('rd-depth-caption','Unique blocks (illustrative)');setText('rd-weights-value',n);setText('rd-weights-caption','Distinct block weight sets');setText('rd-params-value','↑ with blocks');setText('rd-params-caption','Parameter storage');setText('rd-output-value','0');setText('rd-output-caption','Extra reasoning tokens');$('rd-callout').innerHTML='<strong>Parameter scaling:</strong> adding distinct blocks increases model capacity and typically increases parameter memory and compute. This is a conceptual comparison, not a specific model.'}
 else{otherDiagram(n);setText('rd-depth-value','Fixed');setText('rd-depth-caption','Model depth per forward pass');setText('rd-weights-value','Fixed');setText('rd-weights-caption','Model weight sets');setText('rd-params-value','Fixed');setText('rd-params-caption','Parameter storage');setText('rd-output-value',n);setText('rd-output-caption','Intermediate reasoning tokens');$('rd-callout').innerHTML='<strong>Verbal reasoning:</strong> more intermediate tokens mean additional model forward passes. The model parameters stay fixed, but the output sequence grows.'}
 }
function stop(){running=false;cancelAnimationFrame(raf);$('rd-moving-dot').setAttribute('opacity','0');$('rd-rblock').classList.remove('pulse');$('rd-play').textContent='▶ Animate'}
function animation(t){if(!running)return;if(!start)start=t;const n=state[mode],duration=mode==='recurrent'?330:550,idx=Math.floor((t-start)/duration);if(idx>=n){stop();setText('rd-status',`Completed ${n} ${mode==='recurrent'?'core passes':mode==='tokens'?'intermediate tokens':'blocks'}.`);return}if(idx!==lastTick){lastTick=idx;setText('rd-status',`Step ${idx+1} of ${n}.`)}if(mode==='recurrent'){let path=$('rd-loop-path'),p=path.getPointAtLength(((t-start)%duration)/duration*path.getTotalLength());$('rd-moving-dot').setAttribute('cx',p.x);$('rd-moving-dot').setAttribute('cy',p.y);$('rd-moving-dot').setAttribute('opacity','1');$('rd-rblock').classList.toggle('pulse',((t-start)%duration)<160)}else{const g=$('rd-other-drawing');g.style.opacity=((t-start)%duration)<duration/2?'1':'.65'}raf=requestAnimationFrame(animation)}
root.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{stop();mode=b.dataset.mode;setText('rd-status','Drag the slider or play the animation.');render()}));
$('rd-depth').addEventListener('input',e=>{stop();state[mode]=+e.target.value;render()});
$('rd-play').addEventListener('click',()=>{if(running){stop();return}if(state[mode]===0){setText('rd-status','Select at least one token to animate.');return}running=true;start=0;lastTick=-1;$('rd-play').textContent='■ Stop';raf=requestAnimationFrame(animation)});
render();
})();
