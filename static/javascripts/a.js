const img = document.querySelector("#slider");
const arr = ["dalat.jpg", "halong.jpg", "landmark.jpg"];
let i = 0
setInterval(()=>{
    i++;
    if(i > 2) i=0;
    img.style.backgroundImage = `url('../static/images/${arr[i]}')`
    console.log(img.src)
    return
}, 5000);
