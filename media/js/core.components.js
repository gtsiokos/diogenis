
X$('Helpers',
{
	hash: undefined,
	
	getHash: 		function(){
						var h = this.hash || $("input[type='hidden']", "#login").val();
						this.hash = h;
						return this.hash;
					},
	
	splitDate: 		function(date){
						var date = date.split(" ");
						var day = date[0];
						var hour = parseInt(date[1], 10);
						var AmPm = date[2];
						if (AmPm == "π.μ." || AmPm == "μ.μ." && hour == 12) {
							hour = hour;
						} else { hour = hour+12; }

						return {day:day, hour:hour};
					}
});

