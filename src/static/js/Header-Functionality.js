function onClickLogo(element) {
            const logo_icon = document.getElementById('logo');
            logo_icon.addEventListener('click', () => {
                window.location= '/welcome';
            });
        }


function onClickMyCart(element) {
            const my_cart_icon = document.getElementById('my-cart-button');
            my_cart_icon.addEventListener('click', () => {
                window.location= '/users/buy/my-cart';
            });
        }

function onClickMyAccount() {
            document.getElementById("myDropdown").classList.toggle("show");
        }

function onClickDiscuss(element) {
        const my_account_icon = document.getElementById('discuss-button');
        my_account_icon.addEventListener('click', () => {
                window.location= '/forum';
            });
}

function onClickLogOut(element) {
            const logout_icon = document.getElementById('logout-button');
            logout_icon.addEventListener('click', () => {
                window.location= '/users/logout';
            });
        }

function onClickSellButton(element) {
            const sell_icon = document.getElementById('sell-button');
            sell_icon.addEventListener('click', () => {
                window.location= '/welcome/sell';
            });
        }

function onClickBuyButton(element) {
            const buy_icon = document.getElementById('buy-button');
            buy_icon.addEventListener('click', () => {
                window.location= '/welcome/buy';
            });
        }

function onClickBookListButton(element) {
            const booklist_icon = document.getElementById('my-book-list');
            booklist_icon.addEventListener('click', () => {
                window.location= '/welcome/sell/booklist';
            });
        }

window.onclick = function(event) {
  if (!event.target.matches('.icon-button-class')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}