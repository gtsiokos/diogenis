$(function(){

	//********************************
	//Find Login Hash
	//********************************	
	
	var hashValue = $("input[type='hidden']", "#login").val();
	
	//********************************
	//Global Ajax Behaviour
	//********************************		
	
	var theBody = $("body:first");
	
	theBody.ajaxStart(function(){
		theBody.addClass("wait");
	});
	theBody.ajaxComplete(function(){
		theBody.removeClass("wait");
	});
	
	var splitDate = function(date) {
		var date = date.split(" ");
		var day = date[0];
		var hour = parseInt(date[1], 10);
		var AmPm = date[2];
		if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
			hour = hour;
		} else { hour = hour+12; }
		
		return {day:day, hour:hour};
	}
	
	
	//********************************
	//Ajax-Register-Lab Feature
	//********************************
	
	var labList 		= $("#lab-registration");
	var lessonName 		= $("#select-lesson select[name='lesson-name']");
	var lessonTeacher	= $("#select-teacher select[name='lesson-teacher']");
	var lessonClass 	= $("#select-class select[name='lesson-class']");
	var modalMsg 		= $("#modal-messages");
	var submitLab 		= $("#submit-lab");
	
	lessonTeacher.attr("disabled", "disabled").parent("li").addClass("disabled");
	lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
	modalMsg.find("#modal-loader").hide().siblings("p").hide();
	submitLab.hide();
	var unfocusSteps = function() { labList.find("li.focused").removeClass("focused"); };

	labList.find("li>h3").click(function() {
		if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
			unfocusSteps();
			$(this).parent("li").addClass("focused").find("select").first().focus();
		}
		return false;
	});
	
	var lessonToSend, teacherToSend, classToSend;
	var theRequest = function(lessonToSend, teacherToSend, classToSend) {
		
		if (lessonToSend && teacherToSend && classToSend){
			var classInfo 	= classToSend.split(" ");
			var classDate 	= splitDate(classToSend);
			var className 	= classInfo[3];
			var classDay 	= classDate.day;
			var classHour 	= classDate.hour;
			var request = { action:"submitLab", lesson:lessonToSend, teacher:teacherToSend, cname:className, cday:classDay, chour:classHour };
		}
		else if (lessonToSend && teacherToSend){
			var request = { action:"getClasses", lesson:lessonToSend, teacher:teacherToSend };
		}
		else if (lessonToSend){
			var request = { action:"getTeachers", lesson:lessonToSend };
		}
		
		ajaxUrl = '/students/'+hashValue+'/add-new-lab/';
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			success: function(data) {
				if (data[0].status == 1){
					var strHtml
					
					if (data[0].action == "getTeachers") {
						lessonTeacher.children().not(":first-child").remove();
						lessonClass.attr("disabled", "disabled").parent("li")
																	.removeClass("isset").hide().end()
																	.children().not(":first-child").remove();
						var len = data[0].teachers.length;
						for(var i=0; i<len; i++){
							strHtml += "<option value='"+data[0].teachers[i].name+"'>"+data[0].teachers[i].name+"</option>";
						}
						lessonTeacher.append(strHtml);
						
						var parentClass = lessonTeacher.parent("li");
						parentClass.removeClass("disabled");
						
						unfocusSteps();
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							lessonTeacher.removeAttr("disabled");
							
							setTimeout( function() {
								lessonTeacher.focus();
							},900);	
						} else { parentClass.addClass("focused"); lessonTeacher.focus(); }
					}
					else if (data[0].action == "getClasses") {
						lessonClass.children().not(":first-child").remove();
						var len = data[0].classes.length;
						for(var i=0; i<len; i++){
							var str 	= data[0].classes[i].day+" - "+data[0].classes[i].hour+" - "+data[0].classes[i].name;
							var strVal 	= data[0].classes[i].day+" "+data[0].classes[i].hour+" "+data[0].classes[i].name;
							strHtml += "<option value='"+strVal+"'>"+str+"</option>";
						}
						lessonClass.append(strHtml);
						
						var parentClass = lessonClass.parent("li");
						parentClass.removeClass("disabled");
						
						unfocusSteps();
						if ( !parentClass.hasClass("isset") ) {
							parentClass.addClass("focused").addClass("isset");
							lessonClass.removeAttr("disabled");
							
							var boxHeight = parentClass.height();
							parentClass.children().hide();
							parentClass.height(30).fadeIn(350,
												function(){
													$(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
												});
							submitLab.fadeIn(350);
							
							setTimeout( function() {
								lessonClass.focus();
							},900);
						} else { parentClass.addClass("focused"); lessonClass.focus(); }
					}
					else if (data[0].action == "submitLab") {
						modalMsg.find("#modal-loader").fadeOut(150, function(){
																modalMsg.find("p")
																.addClass("ok")
																.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>ανανέωση</a>")
																.fadeIn(200);
															}
														);
					}
				}
				else if (data[0].status == 2){
				
					if (data[0].action == "getTeachers") {
						modalMsg.find("p").addClass("error").text(data[0].msg).fadeIn(200);
					}
					else if (data[0].action == "getClasses") {
						lessonClass.attr("disabled", "disabled").children().not(":first-child").remove();
						submitLab.hide();
						lessonClass.parent("li").hide().removeClass("isset").removeClass("focused").addClass("disabled");
						modalMsg.find("p").addClass("error").text(data[0].msg).fadeIn(200);
					}
					else if (data[0].action == "submitLab") {
						modalMsg.find("#modal-loader").fadeOut(150, function(){
																modalMsg.find("p")
																.addClass("error")
																.text(data[0].msg)
																.fadeIn(200);
															}
														);
					}
				}
			},
			error: function(xhr, err){
				ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
				if(xhr.status==500){
					modalMsg.find("#modal-loader").fadeOut(150);
					setTimeout( function() {
						modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
					},400);
				}
			}
		});
		
		
	};
	
	var cleanMessages = function() {
		modalMsg.find("p").fadeOut(100).delay(100).removeClass();
	}
	
	lessonName.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
			lessonToSend = $(this).val();
			hisParent.addClass("isset");	
		} else {
			lessonToSend = $(this).val();
		}
		theRequest(lessonToSend);
		
		cleanMessages();
	});
	
	lessonTeacher.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
			teacherToSend = $(this).val();
			hisParent.addClass("isset");	
		} else {
			teacherToSend = $(this).val();
		}
		if( lessonToSend && teacherToSend ){
			classToSend = null;
			theRequest(lessonToSend, teacherToSend);
		}
		cleanMessages();
	});
	
	lessonClass.change(function() {
		var hisParent = $(this).parent("li");
		if ( !hisParent.hasClass("isset") ){
			classToSend = $(this).val();
			hisParent.addClass("isset");
		} else {
			classToSend = $(this).val();
		}
		cleanMessages();
	});
	
	var submitLabRequest = function() {
		if ( lessonToSend && teacherToSend && classToSend ) {
			submitLab.unbind("click");
			modalMsg.find("p").hide().removeClass().siblings("img").fadeIn(50);
			theRequest(lessonToSend, teacherToSend, classToSend);
			setTimeout( function() {
				submitLab.bind("click", submitLabRequest);
			},1900);
		}
		else {
			ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
			cleanMessages();
			modalMsg.find("p").addClass("error").text(ms).fadeIn(200);
		}
		return false;
	}
	submitLab.bind("click", submitLabRequest);
	




















});

