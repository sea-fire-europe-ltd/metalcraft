$(document).ready(function(){
	let sheet = document.createElement('style');
	sheet.setAttribute('id','fullsizestyle');
	sheet.innerHTML = ".container {width: 90% !important;}";
	document.body.appendChild(sheet);
});
