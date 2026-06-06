(function(){
  var btn=document.querySelector('button[aria-label="Meni"]');
  var nav=document.querySelector('header nav');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      var open=nav.dataset.open==='1';
      nav.dataset.open=open?'0':'1';
      nav.style.cssText=open?'':'display:flex;flex-direction:column;position:fixed;top:72px;left:0;right:0;bottom:0;background:#0d0d0d;padding:2rem 1.5rem;gap:1.5rem;z-index:40;overflow-y:auto;border-top:1px solid rgba(201,169,110,0.25)';
    });
    nav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){nav.dataset.open='0';nav.style.cssText='';});
    });
  }
  var header=document.querySelector('header');
  if(header){
    function onScroll(){
      if(window.scrollY>60){
        header.style.background='rgba(13,13,13,0.96)';
        header.style.backdropFilter='blur(10px)';
        header.style.webkitBackdropFilter='blur(10px)';
        header.style.borderBottom='1px solid rgba(255,255,255,0.08)';
      } else {
        header.style.background='';
        header.style.backdropFilter='';
        header.style.webkitBackdropFilter='';
        header.style.borderBottom='';
      }
    }
    window.addEventListener('scroll',onScroll,{passive:true});
    onScroll();
  }
})();
