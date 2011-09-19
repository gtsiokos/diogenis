    
//********************************
//Ajax-Register-Lab Feature
//********************************

X$('StudentRegister',
{
    $lab_registration   : undefined,
    $select             :   {
                            lesson:undefined,
                            teacher:undefined,
                            lab:undefined
                            },
    $modal_messages     : undefined,
    $loader             : undefined,
    $submit_lab         : undefined,


    init: function() {
        var self = this;
        
        self.$lab_registration  = $('#lab-registration');
        self.$select.lesson     = $('#select-lesson select[name="lesson-name"]');
        self.$select.teacher    = $('#select-teacher select[name="lesson-teacher"]');
        self.$select.lab        = $('#select-class select[name="lesson-class"]');
        self.$modal_messages    = $('#modal-messages');
        self.$loader            = $('#modal-loader');
        self.$submit_lab        = $('#submit-lab');
        
        var spinner = X$('Helpers').get_spinner();
        self.$loader.spin(spinner.options);
        
        self.stepify().handle_events();
        
        return this;
    },
    
    
    remove_focus: function(){
        var self = this;
        self.$lab_registration.find('li.focused').removeClass('focused');
    },
    
    
    stepify: function(){
        var self = this;
        
        self.$select['teacher'].attr('disabled', 'disabled').parent('li').addClass('disabled');
        self.$select['lab'].attr('disabled', 'disabled').parent('li').addClass('disabled').hide();
        self.$modal_messages.find('p').hide();
        self.$loader.hide();
        self.$submit_lab.hide();

        self.$lab_registration.find('li>h3').click(function() {
            if ( $(this).parent('li').hasClass('isset') && !$(this).parent('li').hasClass('disabled') ){
                self.remove_focus();
                $(this).parent('li').addClass('focused').find('select').first().focus();
            }
            return false;
        });
        
        return this;
    },
    
    
    clean_messages: function() {
        var self = this;
        self.$modal_messages.find('p').fadeOut(100).delay(100).removeClass();
    },
    
    
    handle_events: function(){
        var self = this,
            lesson='',
            teacher='',
            lab='',
            submit=false;
        
        self.$select['lesson'].change(function() {
            var $this = $(this).find(':selected'),
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            lesson = ($this.val()) ? $this.data() : '';
            
            if( lesson ){
                self.submit({lesson:lesson});
            }
        
            self.$submit_lab.hide();
            self.clean_messages();
        });
    
        self.$select['teacher'].change(function() {
            var $this = $(this).find(':selected'),
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            teacher = ($this.val()) ? $this.data() : '';
            
            if( lesson && teacher ){
                self.submit({lesson:lesson, teacher:teacher});
            }
            self.clean_messages();
        });
    
        self.$select['lab'].change(function() {
            var $this = $(this).find(':selected'),
                parent = $(this).parent('li'),
                step_is_not_set = !parent.hasClass('isset');
            
            if ( step_is_not_set ) parent.addClass('isset');
            lab = ($this.val()) ? $this.data() : '';
            
            if( lesson && teacher && lab ){
                self.submit({lesson:lesson, teacher:teacher, lab:lab, submit:false});
            }
            self.clean_messages();
        });
    
        var submit_lab_request = function() {
            if ( lesson && teacher && lab ) {
                self.$submit_lab.unbind('click');
                self.$modal_messages.find('p').hide().removeClass().siblings('img').fadeIn(50);
                self.submit({lesson:lesson, teacher:teacher, lab:lab, submit:true});
                setTimeout( function() {
                    self.$submit_lab.bind('click', submit_lab_request);
                },1900);
            }
            else {
                var ms = "Παρακαλώ συμπληρώστε τα στοιχεία του εργαστηρίου";
                self.clean_messages();
                self.$modal_messages.find('p').addClass('error').text(ms).fadeIn(200);
            }
            return false;
        };
        self.$submit_lab.bind('click', submit_lab_request);
        
        return this;
    },


    submit: function(r) {
        var self = this,
            request;
        
        if (r.lesson && r.teacher && r.lab){
            if (r.submit) {
                request = {
                            //type:'PUT'
                            action:'submit',
                            lab_id:r['lab'].id
                          };
            }
            else {
                request = {
                            //type:'GET'
                            action:'availability',
                            lab_id:r['lab'].id
                          };
            }
        }
        else if (r.lesson && r.teacher){
            request = { 
                        //type:'GET',
                        action:'classes',
                        course_id:r['lesson'].id,
                        teacher_id:r['teacher'].id
                      };
        }
        else if (r.lesson){
            request = {
                        //type:'GET',
                        action:'teachers',
                        course_id:r['lesson'].id
                      };
        }
        //console.log(request);
        var ajax_url = '/students/add-new-lab/';
        $.ajax({
            url: ajax_url,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(request),
            dataType: 'json',
            timeout: 10000,
            beforeSend: function() {
                if (request.action == 'submit') { self.$loader.show(); }
            },
            success: function(data) {
                if (data.status == 1){
                    var strHtml;
                    
                    if (data.action == 'teachers') {
                        self.$select['teacher'].children().not(':first-child').remove();
                        self.$select['lab'].attr('disabled', 'disabled').parent('li')
                                                                    .removeClass('isset').hide().end()
                                                                    .children().not(':first-child').remove();
                        
                        var list_html = '';
                        for(var i=0, teacher; teacher=data.teachers[i]; i++){
                            list_html += '<option data-id="'+teacher.id+'" value="'+teacher.name+'">'+teacher.name+'</option>';
                        }
                        self.$select['teacher'].append(list_html);
                        
                        var parentClass = self.$select['teacher'].parent('li');
                        parentClass.removeClass('disabled');
                        
                        self.remove_focus();
                        if ( !parentClass.hasClass('isset') ) {
                            parentClass.addClass('focused').addClass('isset');
                            self.$select['teacher'].removeAttr('disabled');
                            
                            setTimeout( function() {
                                self.$select['teacher'].focus();
                            },900);    
                        } else { parentClass.addClass('focused'); self.$select['teacher'].focus(); }
                    }
                    else if (data.action == 'classes') {
                        self.$select['lab'].children().not(':first-child').remove();
                        
                        var list_html = '';
                        for(var i=0, lab; lab=data.classes[i]; i++){
                            var str = '['+lab.start_hour+' με '+lab.end_hour+'] '+lab.day+' - '+lab.lesson;
                            list_html += '<option data-id="'+lab.id+'" value="'+str+'">'+str+'</option>';
                        }
                        self.$select['lab'].append(list_html);
                        
                        var parentClass = self.$select['lab'].parent('li');
                        parentClass.removeClass('disabled');
                        
                        self.remove_focus();
                        if ( !parentClass.hasClass('isset') ) {
                            parentClass.addClass('focused').addClass('isset');
                            self.$select['lab'].removeAttr('disabled');
                            
                            var boxHeight = parentClass.height();
                            parentClass.children().hide();
                            parentClass.height(30).fadeIn(350,
                                                function(){
                                                    $(this).animate({height: boxHeight}, 350).children().delay(500).fadeIn(350);
                                                });
                            
                            setTimeout( function() {
                                self.$select['lab'].focus();
                            },900);
                        } else { parentClass.addClass('focused'); self.$select['lab'].focus(); }
                    }
                    else if (data.action == 'availability') {
                        self.$submit_lab.text("Υποβολή").fadeIn(350);
                    }
                    else if (data.action == 'submit') {
                        self.$loader.hide();
                        self.$modal_messages.find('p').addClass('ok').text(data.msg)
                                            .append('<a href="#" onClick="window.location.reload()">ανανέωση</a>')
                                            .fadeIn(200);
                    }
                }
                else if (data.status == 3){
                    if (data.action == 'availability') {
                        self.$modal_messages.find('p').addClass('warning').text(data.msg).fadeIn(200);
                        self.$submit_lab.text("Υποβολή Αιτήματος").fadeIn(350);
                    }
                }
                else if (data.status == 2){
                
                    if (data.action == 'teachers') {
                        self.$modal_messages.find('p').addClass('error').text(data.msg).fadeIn(200);
                    }
                    else if (data.action == 'classes') {
                        self.$select['lab'].attr('disabled', 'disabled').children().not(':first-child').remove();
                        self.$submit_lab.hide();
                        self.$select['lab'].parent('li').hide().removeClass('isset').removeClass('focused').addClass('disabled');
                        self.$modal_messages.find('p').addClass('error').text(data.msg).fadeIn(200);
                    }
                    else if (data.action == 'submit') {
                        self.$loader.hide();
                        self.$modal_messages.find('p').addClass('error').text(data.msg).fadeIn(200);
                                                            
                    }
                }
            },
            error: function(xhr, err){
                var ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
                if(xhr.status==500){
                    self.$loader.hide();
                    self.$modal_messages.find('p').addClass('error').text(ms).fadeIn(200);
                }
            }
        });
        
    }

});
