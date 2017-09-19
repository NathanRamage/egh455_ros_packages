const imgs = ['../images/dog.jpg','../images/dog1.jpg','../images/dog2.jpg','../images/dog3.jpg','../images/dog4.jpg','../images/dog5.jpg','../images/dog6.jpg',
'../images/dog7.jpg','../images/dog8.jpg']

let imageList = document.getElementById('allImages')
let enlargedImage = document.getElementById('enlargedImage')

function loadImages() {
  enlargedImage.src = imgs[0]

  imgs.forEach(function(img) {
    let div = document.createElement('div')
    div.className = "w3-card-4"
    div.style.padding = "1em"
    div.style.backgroundColor = "white"
    div.style.marginTop = "1.5em"

    let imgEL = document.createElement('img')
    imgEL.addEventListener('click', changePicture)
    imgEL.src = img

    div.appendChild(imgEL)
    imageList.appendChild(div)
  })
}

function changePicture(e) {
  console.log(e);
  enlargedImage.src = e.target.src
}
