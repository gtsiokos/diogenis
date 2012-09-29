X$('MessagesMixin',
{
    $messages:          $('#ui-messages'),
	status:             {0:'', 1:'ok', 2:'error', 3:'warning'},
    
    show_message: function(status_id, msg, speed) {
        var self = this,
            speed = speed || 150,
            status = self.status[status_id];
            
        self.$messages.find('p').fadeOut(100, function(){
            $.scrollTo({top: 0}, 500, {axis:'y'});
            $(this).removeClass().addClass(status).html(msg).fadeIn(speed);
        });
    }
});
