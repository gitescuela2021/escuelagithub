$(function(){
	var enlace = $('#link_busqueda');
	enlace.on('click',function(){
		var texto = $('#tx_busqueda');
		enlace.attr('href','http://127.0.0.1:8000/visitante/lista_cursos_busqueda?criterio=' + texto.val());
	});
}())
