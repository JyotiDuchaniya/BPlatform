function onClickAddress(element) {
            const open_address = document.getElementById('addressbox');
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

function onClickUpdateAddress(element) {
            const open_address = document.getElementById('update-address');
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

function onClick(element) {
            const open = document.getElementById('open-change-password');
            const modal = document.getElementById('modal_container');
            const cancel = document.getElementById('cancel-button');
            const close = document.getElementById('close');
            open.addEventListener('click', () => {
                modal.classList.add('show');
            });
            cancel.addEventListener('click', () => {
                modal.classList.remove('show');
            });
            close.addEventListener('click', () => {
                modal.classList.remove('show');
            });
        }

