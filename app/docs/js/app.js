$(function () {
	var $root = $('.wrap'),
		activeClass = 'ep-body-active',
		hash = window.location.hash,
		$hashTarget = null;

	$('html').addClass('has-js').removeClass('no-js');

	//$root.find('.ep-body').hide().attr('aria-hidden', true);

	$root.on('click', '.ep-header a', function () {
		var $this = $(this),
			$body = $this.closest('.ep-header').next(),
			$target = $($this.attr('href'));

		if ($body.hasClass(activeClass)) {
			$root.trigger('hidepanel', $target);
		} else {
			$root.trigger('showpanel', $target);
		}
		return false;
	}).on('hideallpanels', function (e, $except) {
		$root.find('.'+activeClass).not($except).each(function () {
			$root.trigger('hidepanel', $(this));
		});
	}).on('hidepanel', function (e, $body) {
		$($body).removeClass(activeClass).attr('aria-hidden', true);
	}).on('showpanel', function (e, $body) {
		$root.trigger('hideallpanels', $body);
		$($body).removeAttr('aria-hidden').addClass(activeClass);
	});

	if (hash !== "") {
		$hashTarget = $(hash);
		if ($hashTarget.hasClass('ep-body')) {
			$root.trigger('showpanel', $hashTarget);
		}
	}
});