function printSomething(data) {
    console.log(data);
}

function updateEntryData(entry) {
    document.querySelector("#entry_arg1").value = entry["arg1"];
    document.querySelector("#entry_arg2").value = entry["arg2"];
    if (entry["conv"] == "HPC") {
        document.querySelectorAll("input[type='radio'][value='HPC']")[0].setAttribute("checked", "checked")
    } else {
        document.querySelectorAll("input[type='radio'][value='FO/LCC']")[0].setAttribute("checked", "checked")
    };
    let tempList = document.querySelectorAll("option[class='conv_list']");
    for (i = 0; i < tempList.length; i++) {
        tempList[i].removeAttribute("selected") // TODO: figure out the visibility issue!
        // console.log("infor")
        if (tempList[i].value == entry["sel_port"]) {
            // console.log("inif")
            tempList[i].setAttribute("selected", "selected")
        }
    };
    console.log(entry);
};

// ACTIONS ON LOADING
updateEntryData(ent)