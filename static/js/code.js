function m2(text) {
	var pre = text.slice(3, text.indexOf("+")-1);
	var post = text.slice(text.indexOf("+")+2, text.indexOf("·"));
	var domain = text.slice(text.indexOf("·")+1);
	var result1 = "<span>" + pre + "&nbsp;AT&nbsp;" + post + "." + domain + "</span>";
	var result2 = pre + " AT " + post + "." + domain;
	var link = 	document.getElementsByClassName("mail2-button")[0];
	link.innerHTML = result1;
	link.setAttribute("href", "mailto:" + result2);
}
