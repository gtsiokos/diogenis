    
//********************************
//Ajax-Register-Lab Feature
//********************************
    
X$('TeacherAbsences',
{
    $absences_widget        : $('#content>div.lab td.absences'),
    $active_widget          : undefined,
    $messages         : $('#ui-messages'),
    templates               : {
                                absences:$('#absences-tpl').html()
                              },
    msg                     : {1:'ok', 2:'error', 3:'warning'},


    init: function() {
        var self = this;
        
        self.render = X$('Helpers').render;
        self.events = self.handle_events();
        
        self.listen_events();
        
        return this;
    },
    
    clean_messages: function() {
        var self = this;
        self.$messages.find('p').fadeOut(100).delay(100).removeClass();
        
        return this;
    },
    
    show_message: function(status, new_msg, new_speed) {
        var self = this,
            speed = new_speed || 150;
        
        self.clean_messages().$messages.find('p').addClass(self.msg[status]).text(new_msg).fadeIn(speed);
    },
    
    handle_events: function(){
        var self = this;
        
        var update_absences = function(e){
            var $this = $(this),
                subscription = $this.parent().data(),
                request = {},
                option =    {
                            add: $this.hasClass('add'),
                            remove: $this.hasClass('remove')
                            };
            
            self.$active_widget = $this.parents('td.absences');
            
            if(option['add']){
                request = {action:'add', subscription:subscription};
            }
            if(option['remove']){
                request = {action:'remove', subscription:subscription};
            }
            
            self.submit(request);
        }
        
        return {update_absences:update_absences};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        self.$absences_widget.delegate('span', 'click', events.update_absences);
        
        return this;
    },


    submit: function(request) {
        var self = this,
            templates = self.templates,
            events = self.events;
            
        var ajax_url = '/teachers/update-absences/';
        $.ajax({
            url: ajax_url,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(request),
            dataType: 'json',
            timeout: 10000,
            beforeSend: function() {
                self.$absences_widget.undelegate();
            },
            success: function(data) {
                
                    if (data.status == 1){
                        var context = data.absences_context;
                        self.$active_widget.empty().append( self.render(templates.absences, context) );
                    }
                    else if (data.status == 2){
                        self.show_message(data.status, data.msg, 200);
                        $.scrollTo({top: 0}, 500, {axis:'y'});
                    }
                    
            },
            error: function(xhr, err){
                var ms = "Παρουσιάστηκε σφάλμα κατά την αποστολή των δεδομένων";
                //if(xhr.status==500)
                self.show_message(2, ms, 200);
            },
            complete: function(){
                self.listen_events();
            }
        });
        
    }

});

