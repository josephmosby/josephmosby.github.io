function animateIntro() {    	
		setTimeout(function() {
			$("#development_link").fadeIn();}, 1000);
		setTimeout(function() {	
			$("#security_link").fadeIn();}, 2000);
		setTimeout(function() {	
			$("#digital_link").fadeIn();}, 3000);
		
		setTimeout(function() {
			$("#about_link").fadeIn();}, 5000);
		
		$("#development_link").hover(function(){
			$('#development_text').fadeIn();
		},function(){
			$('#development_text').hide();
		});
		
		$("#security_link").hover(function(){
			$('#security_text').fadeIn();
		},function(){
			$('#security_text').hide();
		});

		$("#digital_link").hover(function(){
			$('#digital_text').fadeIn();
		},function(){
			$('#digital_text').hide();
		});	
							
		$("#about_link").hover(function(){
			$('#about_text').fadeIn();
		},function(){
			$('#about_text').hide();
		});	
}

function addMenuText(link_id) {
	$(link_id).hover(function() {
		$(link_id).addClass("menu_text");
		$(link_id).removeClass("link_dot");
		switch(link_id) {
			case "#home_menu_dot":
				$(link_id).html("home");
				break;
			case "#dev_menu_dot":
				$(link_id).html("development");
				break;
			case "#security_menu_dot":
				$(link_id).html("security");
				break;
			case "#digital_menu_dot":
				$(link_id).html("digital");
				break;
			case "#about_menu_dot":
				$(link_id).html("about");
				break;
		}
	}, function() {
		$(link_id).addClass("link_dot");
		$(link_id).removeClass("menu_text");
		$(link_id).empty();
	});
}

function setCookie(c_name, value, exdays) {
	var exdate = new Date();
	exdate.setDate(exdate.getDate() + exdays);
	var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
	document.cookie=c_name + "=" + c_value;
}

function getCookie(c_name) {
	var c_value = document.cookie;
	var c_start = c_value.indexOf(" " + c_name + "=");
	if (c_start == -1) {
		c_start = c_value.indexOf(c_name + "=");
	}
	
	if (c_start == -1) {
		c_value = null;
	} else {
		c_start = c_value.indexOf("=", c_start) + 1;
		var c_end = c_value.indexOf(";", c_start); 
		if (c_end == -1) {
			c_end = c_value.length;
		}
		
		c_value = unescape(c_value.substring(c_start, c_end));
	}
	
	return c_value;
}