
X$('StudentTransfer',
{
    $content:       $('#content'),
    $labs:          $('div.lab', '#content'),
    $dropdown:      $('div.lab span.transfer.enabled', '#content'),
    
    url:            undefined,
    lab:            { 'new': {}, 'old': {} },
    students:       [],
    
    init: function(){
        var self = this;
        
        self.url = self.get_url();
        
        var ajaxTrans       = self.$dropdown.find('ul.labs-list li'),
            msg             = $('#ui-messages p', '#content');
        
        self.$labs.find('table td>input').removeAttr('disabled').attr('checked', false);
        
        ajaxTrans.bind('click', function(){
            var ms,
                data,
                parentDiv = $(this).parents('div.lab');
            
            data = $(this).data()
            self.lab['new'] = {id:data.id};
            data = parentDiv.data();
            self.lab['old'] = {id:data.id};
            
            var i = 0,
                students = parentDiv.find('table tr:not(.disabled) td>input:checked');
            
            for(var i=0, student; student=students[i]; i++){
                self.students[i] = $(student).data();
            }
            
            if (self.students[0]) {

                var request =   {
                                lab:self.lab,
                                students:self.students
                                };

                var ajax_url = '/teachers/submit-student-to-lab/';
                $.ajax({
                    url: ajax_url,
                    type: 'POST',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify(request),
                    dataType: 'json',
                    timeout: 10000,
                    success: function(data) {
                           try {
                               if (data.status == 1){
                                   students.parents('tr').addClass('disabled', 80).find('input').attr('disabled', 'disabled');
                                setTimeout( function() {
                                    msg.fadeOut(100).removeClass().addClass('ok')
                                    .text(data.msg).append('<a href="#" onClick="window.location.reload()">ανανέωση</a>')
                                    .fadeIn(200);
                                },300);
                            }
                            else if ( data.status == 2 ) {
                                setTimeout( function() {
                                    msg.fadeOut(100).removeClass().addClass('error').text(data.msg).fadeIn(200);
                                },300);                    
                            }
                            else {
                                setTimeout( function() {
                                    msg.fadeOut(100).removeClass().addClass('warning').text(data.msg).fadeIn(200);
                                },300);
                            }
                        }
                        catch(e) { this.error(); }
                    },
                    error: function(xhr, err){
                        ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε αργότερα";
                        /*
                        if(xhr.status==500) ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
                        if(xhr.status==404) ms = "Παρουσιάστηκε σφάλμα, δοκιμάστε ξανά";
                        */
                        msg.fadeOut(100).removeClass().addClass('error').text(ms).fadeIn(200);
                    },
                    complete: function() {
                        X$('DropdownWidget').events.dropdown.hide();
                        self.students = [];
                        $.scrollTo({top: 0}, 350, {axis:'y'});
                    }
                });
            } else {
                X$('DropdownWidget').events.dropdown.hide();
                
                ms = "Δεν έχετε επιλέξει κάποιον σπουδαστή";
                setTimeout( function() {
                    msg.fadeOut(100).removeClass().addClass('warning').text(ms).fadeIn(200);
                },300);
                $.scrollTo({top: 0}, 500, {axis:'y'});
            }
            return false;
        });
    
    	return this;
    },
    
    get_url: function(){
        var result = {},
            url = window.location.href;
        
        if( url.match(/pending-students/) ){
            result = 'pending';
        }
        else {
            result = 'home';
        }
        //console.log(result);
        return result;
    }
    
});

X$('DropdownWidget',
{
    events:         undefined,
    
    init: function(){
        this.events = this.handle_events();
        this.listen_events();
    },
                    
    handle_events: function(){
        var self = this,
            dropdown = {};
        
        dropdown.$ = {
                     buttons:   X$('StudentTransfer').$dropdown.find('ul.labs-list'),
                     active:    undefined
                     }
                         
        dropdown.hide = function(){
            var self = this,
                $this = self.$.buttons;
            
            if($this) {
                $this.hide();
                $this.parent().removeClass('active');
            }
        };
        dropdown.close = function(params){
            var self = dropdown,
                $this = self.$.active,
                target = params.event.target;
            
            if($this) {
                var $this = $this[0];
                if(!$.contains($this,target) || !$this == target) {
                    self.hide();
                }
            }
        };
        dropdown.open = function(){
            var self = this,
                $this = self.$.active;
            
            self.hide();
            $this.show();
            $this.parent().addClass('active');
        };
        
        dropdown.$.buttons.each(function(){
            var self = dropdown,
                $this = $(this),
                $parent = $this.parent();
            
            $parent.bind('click', function(e){
                if(e) e.stopPropagation();
                if(e) e.preventDefault();
                self.$.active = $this;
                self.open();
            });
        });
        
        return {dropdown:dropdown};
    },
    
    listen_events: function(){
        var self = this,
            events = self.events;
        
        $.subscribe('widgets.close.dropdown.transfer', events.dropdown.close);
        return this;
    }

});

