var cpost=document.getElementById("cpost")
function postc(){
    cpost.style.top="62px"
}
function postd(){
    cpost.style.top="-310px"
}
var pchat=document.getElementById("pchatbox")
function messc(){
    pchat.style.right="0%"
}
function messd(){
    pchat.style.right="-17.6%"
}
// document.onclick=function(){cpost.style.top="-266px"};
// window.onclick = function () {
//     // cpost.style.top="-266px"
//         }
window.addEventListener('scroll' , ()=>{
    const scrollable=50;
    const scrolled=positiontop=$(document).scrollTop();
    if(Math.ceil(scrolled)>scrollable ){
      postd()
        }});
