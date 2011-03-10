	
//********************************
//Ajax-Register-Lab Feature
//********************************
	
X$('TeacherRegister',
{
	labList 		: undefined,
	lessonName 		: undefined,
	lessonDay 		: undefined,
	lessonHourStart : undefined,
	lessonHourEnd 	: undefined,
	
	thirdStep		: undefined,
	lessonClass 	: undefined,
	maxSlider 		: undefined,
	maxStudents 	: undefined,
	modalMsg 		: undefined,
	submitLab 		: undefined,
	msg				: {1:"ok", 2:"error", 3:"warning"},


	init: function() {
		var _self = this;
		
		_self.labList 		= $("#lab-registration");
		_self.lessonName 	= $("#select-lesson select[name='lesson-name']");
		_self.lessonDay 	= $("#select-lab select[name='lesson-day']");
		_self.lessonHourStart 	= $("#select-lab select[name='lesson-hour-start']");
		_self.lessonHourEnd 	= $("#select-lab select[name='lesson-hour-end']");
		_self.thirdStep		= $("#select-class");
		_self.lessonClass 	= $("#select-class select[name='lesson-class']");
		_self.maxSlider 	= $("#slider-max-students");
		_self.maxStudents 	= $("#max-students");
		_self.modalMsg 		= $("#modal-messages");
		_self.submitLab 	= $("#submit-lab");
		
		_self.stepify().setEvents();
		
		return this;
	},
	
	
	removeFocus: function(){
		var _self = this;
		_self.labList.find("li.focused").removeClass("focused");
	},
	
	
	stepify: function(){
		var _self = this;
		
		_self.lessonDay.attr("disabled", "disabled").parent("li").addClass("disabled");
		_self.lessonHourStart.attr("disabled", "disabled");
		_self.lessonHourEnd.attr("disabled", "disabled");
		_self.lessonClass.attr("disabled", "disabled").parent("li").addClass("disabled").hide();
		_self.modalMsg.find("#modal-loader").hide().siblings("p").hide();
		_self.maxSlider.slider({ range: "min", min: 5, max: 40, value: 20,
								slide: function( event, ui ) {
									_self.maxStudents.val(ui.value);
								}
							});
		_self.maxStudents.val( _self.maxSlider.slider("value") );
		_self.submitLab.hide();
		
		_self.labList.find("li>h3").click(function() {
			if ( $(this).parent("li").hasClass("isset") && !$(this).parent("li").hasClass("disabled") ){
				_self.removeFocus();
				$(this).parent("li").addClass("focused").find("select").first().focus();
			}
			return false;
		});
		
		return this;
	},
	
	
	cleanMessages: function() {
		var _self = this;
		_self.modalMsg.find("p").fadeOut(100).delay(100).removeClass();
		
		return this;
	},
	
	showMessage: function(status, new_msg, new_speed) {
		var _self = this;
		var speed = new_speed || 150;
		
		_self.cleanMessages().modalMsg.find("p").addClass(_self.msg[status]).text(new_msg).fadeIn(speed);
	},
	
	setEvents: function(){
		var _self = this;
		var	lessonToSend,
			dayToSend,
			hourToSend = {start: 1, end: 1},
			classToSend;
		
		_self.lessonName.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
		
				hisParent.removeClass("focused");
				lessonToSend = $(this).val();
				
				_self.lessonDay.parent("li").removeClass("disabled").addClass("focused").addClass("isset");
				_self.lessonDay.removeAttr("disabled").focus();
				_self.lessonHourStart.removeAttr("disabled");
				_self.lessonHourEnd.removeAttr("disabled");
			
				hisParent.addClass("isset");	
			} else {
				lessonToSend = $(this).val();
			}
			_self.cleanMessages();
		});
	
		_self.lessonDay.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
		
				dayToSend = $(this).val();
			
				if( !hisParent.hasClass("isset" ) ) {
					hisParent.addClass("isset");
				}
			
			} else {
				dayToSend = $(this).val();
			}
			if( dayToSend && hourToSend.start!==1 && hourToSend.end!==1 ){
				classToSend = null;
				_self.submit(dayToSend, hourToSend);
			}
			_self.cleanMessages();
		});
	
		_self.lessonHourStart.change(function() {
			var start,
				hisParent = $(this).parent("li");
			
			if ( !hisParent.hasClass("isset") ){
		
				start = $(this).attr("value");
				
				if( !hisParent.hasClass("isset" ) ) {
					hisParent.addClass("isset");
				}
			
			} else {
				start = $(this).attr("value");
			}
			hourToSend.start = parseInt(start, 10);
			
			if( dayToSend && hourToSend.start!==1 && hourToSend.end!==1 ){
				classToSend = null;
				_self.submit(dayToSend, hourToSend);
			}
			_self.cleanMessages();
		});
		
		_self.lessonHourEnd.change(function() {
			var end,
				hisParent = $(this).parent("li");
			
			if ( !hisParent.hasClass("isset") ){
		
				end = $(this).attr("value");
				
				if( !hisParent.hasClass("isset" ) ) {
					hisParent.addClass("isset");
				}
			
			} else {
				end = $(this).attr("value");
			}
			hourToSend.end = parseInt(end, 10);
			if( dayToSend && hourToSend.start!==1 && hourToSend.end!==1 ){
				classToSend = null;
				_self.submit(dayToSend, hourToSend);
			}
			_self.cleanMessages();
		});

		this.lessonClass.change(function() {
			var hisParent = $(this).parent("li");
			if ( !hisParent.hasClass("isset") ){
		
				classToSend = $(this).val();
				hisParent.addClass("isset");
		
			} else {
				classToSend = $(this).val();
			}
			_self.cleanMessages();
		});
	
		var submitLabRequest = function() {
			if ( lessonToSend && dayToSend && hourToSend.start && hourToSend.end && classToSend ) {
				_self.submitLab.unbind("click");
				_self.modalMsg.find("p").hide().removeClass().siblings("img").fadeIn(50);
				_self.submit(dayToSend, hourToSend, lessonToSend, classToSend);
				setTimeout( function() {
					_self.submitLab.bind("click", submitLabRequest);
				},1900);
			}
			else {
				var ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
				_self.showMessage(2, ms, 200);
			}
			return false;
		};
		_self.submitLab.bind("click", submitLabRequest);
		
		return this;
	},


	submit: function(dayToSend, hourToSend, lessonToSend, classToSend) {
		var _self = this,
			request,
			maxToSend = _self.maxSlider.slider("value");
		
		if (classToSend) 	{ request = { action: "submitLab", newName: lessonToSend, newDay: dayToSend, newHour: hourToSend, newClass: classToSend, maxStudents: maxToSend }; }
		else 				{ request = { action: "getClass", newDay: dayToSend, newHour: hourToSend }; }
		
		var ajaxUrl = '/teachers/'+X$('Helpers').getHash()+'/add-new-lab/';
		$.ajax({
			url: ajaxUrl,
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			data: $.toJSON(request),
			dataType: 'json',
			timeout: 10000,
			beforeSend: function() {
				if (request.action == "submitLab") { _self.modalMsg.find("#modal-loader").show(); }
			},
			success: function(data) {
				try {
					if (data[0].status == 1){

						if (data[0].action == "getClass") {
							_self.lessonClass.children().not(":first-child").remove();
							var len = data[0].classes.length;
							for(var i=0; i<len; i++){
								var str = "<option value='"+data[0].classes[i].name+"'>"+data[0].classes[i].name+"</option>";
								_self.lessonClass.append(str);
							}
							var parentClass = _self.lessonClass.parent("li");
							var parentMeridiam = _self.lessonDay.parent("li");
					
							parentClass.removeClass("disabled");
							_self.lessonClass.removeAttr("disabled");
						
							if ( !parentClass.hasClass("isset") ) {
								parentClass.addClass("focused").addClass("isset");
								parentMeridiam.removeClass("focused");
							
								var boxHeight = parentClass.height();
								parentClass.children().hide();
								parentClass.height(30).fadeIn(350,
													function(){
														$(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
													});
								_self.submitLab.fadeIn(350);
							
								setTimeout( function() {
									_self.lessonClass.focus();
								},900);	
							} else { _self.lessonClass.focus(); }
						}
						else if (data[0].action == "submitLab") {
							_self.modalMsg.find("#modal-loader").fadeOut(150, function(){
																	_self.modalMsg.find("p")
																	.addClass("ok")
																	.text(data[0].msg).append("<a href='#' onClick='window.location.reload()'>ανανέωση</a>")
																	.fadeIn(200);
																}
															);
						}
					}
					else if (data[0].status == 2){
				
						if (data[0].action == "getClass") {
							_self.showMessage(data[0].status, data[0].msg, 200);
						}
						else if (data[0].action == "submitLab") {
							_self.modalMsg.find("#modal-loader").fadeOut(150, function(){
																	_self.showMessage(data[0].status, data[0].msg, 200);
																}
															);
						}
					}
				}
				catch(e) { this.error(); }
			},
			error: function(xhr, err){
				var ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
				//if(xhr.status==500)
				_self.modalMsg.find("#modal-loader").fadeOut(150);
				setTimeout( function() {
					_self.showMessage(2, ms);
				},400);
			}
		});
		
	}

});

