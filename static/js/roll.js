window.onload = roll;

function showenchants() {
    //toggle enchantments when hovering over item
    var x = document.getElementById("enchants");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
}

function roll() {
    //the animation
    var box1 = document.getElementById("box1");
    var box2 = document.getElementById("box2");
    var box3 = document.getElementById("box3");
    var box4 = document.getElementById("box4");
    const boxes = [box1, box2, box3, box4];
    const time = Math.floor(Math.random() * 2000)+4000;

    setTimeout(() => {
        boxes.forEach(box => {
            box.style.animation = 'none'; // stop animation
            hide(box);

            var text = document.getElementById("spinning");
            text.style.display="none";

            var item = document.getElementsByClassName('pick_item');
            for (var i = 0; i < item.length; i ++) {
                item[i].style.display = 'block';
            }
        });
    }, time);
}

//hide the black boxes
function hide(x) {
    x.style.display="none";
}