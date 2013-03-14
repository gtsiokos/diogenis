
X$('Helpers',
{
    csrf_token: undefined,
    //hash: undefined,
    
    init:               function(){
                            this.getCsrfToken().setGlobalAjax().generateFooterEmail();
                            return this;
                        },
    
    render:             function(template, context){
                            var template = Handlebars.compile(template);
                            return template(context);
                        },
    
    get_spinner:        function(){
                            var options = {
                                           lines: 12, // The number of lines to draw
                                           length: 6, // The length of each line
                                           width: 4, // The line thickness
                                           radius: 12, // The radius of the inner circle
                                           color: '#444', // #rbg or #rrggbb
                                           speed: 1.6, // Rounds per second
                                           trail: 55, // Afterglow percentage
                                           shadow: false // Whether to render a shadow
                                          };
                            
                            return {options:options};
                        },
    
    getCsrfToken:       function(){
                            var self = this,
                                cookie,
                                cookies;
                            
                            if (document.cookie && document.cookie != '') {
                                cookies = document.cookie.split(';');
                                for (var i = 0, len = cookies.length; i<len; i++) {
                                    cookie = self.getCookie(cookies[i]);
                                    if (cookie['name'] === 'csrftoken') {
                                        self.csrf_token = cookie['value']
                                        break;
                                    }
                                }
                            }
                            return this;
                        },
    
    getCookie:          function(cookie){
                            cookie = $.trim(cookie);
                            cookie = cookie.split('=');
                            return { name:cookie[0], value:cookie[1] }
                        },
    /*
    getHash:             function(){
                            var h = this.hash || $("input[type='hidden']", "#login").val();
                            this.hash = h;
                            return this.hash;
                        },
    */
    splitDate:          function(date){
                            var date = date.split(" ");
                            var day = date[0];
                            var hour = parseInt(date[1], 10);
                            var AmPm = date[2];
                            if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
                                hour = hour;
                            } else { hour = hour+12; }

                            return {day:day, hour:hour};
                        },
    
    explodeFullname:    function(day){
                            var daysStr     = "Δευτέρα Τρίτη Τετάρτη Πέμπτη Παρασκευή",
                                days         = daysStr.split(/ +/),
                                matchedDay    = undefined;
                            
                            for(var i=0, len=days.length; i<len; i++){
                                if( day == days[i].substr(0,3) ){
                                    matchedDay = days[i];
                                    break;
                                }
                            }
                            
                            return matchedDay || false;
                        },
    
    //********************************
    //Global Ajax Behaviour
    //********************************    
    setGlobalAjax:      function(){
                            var self = this,
                                theBody = $("body:first");
                            
                            $.ajaxSetup({ cache: false });
                            
                            theBody.ajaxStart(function(){
                                theBody.addClass("wait");
                            });
                            
                            theBody.ajaxSend(function(e, xhr, settings){
                                if ( !(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)) ){
                                    xhr.setRequestHeader("X-CSRFToken", self.csrf_token);
                                }
                            });
                            
                            theBody.ajaxComplete(function(){
                                theBody.removeClass("wait");
                            });
                            
                            return this;
                        },

    //********************************
    //Generates email for search-bots defence
    //********************************                          
    generateFooterEmail:function(){
                            var is_temporary = false,
                                $email = $("#footer-email"),
                                domain = $email.attr('rel').replace('http://', '@');
                            
                            if(is_temporary){
	                            $email.attr('href', 'mailto:onnotes@gmail.com');
                            }else{
                                $email.attr('href', 'mailto:diogenis'+domain);
                            }
                            
                            return this;
                        }
});


X$('JSON',
{

get: function(object, expression, callback){
    var matches = [];
    
    if(typeof expression === "string"){
        matches = JSONSelect.match(expression,object);
    }
    if(callback && $.isFunction(callback)){
        callback.call(matches);
    }
    return matches;
}

});

