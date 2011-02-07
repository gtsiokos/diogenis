
(function($, window, document, undefined) {
    
    var App = function(module_name, properties){
        return new App.core.init(module_name, properties);
    };
    
    var App = (function(){
    
        App.core = App.prototype = {
        	
        	init: function(n, p){
                var self = this;
                //console.log("called module [", n,"]");
                if (p){
		            $(function(){
		                self.modules[n] = p;
		            	// In case it needs initialization
		            	try{
		            		self.modules[n].init();
		            	}
		            	catch(e){ }
		            });
		        }
                else if(n && !p) {
                	return self.get(n);
                }
                return self; 
            },
            get: function(n){
            	return App.core.modules[n];
            },
            modules: {}
        };

        App.core.init.prototype = App.core;
        App.get = App.core.get;
        
        return window.X$ = App;
    })();
    
})(jQuery, this, this.document);


$(function(){
	
	//********************************
	//Focus-Out Feauture for Options Panel
	//********************************	
	
	var oPanel = $("#login");
	oPanel.find('div.panel').hide();
	
	var theActive, isActive;
	
	var hidePanel = function(){
		if(theActive) {
			theActive.hide();
			theActive.parent().removeClass("active");
		}
	};
	
	oPanel.find("div.panel").each(function(){
		
		var options = $(this);
		var loginDiv = $(this).parent();
		
		var showPanel = function(){
			hidePanel();
			theActive = options.show();
			loginDiv.addClass("active");
			isActive = options;
		};
		
		loginDiv.children("a.options-panel").click(function(e){
			if ( loginDiv.hasClass("active") ){
				hidePanel();
			} else {
				showPanel();
			}
			if(e){ e.stopPropagation(); }
			if(e){ e.preventDefault(); }
		});
	});
	
	$(document.body).bind('click',function(e) {
		if(isActive) {
			var active = isActive[0];
			if(!$.contains(active,e.target) || !active == e.target) {
				hidePanel();
			}
		}
	});
	
});
