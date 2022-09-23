// the animation of the navigation on the hover
let nav  = document.querySelector('nav > .left > ul')
let items = nav.querySelectorAll('ul > li > a')

Array.from(items).forEach(item => {
    item.addEventListener('mouseover', e => {
        Array.from(items).forEach(i => {
            i.classList.add('deactive')
        })
        item.className = 'active'
    })
    item.addEventListener('mouseleave', e => {
        Array.from(items).forEach(my_items => {
            my_items.classList.remove('active')
            my_items.classList.remove('deactive')
        })
    })
})


// the sticky navigation
let navigation = document.querySelector('body > nav')
window.addEventListener('scroll', e => {
    if (window.scrollY > 0 ){
        navigation.classList.add('stiky')
    }else if (window.scrollY == 0){
        navigation.classList.remove('stiky')
    }
})


// set the navigation height
function SetHeight(){
    let ul = document.querySelector('nav .left > ul')
    ul.style.setProperty('--my-height', `${ul.clientHeight + 30000}px`)
}
SetHeight()


// toggle the active in navigation
let btn = document.querySelector('.left > .btn')
btn.addEventListener('click', e => {
    navigation.classList.toggle('active')
})

// get and set the lines 
lines = document.querySelectorAll('.line-wrapper > .line')

let LargValue = 0
let LargElement = null

Array.from(lines).forEach(line => {
    elementValue = Number(getComputedStyle(line).getPropertyValue('--per'))

    if(elementValue > LargValue ){
        LargValue = elementValue
        LargElement = line
    }
})
Array.from(lines).forEach(line => {
    elementValue = Number(getComputedStyle(line).getPropertyValue('--per'))
    if(line != LargElement){
        line.style.setProperty('--per', `${((elementValue*100)/LargValue)}`)
    } 
})
if (LargElement != null){
    LargElement.style.setProperty('--per', '100')
}


// search form

var btnDelete = document.getElementById('clear');
var inputFocus = document.getElementById('inputFocus');
//- btnDelete.on('click', function(e) {
//-   e.preventDefault();
//-   inputFocus.classList.add('isFocus')
//- })
//- inputFocus.addEventListener('click', function() {
//-   this.classList.add('isFocus')
//- })
btnDelete.addEventListener('click', function(e){
    e.preventDefault();
    inputFocus.value = ''
})
document.addEventListener('click', function(e)
    {
    if (document.getElementById('first').contains(e.target))
        {
          inputFocus.classList.add('isFocus')
        }
    else
        {
          // Clicked outside the box
          inputFocus.classList.remove('isFocus')
        }
});
