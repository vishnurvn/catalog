let searchField = document.getElementById('search-book')
let homeFlag = document.getElementById('flag')

toggleSpinner = () => {
	let spinner = document.getElementById('spinner-wrapper')
	spinner.classList.toggle('display-spinner')
}

setCurrentPage = (elem) => {
	let pageLinkNode = document.createElement('span')
	pageLinkNode.setAttribute('class', 'page-link')
	let currentSpanNode = document.createElement('span')
	pageLinkNode.textContent = elem.textContent
	currentSpanNode.setAttribute('class', 'sr-only')
	currentSpanNode.textContent = '(current)'

	pageLinkNode.append(currentSpanNode)
	return pageLinkNode
}

getBookList = (page, element) => {
	let newElement = setCurrentPage(element.firstChild)
	element.removeChild(element.firstChild)
	element.append(newElement)

	toggleSpinner()
	
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
			let keys = ['author', 'isbn', 'rating', 'availability']
			let bookListTableBody = document.getElementById('book-list-data')
			while (bookListTableBody.hasChildNodes()) {
				bookListTableBody.removeChild(bookListTableBody.firstChild)
			}
			toggleSpinner()
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
	let pageOne = document.getElementsByClassName('page-numbers')[0]
	pageOne.firstChild.click()
}

searchField.addEventListener('change', () => {
    console.log(searchField.value)
})