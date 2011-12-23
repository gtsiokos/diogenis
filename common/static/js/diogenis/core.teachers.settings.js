
X$('TeacherSettings',
{
    $form: $('#change-password'),
    $button: $('#change-password-button'),
    
    init: function(){
        var self = this;
        
        if(self.$button){
            self.handle_events();
        }
        return this;
    },
    
    handle_events: function(){
        var self = this;
        
        self.$button.click(function(e){
            e.preventDefault();
            e.stopPropagation();
            
            var input = self.$form.find('input:first'),
                text = 'Ο νέος κωδικός σας είναι ο "'+input.val()+'";'
            
            smoke.confirm(text,function(e){
                if(e){
                    self.$form.submit();
                }
            }, {classname:'warning', ok:'Ναι, άλλαξέ τον', cancel:'Ακύρωση'});
        });
        
        return this;
    }
});

