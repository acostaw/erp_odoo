function satisfecho() {
    var rating= document.querySelector('.rating');
    rating.textContent='Satisfecho'
    document.querySelector(".ratingForm").value = 'Satisfecho'
    var imagen = document.querySelector(".imagen");
    imagen.src = "/intn_informe_bascula/static/src/img/rating_10.png";
    var smile = document.querySelector('.smile');
    smile.style.display = 'none';
    var feedback = document.querySelector('.feedback-div');
    feedback.style.display = 'block';
}
function no_satisfecho(){
    var rating= document.querySelector('.rating');
    rating.textContent='No Satisfecho'
    document.querySelector(".ratingForm").value = 'No Satisfecho'
    var imagen = document.querySelector(".imagen");
    imagen.src = "/intn_informe_bascula/static/src/img/rating_5.png";
    var smile = document.querySelector('.smile');
    smile.style.display = 'none';
    var feedback = document.querySelector('.feedback-div');
    feedback.style.display = 'block';
}
function muy_insatisfecho(){
    var rating= document.querySelector('.rating');
    rating.textContent='Muy Insatisfecho'
    document.querySelector(".ratingForm").value = 'Muy Insatisfecho'
    var imagen = document.querySelector(".imagen");
    imagen.src = "/intn_informe_bascula/static/src/img/rating_1.png";
    var smile = document.querySelector('.smile');
    smile.style.display = 'none';
    var feedback = document.querySelector('.feedback-div');
    feedback.style.display = 'block';
}
function enviarComentario(){
    var rating= document.querySelector('.ratingForm');
    if ( rating.value !='Satisfecho'){
        alert('Por favor, antes de enviar su calificación deje un comentario');
    }else{
        var feedback = document.querySelector('.feedback-div');
        feedback.style.display = 'none';
        var despedida = document.querySelector('.despedida');
        despedida.style.display = 'block';
        document.getElementById("formCalificacion").submit();
    }
}