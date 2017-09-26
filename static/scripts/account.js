// Dynamically build carousel items

function buildFormItems(number, name, type) {
  var element = document.createElement('div');

  element.classList.add('formItems');

  element.innerHTML = '<form class="AccInfoForm" action="#">' +
    '<input type="text" class="form-control" value=' + number +  ' placeholder="Account Number" readonly>' +
    '<input type="text" class="form-control" value=' + name + ' placeholder="Account Name" readonly>' +
    '<input type="text" class="form-control" value=' + type + ' placeholder="Account Type" readonly>' +
  '</form>';

  return element;
}

function buildAddAccount() {
  var element = document.createElement('div');

  element.classList.add('addAcc');

  element.innerHTML = '<a  class="newAcc">Add Account</a>';

  return element;
}

function buildCard(bankName, cardType, cardNumber, expiryDate, vendor) {
  var element = document.createElement('div');

  element.id = 'cardWall';

  element.classList.add('space', 'cardWall');

  element.innerHTML = '<div class="cardContent">' +
    '<div class="row">' +
      '<div class="col-md-6" id="bankName">' +
        bankName +
      '</div>' +
      '<div class="col-md-6" id="cardType">' +
        cardType +
      '</div>' +
    '</div>' +
    '<div class="row" id="chip">' +
      '<img src="" alt="">' +
    '</div>' +
    '<div class="row">' +
      '<p id="cardNo">' + cardNumber + '</p>' +
    '</div>' +
    '<div class="row" id="exVendor">' +
      '<div class="col-md-6 col-sm-6 col-xs-6 col-lg-6" id="expiry">' +
        expiryDate +
      '</div>' +
      '<div class="col-md-6 col-sm-6 col-xs-6 col-lg-6" id="vendor">' +
        vendor +
      '</div>' +
    '</div>' +
    '<div class="overlay">' +
      '<div class="row" id="addHide">' +
        '<div class="col-md-6 col-sm-6 col-xs-6 col-lg-6 text-center" onlick="duplicate()" id="plus">' +
          '<p class="glyphicon glyphicon-plus"><br>Add Card</p>' +
        '</div>' +
        '<div class="col-md-6 col-sm-6 col-xs-6 col-lg-6 text-center" id="hide">' +
          '<p class="glyphicon glyphicon-eye-open"><br>Hide Card</p>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</div>';

  return element;
}

$(document).ready(function() {


  var user = $('#my-user').data();
  var profileCarousel = document.querySelector('#profileCarousel');
  var element = [];
  console.log(user)

  if (user.user.accountIn == 0) {
    var number = 'Number';
    var name = 'Name';
    var type = 'Type';
    var bankName = 'No Bank';
    var cardType = 'No Card';
    var cardNumber = 'xxxx xxxx xxxx xxxx';
    var expiryDate = 'MM/YYYY';
    var vendor = 'Vendor';

    var element = document.createElement('div');

    element.classList.add('item');

    var profileForm = buildFormItems(number, name, type);
    element.appendChild(profileForm)

    var profileNewAcc = buildAddAccount();
    element.appendChild(profileNewAcc)

    var profileCard = buildCard(bankName, cardType, cardNumber, expiryDate, vendor);
    element.appendChild(profileCard);

  } else {
    for (i = 1; i < Object.keys(user.user.Account).length; i++) {
      var number = user.user.Account[i.toString()][2];
      var name = user.user.Account[i.toString()][4];
      var type = user.user.Account[i.toString()][5];
      var bankName = user.user.Account[i.toString()][3];
      var cardType = 'No Card';
      var cardNumber = 'xxxx xxxx xxxx xxxx';
      var expiryDate = 'MM/YYYY';
      var vendor = 'Vendor';


      var element = document.createElement('div');

      element.classList.add('item');

      var profileForm = buildFormItems(number, name, type);
      element.appendChild(profileForm)

      var profileNewAcc = buildAddAccount();
      element.appendChild(profileNewAcc)

      var profileCard = buildCard(bankName, cardType, cardNumber, expiryDate, vendor);
      element.appendChild(profileCard);
      // if (user.user.accountIn == 1) {
      //   var number = user.user.Account['0'][2];
      //   var name = user.user.Account['0'][4];
      //   var type = user.user.Account['0'][5];
      //   var bankName = user.user.Account['0'][3];
      //   var cardType = 'No Card';
      //   var cardNumber = 'xxxx xxxx xxxx xxxx';
      //   var expiryDate = 'MM/YYYY';
      //   var vendor = 'Vendor';
      //
      //   element.classList.add('item');
      //
      //   var profileForm = buildFormItems(number, name, type);
      //   element.appendChild(profileForm)
      //
      //   var profileNewAcc = buildAddAccount();
      //   element.appendChild(profileNewAcc)
      //
      //   var profileCard = buildCard(bankName, cardType, cardNumber, expiryDate, vendor);
      //   element.appendChild(profileCard);
      //
      // } else {
      //   var number = user.user.Account[i.toString()][2];
      //   var name = user.user.Account[i.toString()][4];
      //   var type = user.user.Account[i.toString()][5];
      //   var bankName = user.user.Account[i.toString()][3];
      //   var cardType = 'No Card';
      //   var cardNumber = 'xxxx xxxx xxxx xxxx';
      //   var expiryDate = 'MM/YYYY';
      //   var vendor = 'Vendor';
      //
      //   var element = document.createElement('div');
      //
      //   element.classList.add('item');
      //
      //   var profileForm = buildFormItems(number, name, type);
      //   element.appendChild(profileForm)
      //
      //   var profileNewAcc = buildAddAccount();
      //   element.appendChild(profileNewAcc)
      //
      //   var profileCard = buildCard(bankName, cardType, cardNumber, expiryDate, vendor);
      //   element.appendChild(profileCard);
      // }
    }
  }

  profileCarousel.appendChild(element);

  // profileCarousel.appendChild(element);

  $('#profileCarousel').each(function() {
    $(this).find(".item").first().addClass( "active" );
  });


$('#profileCarousel').on('click', '.newAcc', function() {
  $(this).closest('.profileWall').fadeOut();
  $('.newAccWall').show();
});

});
