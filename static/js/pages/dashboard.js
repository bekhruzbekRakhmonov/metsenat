var physicalTab = document.querySelector("#tab-physical")
var orgTab = document.querySelector("#tab-org")
var statisticsTab = document.querySelector("#tab-statistics")
var studentsTab = document.querySelector("#tab-students")

var physicalDivTab = document.querySelector("#pills-physical")
var orgDivTab = document.querySelector("#pills-org")
var statisticsDivTab = document.querySelector("#pills-statistics")
var studentsDivTab = document.querySelector("#pills-students")

var locPath = window.location.pathname

console.log(locPath)

physicalTab.onclick = () => {
    window.location.replace("/dashboard/physical-sponsor/")
    orgTab.classList.remove("show", "active")
    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.add("show", "active")

}

if (locPath === "/dashboard/physical-sponsor/") {
    orgTab.classList.remove("show", "active")
    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.add("show", "active")
}

orgTab.onclick = () => {
    window.location.replace("/dashboard/org-sponsor/")

    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.remove("show", "active")
    orgTab.classList.add("show", "active")
}

if (locPath === "/dashboard/org-sponsor/") {
    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.remove("show", "active")
    orgTab.classList.add("show", "active")
}

statisticsTab.onclick = () => {
    window.location.replace("/dashboard/")

    orgTab.classList.remove("show", "active")
    statisticsTab.classList.add("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.remove("show", "active")

}

if (locPath === "/dashboard/") {
    orgTab.classList.remove("show", "active")
    statisticsTab.classList.add("show", "active")
    studentsTab.classList.remove("show", "active")
    physicalTab.classList.remove("show", "active")
}

studentsTab.onclick = () => {
    window.location.replace("/dashboard/students/")

    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.add("show", "active")
    physicalTab.classList.remove("show", "active")
    orgTab.classList.remove("show", "active")
}

if (locPath === "/dashboard/students/") {
    statisticsTab.classList.remove("show", "active")
    studentsTab.classList.add("show", "active")
    physicalTab.classList.remove("show", "active")
    orgTab.classList.remove("show", "active")
}