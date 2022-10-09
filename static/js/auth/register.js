var loginTab = document.querySelector("#tab-physical")
var registerTab = document.querySelector("#tab-org")
var loginDivTab = document.querySelector("#pills-physical")
var registerDivTab = document.querySelector("#pills-org")


loginTab.onclick = () => {
    registerTab.classList.remove("show", "active")
    loginTab.classList.add("show", "active")
    registerDivTab.classList.remove("show", "active")
    loginDivTab.classList.add("show", "active")
}
registerTab.onclick = () => {
    loginTab.classList.remove("show", "active")
    registerTab.classList.add("show", "active")
    loginDivTab.classList.remove("show", "active")
    registerDivTab.classList.add("show", "active")
}