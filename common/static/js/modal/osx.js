/*
 * SimpleModal OSX Style Modal Dialog
 * http://www.ericmmartin.com/projects/simplemodal/
 * http://code.google.com/p/simplemodal/
 *
 * Copyright (c) 2010 Eric Martin - http://ericmmartin.com
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Revision: $Id: osx.js 238 2010-03-11 05:56:57Z emartin24 $
 */

jQuery(function ($) {
	var OSX = {
		container: null,
		init: function () {
			$("#add-lab").click(function (e) {
				e.preventDefault();	

				$("#osx-modal-content").modal({
					overlayId: 'osx-overlay',
					containerId: 'osx-container',
					closeHTML: null,
					minHeight: 80,
					opacity: 70, 
					position: ['0'],
					overlayClose: true,
					onOpen: OSX.open,
					onClose: OSX.close
				});
			});
		},
		open: function (d) {
		
			var self = this;
			self.container = d.container[0];
			d.overlay.fadeIn(300, function () {
				setTimeout( function() {
					$("#osx-modal-content", self.container).show();
					$("#osx-modal-title", self.container).show();
					$("div.close", self.container).show();
					$("#osx-modal-data", self.container).show();
					
					if(!window.getComputedStyle){
						// IE <= 8 doesn't support "getComputedStyle" property
						var conPosition = ($(window).width()/2 - d.container.width()/2);
						d.container.show().offset({ top: -(d.container.height() + 20), left: conPosition }).animate({ top: 0 }, 500 );
					}
					else{
						d.container.show().offset({ top: -(d.container.height() + 20) }).animate({ top: 0 }, 500 );
					}
				}, 100);
			});
		
		},
		close: function (d) {
			var self = this; // this = SimpleModal object
			d.container.animate(
				{top:"-" + (d.container.height() + 20)},
				350,
				function () {
					self.close(); // or $.modal.close();
				}
			);
		}
	};

	OSX.init();

});
