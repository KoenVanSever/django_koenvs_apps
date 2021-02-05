// import Cookies from "js.cookie.min.js";
window.onload = () => {
    let temp = Cookies.get("csrftoken");
    return temp;
}
const csrfToken = window.onload()
console.log(`The loaded csrf_token is: ${csrfToken}`);

let listChecks = document.querySelectorAll(".checkbox");

document.querySelector("#test").addEventListener("click", () => {
    console.log("clicked");
    $.ajax({
        type: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        url: "/dimming/ajax/",
        data: "test",
        success: () => {
            console.log("success");
        }
    })
    // const request = new XMLHttpRequest("{% url 'dimming:ajax' %}")
})

selected.forEach(sel => {
    listChecks.forEach(check => {
        if (sel == check.value) {
            check.checked = true;
        };
    });
});