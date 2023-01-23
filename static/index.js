let intervalId;
function checkEmpty(inputField) {
  if (inputField.value.trim() == "") {
    // Mostrar un mensaje de error al usuario
    alert("Por Favor Escribe En el cuadro de texto!");
    return false;
  }
  return true;
}
document.getElementById("chat-form").addEventListener("submit", function(event) {
  event.preventDefault(); // Se encarga de que el submit o enviar se haya ejecutado
   // Validar el campo de mensaje
   if (!checkEmpty(document.getElementById("message"))) {
    return;
  }
  var message = document.getElementById("message").value;
  fetch("/chatbot", {//fetch se encarga de las peticiones y la conexion con python
    method: "POST",
    body: JSON.stringify({ message: message }),// envia el mensaje a python de manera string
    headers: {
      "Content-Type": "application/json"// el contenido que se va a enviar de tipo json
    
    }
  }).then(function(response) {// en el caso de que se retorne la funcion guarda el texto de la respuesta ("response")
    return response.text()
  }).then(function(response) {
    // Proceso de entrada y salida | Mensaje del usuario y respuesta
    // Datos introducidos por el usuario
    var s =document.createElement('p');
    s.className='Mensaje_usuario';//Crea una clase del parrafo "Respuesta_bot"
    s.innerText=message;

    document.getElementById('respuesta2').appendChild(s)
    document.getElementById('chatborder').scrollTop = document.getElementById('chatborder').scrollHeight;//posiciona al ultimo mensaje
  

//Respuesta de la IA
var p = document.createElement('p');
p.className='Respuesta_bot';//Crea una clase del parrafo "Respuesta_bot"
p.innerText='';
document.getElementById('respuesta2').appendChild(p);

// Función para escribir la respuesta caractér por caractér
function writeResponse(response) {
  clearInterval(intervalId);
  let charIndex = 0;
  intervalId = setInterval(() => {
    p.innerText += response[charIndex];
    charIndex++;
    document.getElementById('chatborder').scrollTop = document.getElementById('chatborder').scrollHeight;
    if (charIndex === response.length) {
      clearInterval(intervalId);
    }
  }, 75);
}
// Llamar a la función para escribir la respuesta
writeResponse(response);
  });

  // Clear the message field
  document.getElementById("message").value = "";
}
);