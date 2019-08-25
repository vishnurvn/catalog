let searchField = document.getElementById('search-book')
let homeFlag = document.getElementById('flag')

window.onload = () => {
	let pageOne = document.getElementsByClassName('page-numbers')[0]
	pageOne.firstElementChild.click()
}

searchField.addEventListener('change', () => {
    console.log(searchField.value)
})