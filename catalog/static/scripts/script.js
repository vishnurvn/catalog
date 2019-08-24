let searchField = document.getElementById('search-book')
let homeFlag = document.getElementById('flag')

toggleSpinner = () => {
	let spinner = document.getElementById('spinner-wrapper')
	spinner.classList.toggle('display-spinner')
}

setCurrentPage = (elem) => {
	let elements = document.getElementsByClassName('page-numbers')
	let elementArray = [...elements]
	elementArray.forEach((element) => {
		let val = element.firstElementChild.value
		if (element.firstElementChild === elem) {
			let srSpan = document.createElement('span')
			srSpan.setAttribute('class', 'sr-only')
			srSpan.textContent = '(current)'
			while (element.firstElementChild.hasChildNodes()) {
				element.firstElementChild.firstChild.remove()
			}
			let pageNumNode = document.createTextNode(val)
			element.classList.add('active')
			element.firstElementChild.append(pageNumNode)
			element.firstElementChild.append(srSpan)
		} else {
			let pageNumNode = document.createTextNode(val)
			while (element.firstElementChild.hasChildNodes()) {
				element.firstElementChild.firstChild.remove()
			}
			element.firstElementChild.append(pageNumNode)
			element.classList.remove('active')
		}
	})
}

getBookList = (page, element) => {
	setCurrentPage(element)

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
	pageOne.firstElementChild.click()
}

searchField.addEventListener('change', () => {
    console.log(searchField.value)
})