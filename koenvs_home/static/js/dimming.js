let listChecks = document.querySelectorAll(".checkbox");
for (e in selected) {
    for (f in listChecks) {
        console.log(f);
        if (f.value == e) {
            console.log("match");
        } else {
            console.log("no match");
        }
    }
}