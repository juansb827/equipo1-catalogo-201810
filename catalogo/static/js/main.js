/*
$(document).ready(function(){
    $('.header').height($(window).height());
})
*/
$("#verCatalogo").click(function(){
    $("body,html").animate({
     scrollTop:  $('.header').height() -  $('nav').height() 
    },1000)
    
   })