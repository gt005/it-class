let CookieManager = {
    set: function (name, value, days) {
         let expires = "";
          if (days) {
              let d = new Date();
              d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
              expires = "; expires=" + d.toGMTString();
          }
          document.cookie = name + "=" + value + expires + ";";
          return this.get(name);
    },
    get: function (name) {
          name += "=";
          let b = document.cookie.split(';'), c;
          for (var i = 0; i < b.length; i++) {
              c = b[i].replace(/(^\s+)|(\s+$)/g, "");
              while (c.charAt(0) == ' ')
                   c = c.substring(1, c.length);
              if (c.indexOf(name) == 0)
                   return c.substring(name.length, c.length);
          }
          return null;
    },
    remove: function (name) {
          this.set(name, "", -1);
    }
};


function sendShoppingCartOperation(url) {
    let request = new XMLHttpRequest();
    url += ("&token=" + CookieManager.get("csrftoken"));
    request.open('GET', url);
    request.responseType = 'json';
    request.send();
    return request
}


function getCorrectNameForPoints (number) {
    if ((10 <= number % 100) && (number % 100 <= 20) || (number % 10 == 0) || (5 <= (number % 10)) && ((number % 10) <= 9)) {
        return "Баллов"
    } else if (number % 10 == 1) {
        return "Балл"
    }
    return "Балла"
}


function showAlertElement(message, success=false) {
    let alertElement = `<div class="alert alert-danger alert-dismissible fade show" id="alert-msg" role="alert"><strong>Ошибка:</strong> <span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;

    if (success === true)
    {
        alertElement = `<div class="alert alert-success alert-dismissible fade show" id="alert-msg" role="alert"><span class="alert-msg-text">${message}</span> <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> </div>`;
    }

    document.querySelector(".messages-container").innerHTML += alertElement;

    $(".alert").delay(2500).slideUp(200, function() {
        $(this).alert('close');
    });
}