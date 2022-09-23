let inputTag = document.querySelectorAll('form.wrapper > div#item')
Array.from(inputTag).forEach(item => {
	item.addEventListener('click', e => {
		Array.from(inputTag).forEach(i => {
			if (i.querySelector('input').value ==''){
				i.classList.remove('active')
			}	
		})
		item.classList.add('active')
	})
})

let error = document.querySelector('.error')
let error_2 = document.querySelector('.error_2')
if (error){
	error_2.textContent = error.textContent
}
