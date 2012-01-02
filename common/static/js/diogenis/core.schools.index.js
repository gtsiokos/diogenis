
X$('SchoolsIndex',
{
    $form: $('#courses-upload'),
    $file: undefined,
    
    init: function(){
        var self = this;
        self.$file = self.$form.find('input:file');
        
        self.handle_events();
        return this;
    },
    
    handle_events: function(){
        var self = this;
        
        self.$file.change(function(e){
            self.$form.submit();
        });
        
        return this;
    }
});


X$('SchoolsSubscriptionsActivation',
{
    $form: $('#subscriptions-activation'),
    $checkbox: undefined,
    
    init: function(){
        var self = this;
        self.$checkbox = self.$form.find('input:checkbox');
        
        self.handle_events();
        return this;
    },
    
    handle_events: function(){
        var self = this;
        
        self.$checkbox.change(function(e){
            self.$form.submit();
        });
        
        return this;
    }
});
