let searchField = document.getElementById('search-book')
let homeFlag = document.getElementById('flag')

getBookList = (page) => {
	const url = 'http://127.0.0.1:5000/get_book_list'
	let data = {
		'page': page
	}
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	}).then(
		response => {
			return response.json()
		}
	).then(
		data => {
			console.clear()
			console.log(data)
			let keys = ['author', 'isbn', 'rating', 'availability']
			let bookListTableBody = document.getElementById('book-list-data')
			console.log(page)

			while (bookListTableBody.hasChildNodes()) {
				bookListTableBody.removeChild(bookListTableBody.firstChild)
			}
			data.forEach((item) => {
				let rowElement = document.createElement('tr')
				let dataElement = document.createElement('td')
				let anchorNode = document.createElement('a')
				let textNode = document.createTextNode(item['title'])
				anchorNode.append(textNode)
				anchorNode.setAttribute('href', `http://127.0.0.1:5000/book/${item['id']}`)
				dataElement.append(anchorNode)
				rowElement.append(dataElement)
				keys.forEach((key) => {
					let dataElement = document.createElement('td')
					let textNode = document.createTextNode(item[key])
					dataElement.append(textNode)
					rowElement.append(dataElement)
				})
				bookListTableBody.append(rowElement)
			})

		}
	)
}

window.onload = () => {
	getBookList(1)
}

searchField.addEventListener('change', () => {
    console.log(searchField.value)
})