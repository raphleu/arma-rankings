
(function () {
	$(document).ready(function () {
		// make the nav active for its current page
		var pathname = window.location.pathname;
		$('.nav > li > a[href="'+pathname+'"]').parent().addClass('active');

		$('#changeToggleNav').click(function() {
			$('.bar-icon-nav').toggleClass('hidden');
			$('.close-icon-nav').toggleClass('hidden');
		});

		$('.time-table div').each(function () {
			var part = $(this).text().split(':')
			$(this).replaceWith("<div class='l'>" + part[0] + "</div><div class='r'>" + part[1] + "</div>");
		});
	})
})();