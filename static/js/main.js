//GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

//ENSURE SEARCH FROM EXISTS
if(searchForm){
    for(let i=0; pageLinks.length > i ; i++){
        pageLinks[i].addEventListener('click',function (e) {
        e.preventDefault()

        //GET THE DATA ATTRIBUTE
        let page = this.dataset.page

        //ADD HIDDEN SEARCH INPUT TO FORM
        searchForm.innerHTML += `<input value=${page} name="page" hidden />`

        //SUBMIT FORM
        searchForm.submit()

        })
    }
}

var toastElList = [].slice.call(document.querySelectorAll('.toast'));
var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(function(toast) {
        toast.show();
    });