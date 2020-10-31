// * Declaration of variables
let arg1 = document.querySelector("#entry_arg1");
let arg2 = document.querySelector("#entry_arg2");
let hpc = document.querySelectorAll("input[type='radio'][value='HPC']")[0];
let fo = document.querySelectorAll("input[type='radio'][value='FO/LCC']")[0];
let portList = document.querySelectorAll("option[class='conv_list']");
// let bufTimeMan = document.getElementById("buftime");
let finalForm = document.getElementById("finalForm");
let finalData = document.getElementById("finalData");
let dialog = document.querySelector('.example-dialog');
let pid = document.querySelector('#pid_entry');

// /i function declaration: loads before any code is executed (delays program before any code is ran)
// /i this also means that the function can be called before it is declared!!! function expression can not do that
function printSomething(data) {
    console.log(data);
};
// /i function declaration: loads before any code is executed (delays program before any code is ran)
// /i this also means that the function can be called before it is declared!!! function expression can not do that
function getConvStatus() {
    if (hpc.checked) {
        return "HPC";
    } else if (fo.checked) {
        return "FO/LCC";
    } else {
        return "Unknown";
    };
};

// /i function expression: are loaded when encountered (won't slow down your code if not called)
// /i can't be declared after usage
// /i handy if used in a conditional block (you are not loading when you don't need that shit)
let getPortStatus = () => {
    let temp = document.querySelectorAll("option.conv_list");
    let res;
    for (x in temp) {
        if (temp[x].selected) {
            res = temp[x].value;
        };
    };
    return res;
}

function updateEntryData(entry) {
    arg1.value = entry["arg1"];
    arg2.value = entry["arg2"];
    // bufTimeMan.value = entry["buf_time_man"];
    if (entry["conv"] == "HPC") {
        hpc.setAttribute("checked", "checked")
    } else {
        fo.setAttribute("checked", "checked")
    };
    portList = document.querySelectorAll("option[class='conv_list']"); // ! not sure if necessary to refresh
    for (i = 0; i < portList.length; i++) {
        portList[i].removeAttribute("selected") // TODO: figure out the visibility issue!
        // console.log("infor");
        if (portList[i].value == entry["sel_port"]) {
            // console.log("inif");
            portList[i].setAttribute("selected", "selected");
        }
    };
    console.log(entry);
    if (entry["ledcalib_state"][0] == "low" || entry["ledcalib_state"][0] == "high") {
        showDialogLedCalib();
    }
    pid.value = entry["pid"];
};

function getEntryData(comm, manual = false, ledcalib_state = ["off", 0]) {
    let temp = {
        "arg1": arg1.value,
        "arg2": arg2.value,
        "conv": getConvStatus(),
        "sel_port": getPortStatus(),
        "command": comm,
        // "buf_time_man": bufTimeMan.value,
        "manual": manual,
        "ledcalib_state": ledcalib_state,
        "pid": pid.value,
    };
    return JSON.stringify(temp)
};

function sendData(comm) {
    finalData.setAttribute("value", getEntryData(comm));
    finalForm.submit();
}

function sendManData() {
    let manEnt = document.getElementById("manent");
    finalData.setAttribute("value", getEntryData(manEnt.value, true));
    finalForm.submit();
}

// ! dialog in Firefox --> surf to "about:config" in webbrowser and search for dom.enable_dialog and enable this configuration parameter to be able to use

function showDialogLedCalib() {
    if (typeof dialog.showModal === 'function') {
        dialog.showModal();
        console.log("dialog showed");
    } else {
        console.log('The dialog API is not supported by this browser');
    };
};

function submitLedCalib() {
    let curr = document.getElementById("curr_input").value;
    console.log("current value: ", curr);
    let temp = ent["ledcalib_state"];
    temp[1] = curr;
    finalData.setAttribute("value", getEntryData("ledcalib", false, temp));
    finalForm.submit();
    console.log("LED current submitted");
};

function abortLedCalib() {
    console.log("LED calib aborted");
    dialog.close()
};

function testMinimize() {
    let temp = document.getElementById("comm_butt_div");
    let term = document.querySelector("#term")
    let height = getComputedStyle(term).getPropertyValue("height").match(/\d*/);
    // /i the .match(/\d/) is converting to a number with format .match(regexp) "/\d/" --> forward slashes show regexp, backslash d means look for numbers
    if (temp.hidden === true) {
        temp.hidden = false;
        target = (Number(height) - 238) + "px";
        console.log(target)
        term.style.height = target;
    } else {
        temp.hidden = true;
        target = (Number(height) + 238) + "px";
        term.style.height = target;
    }
    console.log("new height is:", term.style.height)
}

document.querySelector("#term").addEventListener("click", testMinimize, false);

// ACTIONS ON LOADING
updateEntryData(ent)