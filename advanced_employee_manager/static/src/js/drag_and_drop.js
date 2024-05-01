document.addEventListener("DOMContentLoaded", function() {
    console.log("111111111111111111");
    let lists = document.getElementsByClassName("list");
    let right = document.getElementById("right");
    let left = document.getElementById("left");

    console.log("Lists: ", lists.length);
    console.log("Right: ", right);
    console.log("Left: ", left);

    if (right && left) {
        right.addEventListener("dragover", function(e) {
            e.preventDefault();
        });

        left.addEventListener("dragover", function(e) {
            e.preventDefault();
        });

        for(let list of lists) {
            list.addEventListener("dragstart", function(e) {
                let selected = e.target;

                right.addEventListener("drop", function(e) {
                    right.appendChild(selected);
                    selected = null;
                });

                left.addEventListener("drop", function(e) {
                    left.appendChild(selected);
                    selected = null;
                });
            });
        }
    } else {
        console.error('Elements with id "right" or "left" not found');
    }
});