function onClickAddicon(element) {
            const my_cart_icon = document.getElementById('add-to-cart-button');
            my_cart_icon.addEventListener('click', () => {
                window.location= '/users/my-cart';
            });
}

function onClickAddressMyCart(element) {
    const open_address = document.getElementById('change-address-my-cart');
    const modal_address = document.getElementById('modal_container_address');
    const cancel_address = document.getElementById('cancel-button_address');
    const close_address = document.getElementById('close_address');
    open_address.addEventListener('click', () => {
        modal_address.classList.add('show');
    });
    cancel_address.addEventListener('click', () => {
        modal_address.classList.remove('show');
    });
    close_address.addEventListener('click', () => {
        modal_address.classList.remove('show');
    });
}
