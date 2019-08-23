let borrowButton = document.getElementById('borrow-button')

borrowButton.addEventListener('click', () => {
    borrowButton.classList.toggle('btn-primary')
    borrowButton.classList.toggle('btn-success')
})