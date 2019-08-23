let borrowButton = document.getElementById('borrow-button')

borrowButton.addEventListener('click', () => {
    borrowButton.classList.toggle('btn-primary')
    borrowButton.classList.toggle('btn-success')
    if (borrowButton.innerHTML == 'Borrow') {
        borrowButton.innerHTML = 'Borrowed'
    } else {
        borrowButton.innerHTML = 'Borrow'
    }
})