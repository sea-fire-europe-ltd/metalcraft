$(document).ready(function(){
	let sheet = document.createElement('style');
	sheet.setAttribute('id','fullsizestyle');
	sheet.innerHTML = ".container {width: 100% !important;}";
	document.body.appendChild(sheet);
});
