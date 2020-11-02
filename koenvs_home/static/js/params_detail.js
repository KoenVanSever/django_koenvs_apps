function inverseInput(el1, el2) {
    el1.addEventListener("keypress", (e) => {
        if (e.key == 'Enter') {
            let temp = Number(el1.value);
            el2.value = temp <= 255 ? 255 - temp : 0;
        }
    });
    el2.addEventListener("keypress", (e) => {
        if (e.key == 'Enter') {
            let temp = Number(el2.value);
            el1.value = temp <= 255 ? 255 - temp : 0;
        }
    });
}
inverseInput(document.getElementById("byte128"), document.getElementById("byte132"));
inverseInput(document.getElementById("byte129"), document.getElementById("byte133"));
inverseInput(document.getElementById("byte130"), document.getElementById("byte134"));
inverseInput(document.getElementById("byte131"), document.getElementById("byte135"));

const currentDate = new Date();
function setProgDate(date) {
    console.log("Run setProgDate");
    let [month, day, year] = date.toLocaleDateString().split("/");
    let [hour, minute, second] = date.toLocaleTimeString().slice(0, 7).split(":");
    document.getElementById("byte171").value = year.substring(year.length - 2, year.length);
    document.getElementById("byte172").value = month;
    document.getElementById("byte173").value = day;
    document.getElementById("byte174").value = hour;
}
function ISO8601_week_no(dt) {
    let tdt = new Date(dt.valueOf());
    let dayn = (dt.getDay() + 6) % 7;
    tdt.setDate(tdt.getDate() - dayn + 3);
    let firstThursday = tdt.valueOf();
    tdt.setMonth(0, 1);
    if (tdt.getDay() !== 4) {
        tdt.setMonth(0, 1 + ((4 - tdt.getDay()) + 7) % 7);
    }
    return 1 + Math.ceil((firstThursday - tdt) / 604800000);
}

function setRelDateRegInv(date) {
    console.log("Run setRelDateRegInv");
    year = date.getFullYear();
    week = ISO8601_week_no(date);
    document.getElementById("byte128").value = String(year - 2000);
    document.getElementById("byte132").value = String(255 - (year - 2000));
    document.getElementById("byte129").value = String(week);
    document.getElementById("byte133").value = String(255 - week);
    document.getElementById("byte130").value = "1";
    document.getElementById("byte134").value = "254";
    document.getElementById("byte131").value = "1";
    document.getElementById("byte135").value = "254";
}

document.getElementById("set_prog").addEventListener("click", () => { setProgDate(currentDate) });
document.getElementById("set_release").addEventListener("click", () => { setRelDateRegInv(currentDate) });
document.getElementById("adjust_flux").addEventListener("click", () => {
    let targetFlux = Number(document.getElementById("flux_input").value);
    for (let i of [163, 164, 165, 166, 167, 168]) {
        let targetEntry = "byte" + i;
        console.log(targetEntry);
        document.getElementById(targetEntry).value = targetFlux;
    }
});
function setDefault(params, ovr = null) {
    let temp = JSON.parse(params);
    for (e in ovr) {
        temp[e] = ovr[e];
    }
    for (e in temp) {
        let id = "byte" + e;
        document.getElementById(id).value = temp[e];
    }
}
document.getElementById("default_regular").addEventListener("click", () => {
    setDefault(defParams, { 212: 255 });
});
document.getElementById("default_sign").addEventListener("click", () => {
    setDefault(defParams, { 212: 254 });
});
function getData(paramList) {
    temp = JSON;
    paramList.forEach(e => {
        input = e.getElementsByTagName("input")[0].value;
        label = e.getElementsByClassName("param_label")[0].innerHTML;
        labelClean = label.replace(/\W/g, "");
        temp[labelClean] = input;
    });
    return temp;
}