window.onload = function() {
    document.body.style.filter = "blur(0px)";
}
function changeColor() {//modo oscuro
    document.body.style.background="var(--gradient_2_body)";
    document.getElementById("header").style.setProperty("background-image","var(--gradient_2_header)");
    document.getElementById("titulo").innerText = "Bienvenido a C.E.D.A.A.C.";
    document.getElementById("titulo").style.setProperty("background-image", "var(..gradient_2_h1)");
    document.querySelector("titulo").style.setProperty("--webtik-background-clip","text");
    document.querySelector("titulo").style.setProperty("--webtik-text-fill-color","transparent");
    document.getElementsByClassName("Mensaje_usuario").style.setProperty("background","var(__color_2_mu_background)");
}
function returnColor(){//Modo Claro
    document.body.style.background="var(--gradient_default_body)";
    document.getElementById("header").style.setProperty("background-image","var(--gradient_default_header)");
    document.getElementById("titulo").innerText = "Bienvenido a C.E.D.A.A.C.";
    document.getElementById("titulo").style.setProperty("text-shadow", "none");
    document.getElementById("titulo").style.setProperty("background-image" , "var(--gradient_default_h1)");
    document.querySelector("titulo").style.setProperty("--webtik-background-clip", "text");
    document.querySelector("titulo").style.setProperty("--webtik-text-fill-color", "transparent");
}