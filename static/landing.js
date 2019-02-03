$(function () {

  $('#loginButton').click(function (e) {
    $("#login").delay(100).fadeIn(100);
    $("#register").fadeOut(100);
    $('#registerButton').removeClass('active');
    $(this).addClass('active');
    e.preventDefault();
  });
  $('#registerButton').click(function (e) {
    $("#register").delay(100).fadeIn(100);
    $("#login").fadeOut(100);
    $('#loginButton').removeClass('active');
    $(this).addClass('active');
    e.preventDefault();
  });

  $('#passwordRegister, #passwordCheck').on('keyup', function () {
    var p = $('#passwordRegister').val();
    var pc = $('#passwordCheck').val();
    if (p == pc && p.length >= 8 && pc.length >= 8) {
      $('#registerB').prop("disabled", false);
    } else
      $('#registerB').prop("disabled", true);
  });
});
