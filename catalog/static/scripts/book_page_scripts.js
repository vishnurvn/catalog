let borrowButton = document.getElementById('borrow-button')

borrowBook = (bookId) => {
	let url = `http://127.0.0.1:5000/book/${bookId}/borrow`
	fetch(url, {
		headers: {
			method: 'GET'
		}
	}).then(
		response => {
			return response.json()
		}
	).then(
		data => {
			console.log(data)
		}
	)
}

borrowButton.addEventListener('click', () => {
    borrowButton.classList.toggle('btn-primary')
    borrowButton.classList.toggle('btn-success')
    if (borrowButton.innerHTML == 'Borrow') {
        borrowButton.innerHTML = 'Borrowed'
    } else {
        borrowButton.innerHTML = 'Borrow'
    }
})