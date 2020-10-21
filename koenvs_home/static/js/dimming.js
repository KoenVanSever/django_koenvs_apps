let listChecks = document.querySelectorAll(".checkbox");

selected.forEach(sel => {
    listChecks.forEach(check => {
        if (sel == check.value) {
            check.checked = true;
        };
    });
});