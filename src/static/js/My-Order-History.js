function onClickViewDetails(element) {
            const open_details = document.getElementById('view-details');
            const modal_details = document.getElementById('modal_container_view_details');
            const close_details = document.getElementById('close_view_details');
            open_details.addEventListener('click', () => {
                modal_details.classList.add('show');
            });
            close_details.addEventListener('click', () => {
                modal_details.classList.remove('show');
            });
        }
