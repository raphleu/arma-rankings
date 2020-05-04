
(function () {
	$(document).ready(function () {
		// make the nav active for its current page
		var pathname = window.location.pathname;
		$('.nav > li > a[href="'+pathname+'"]').parent().addClass('active');

		$('#changeToggleNav').click(function() {
			$('.bar-icon-nav').toggleClass('hidden');
			$('.close-icon-nav').toggleClass('hidden');
		});
	})
})();