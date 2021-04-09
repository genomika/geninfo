$( document ).ready(function() { 
    $('.div-title-name').click(function(){
        if ($(this).find('.oculta').css('display') == 'none') {
            $(this).find('.position-img').css('display') == 'none';
            $(this).find('.oculta').slideDown("slow");
            $(this).find('.expand').css('transform', 'rotate(45deg)');
        }else{
            $(this).find('.position-img').css('display') == 'none';
            $(this).find('.oculta').slideUp("slow");
            $(this).find('.expand').css('transform', 'rotate(315deg)');
        }
     });
});

$(document).ready(function(){
    $('.oculta').click(function(){

    });
});

$( document ).ready(function() { 
    $('.filter').click(function(){
        $(this).find('.card-days').slideToggle();
     });
});

$( document ).ready(function() { 
    var a = window.document.getElementById('area')
    a.addEventListener('mouseenter', entrar)
    a.addEventListener('mouseout', sair)
    function entrar(){
        a.style.color = 'rgb(58, 192, 196)'
        a.style.fontWeight = 'bold'
        a.style.borderBottom =  '2px solid rgb(58, 192, 196)'
        a.style.cursor = 'pointer'
    }
    function sair(){
        a.style.color = 'rgb(71, 88, 103)'
        a.style.borderBottom =  'None'

    }
});

