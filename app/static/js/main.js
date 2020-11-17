
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

		$('.donut').peity('donut')
		$(function () {
			$('[data-toggle="tooltip"]').tooltip()
		})

		if (window.location.pathname.indexOf('/rankings') > -1) {
			if (document.getElementById('SBL_clock')) {
				var next_tuesday_eu_session = getNextOccuranceOfUTCDayAndHour(2, 18);
				var next_saturday_eu_session = getNextOccuranceOfUTCDayAndHour(6, 18);
				var next_eu_session;

				if (next_tuesday_eu_session > next_saturday_eu_session) {
					next_eu_session = next_saturday_eu_session
				}
				else {
					next_eu_session = next_tuesday_eu_session
				}

				var next_thursday_us_session = getNextOccuranceOfUTCDayAndHour(4, 23);
				var next_saturday_us_session = getNextOccuranceOfUTCDayAndHour(6, 20);
				var next_us_session;

				if (next_thursday_us_session > next_saturday_us_session) {
					next_us_session = next_saturday_us_session
				}
				else {
					next_us_session = next_thursday_us_session
				}

				var next_session;
				if (next_us_session < next_eu_session) {
					next_session = next_us_session
				}
				else {
					next_session = next_eu_session
				}

				const params = new URLSearchParams(window.location.search)
				match_type = params.get('match_subtype_id')
				if (match_type == "sbl-s2") {
					initializeClock('SBL_clock', next_session)
				}
			}
		}

		if (window.location.pathname.indexOf('/league-info') > -1) {
			setLocalTimes();
		}
		
	})
})();

function getTimeRemaining(endtime) {
	var t = Date.parse(endtime) - Date.parse(new Date());
	var seconds = Math.floor((t / 1000) % 60);
	var minutes = Math.floor((t / 1000 / 60) % 60);
	var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
	var days = Math.floor(t / (1000 * 60 * 60 * 24));
	return {
		'total': t,
		'days': days,
		'hours': hours,
		'minutes': minutes,
		'seconds': seconds
	};
}

function initializeClock(id, endtime) {
	var clock = document.getElementById(id);
	var daysSpan = clock.querySelector('.days');
	var hoursSpan = clock.querySelector('.hours');
	var minutesSpan = clock.querySelector('.minutes');
	var secondsSpan = clock.querySelector('.seconds');

	function updateClock() {
		var t = getTimeRemaining(endtime);

		daysSpan.innerHTML = t.days;
		hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
		minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
		secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

		if (t.total <= 0) {
		clearInterval(timeinterval);
		}
	}

	updateClock();
	var timeinterval = setInterval(updateClock, 1000);
}
  
function getNextOccuranceOfUTCDayAndHour(day, hour) {
    d = new Date();
    d.setUTCDate(d.getUTCDate() + (7 + day - d.getUTCDay()) % 7)
    d.setUTCHours(hour, 0, 0, 0);
    if (d < new Date()) {
        d.setUTCDate(d.getUTCDate() + 7);
    }
    return d;
}

function setLocalTimes() {
	document.getElementsByName('local-time').forEach(function(element) {
		let utc_time = element.textContent;
		let local_time = moment.utc(utc_time,'HH:mm').local().format("HH:mm");
		let local_time_zone = moment.tz(moment.tz.guess()).zoneAbbr()
		element.textContent = local_time + " " + local_time_zone;
	});
}