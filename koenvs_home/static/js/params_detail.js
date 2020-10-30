function getData() {
    let paramList = document.querySelectorAll(".param");
    temp = JSON;
    paramList.forEach(e => {
        input = e.getElementsByTagName("input")[0].value;
        label = e.getElementsByClassName("param_label")[0].innerHTML;
        labelClean = label.replace(/\W/g, "");
        temp[labelClean] = input;
    });
    return temp;
}



