$(function () {
	('use strict');

	//Message notification fading
	setTimeout(function () {
		$('#message').fadeOut('slow');
		$('#toast-container').fadeOut('slow');
	}, 3500);

	/* WOW.js init */
	new WOW().init();

	// MDB Lightbox Init
	$(function () {
		$('#mdb-lightbox-ui').load(
			'./assets/mdb-addons/mdb-lightbox-ui.html'
		);
	});

	// Material Select Initialization
	$(document).ready(function () {
		$('.mdb-select').materialSelect();
	});

	// initialize scrollspy
	$('body').scrollspy({
		target: '.dotted-scrollspy',
	});
	$('body').scrollspy({
		target: '#fm-block',
	});

	// Back to top
	var $btn = $('#btnTop');
	var $scrollMenu = $('.dotted-scrollspy > ul.nav');
	var $main_header = $('#main_header');
	var startpoint = $main_header.scrollTop() + $main_header.height();
	$(window).on('scroll', function () {
		if ($(window).scrollTop() > startpoint) {
			$btn.show();
			$scrollMenu.show();
		} else {
			$btn.hide();
			$scrollMenu.hide();
		}
	});

	$(document).on('click', '.gmodal-loader', function (e) {
		e.preventDefault();
		var url = $(this).data('url');
		var title = $(this).data('title');
		var target = $(this).data('target');

		$.ajax({
			url: url,
			type: 'GET',

			success: function (res) {
				$(target + ' #gmodalContent').html(res);
				$(target + ' #gmodalTitle').html(title);
			},

			error: function (er) {
				console.log(er);
			},
		});
	});
});
