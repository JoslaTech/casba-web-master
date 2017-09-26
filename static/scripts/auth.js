$(document).ready(function(){

  $(".newAccount").click(function(){
    $('.loginWall').fadeOut();
    $(".signupWall").show();
  });

  $('.digital').on('click', '.newLogin', function() {
    $(this).closest('.signupWall').fadeOut();
    $(".loginWall").show();
  });

  $('.analytics').on('click', '.newLogin', function() {
    $(this).closest('.signupWall').fadeOut();
    $(".loginWall").show();
  });

  $(".forgotPassword").click(function(){
    $('.loginWall').fadeOut();
    $(".passwordWall").show();
  });

  $(".accountWall-NewAccount").click(function(){
    $('.accountWall-Stats').fadeOut();
    $(".newAccountWall").show();
  });

  $(".accountWall-NewCard").click(function(){
    $('.accountWall-Stats').fadeOut();
    $(".newCardWall").show();
  });

  $('.digital').on('click', '.dismiss', function() {
    $(this).closest('.dismissParent').fadeOut();
    $(".loginWall").show();
  });

  $('.digital').on('click', '.dismiss', function() {
    $(this).closest('.dismissParent').fadeOut();
    $(".profileWall").show();
  });

});
