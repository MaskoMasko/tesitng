var pass1 = document.querySelector(".pass1")
var pass2 = document.querySelector(".pass2")
var form = document.querySelector(".form")
var btn = document.querySelector("button")
var errmsg = document.querySelector(".pass-err")
form.addEventListener("submit", (e)=>{
    e.returnValue = true;
    if(pass1.value == "" || pass2.value == ""){
        errmsg.innerHTML = "ENTER PASSWORD"
        e.preventDefault()
    }
    if(pass1.value == pass2.value){
        form.setAttribute("action", "/signupTry")
        form.setAttribute("method", "POST")
    }else{
        errmsg.innerHTML = "ONE OF PASSWORDS IS INCORRECT"
            e.preventDefault()
    }
})