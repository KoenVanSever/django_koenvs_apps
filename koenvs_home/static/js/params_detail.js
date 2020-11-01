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

// TODO: put buttons for these functions to run instead of running them upon page rendering
setProgDate(currentDate);
setRelDateRegInv(currentDate);

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