// * Declaration of variables
let arg1 = document.querySelector("#entry_arg1")
let arg2 = document.querySelector("#entry_arg2")
let hpc = document.querySelectorAll("input[type='radio'][value='HPC']")[0]
let fo = document.querySelectorAll("input[type='radio'][value='FO/LCC']")[0]
let portList = document.querySelectorAll("option[class='conv_list']")
let finalForm = document.getElementById("finalForm");
let finalData = document.getElementById("finalData");

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
};

function getEntryData(comm) {
    let temp = {
        "arg1": arg1.value,
        "arg2": arg2.value,
        "conv": getConvStatus(),
        "sel_port": getPortStatus(),
        "command": comm,
    };
    return JSON.stringify(temp)
};

function sendData(comm) {
    finalData.setAttribute("value", getEntryData(comm))
    finalForm.submit();
}

// ACTIONS ON LOADING
updateEntryData(ent)