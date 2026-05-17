/*  ---------------------------------------------------
    LNS CARz - Main JavaScript
    Updated for Sri Lankan LKR pricing
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Car filter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.car-filter').length > 0) {
            var containerEl = document.querySelector('.car-filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });

    $(".offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });

    //Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });

    /*------------------
        Navigation
    --------------------*/
    $(".header__menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*--------------------------
        Car Image Slider
    ----------------------------*/
    $(".car__item__pic__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false
    });

    /*--------------------------
        Testimonial Slider
    ----------------------------*/
    var testimonialSlider = $(".testimonial__slider");
    testimonialSlider.owlCarousel({
        loop: true,
        margin: 0,
        items: 2,
        dots: true,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
        responsive: {
            768: { items: 2 },
            0: { items: 1 }
        }
    });

    /*-----------------------------
        Car Thumb Slider
    -------------------------------*/
    $(".car__thumb__slider").owlCarousel({
        loop: true,
        margin: 25,
        items: 5,
        dots: false,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        mouseDrag: false,
        responsive: {
            768: { items: 5 },
            320: { items: 3 },
            0: { items: 2 }
        }
    });

    /*-----------------------
        LKR Range Slider — Hero (Buy tab)
    ------------------------ */
    function formatLKR(val) {
        if (val >= 1000000) {
            return 'LKR ' + (val / 1000000).toFixed(1) + 'M';
        } else if (val >= 1000) {
            return 'LKR ' + (val / 1000).toFixed(0) + 'K';
        }
        return 'LKR ' + val;
    }

    var rangeSlider = $(".price-range");
    rangeSlider.slider({
        range: true,
        min: 500000,
        max: 50000000,
        step: 500000,
        values: [2000000, 15000000],
        slide: function (event, ui) {
            $("#amount").val(formatLKR(ui.values[0]) + " – " + formatLKR(ui.values[1]));
        }
    });
    $("#amount").val(formatLKR($(".price-range").slider("values", 0)) + " – " + formatLKR($(".price-range").slider("values", 1)));

    /*-----------------------
        LKR Range Slider — Hero (Sell tab)
    ------------------------ */
    var sellSlider = $(".price-range-sell");
    sellSlider.slider({
        range: true,
        min: 500000,
        max: 50000000,
        step: 500000,
        values: [3000000, 12000000],
        slide: function (event, ui) {
            $("#amount2").val(formatLKR(ui.values[0]) + " – " + formatLKR(ui.values[1]));
        }
    });
    $("#amount2").val(formatLKR($(".price-range-sell").slider("values", 0)) + " – " + formatLKR($(".price-range-sell").slider("values", 1)));

    /*-----------------------
        LKR Range Slider — Car Listings Page
    ------------------------ */
    var carSlider = $(".car-price-range");
    carSlider.slider({
        range: true,
        min: 500000,
        max: 50000000,
        step: 500000,
        values: [2000000, 20000000],
        slide: function (event, ui) {
            $("#caramount").val(formatLKR(ui.values[0]) + " – " + formatLKR(ui.values[1]));
        }
    });
    $("#caramount").val(formatLKR($(".car-price-range").slider("values", 0)) + " – " + formatLKR($(".car-price-range").slider("values", 1)));

    /*-----------------------
        LKR Range Slider — Filter sidebar
    ------------------------ */
    var filterSlider = $(".filter-price-range");
    filterSlider.slider({
        range: true,
        min: 500000,
        max: 50000000,
        step: 500000,
        values: [1000000, 25000000],
        slide: function (event, ui) {
            $("#filterAmount").val(formatLKR(ui.values[0]) + " – " + formatLKR(ui.values[1]));
        }
    });
    $("#filterAmount").val(formatLKR($(".filter-price-range").slider("values", 0)) + " – " + formatLKR($(".filter-price-range").slider("values", 1)));

    /*--------------------------
        Select
    ----------------------------*/
    $("select").not(".form-control-lns").niceSelect();

    /*------------------
        Magnific Popup
    --------------------*/
    $('.video-popup').magnificPopup({
        type: 'iframe'
    });

    /*------------------
        Single Product
    --------------------*/
    $('.car-thumbs-track .ct').on('click', function () {
        $('.car-thumbs-track .ct').removeClass('active');
        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.car-big-img').attr('src');
        if (imgurl != bigImg) {
            $('.car-big-img').attr({ src: imgurl });
        }
    });

    /*------------------
        Counter Up
    --------------------*/
    $('.counter-num').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

    /*------------------
        Form Validation & Submission feedback
    --------------------*/
    // Sell form
    $('#sellForm').on('submit', function(e) {
        e.preventDefault();
        var btn = $(this).find('.site-btn');
        btn.text('Submitting...').prop('disabled', true);
        setTimeout(function() {
            btn.text('✓ Submitted Successfully!').css('background','#28a745');
            setTimeout(function() {
                btn.text('Submit for Sale').css('background','').prop('disabled', false);
            }, 4000);
        }, 1200);
    });

    // Booking form
    $('#bookingForm').on('submit', function(e) {
        e.preventDefault();
        var btn = $(this).find('.site-btn');
        btn.text('Booking...').prop('disabled', true);
        setTimeout(function() {
            btn.text('✓ Appointment Booked!').css('background','#28a745');
            setTimeout(function() {
                btn.text('Book Appointment').css('background','').prop('disabled', false);
            }, 4000);
        }, 1200);
    });

    // Brokering form
    $('#brokerForm').on('submit', function(e) {
        e.preventDefault();
        var btn = $(this).find('.site-btn');
        btn.text('Sending...').prop('disabled', true);
        setTimeout(function() {
            btn.text('✓ Request Submitted!').css('background','#28a745');
            setTimeout(function() {
                btn.text('Submit Request').css('background','').prop('disabled', false);
            }, 4000);
        }, 1200);
    });

    // Contact form
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
        var btn = $(this).find('.site-btn');
        btn.text('Sending...').prop('disabled', true);
        setTimeout(function() {
            btn.text('✓ Message Sent!').css('background','#28a745');
            setTimeout(function() {
                btn.text('Send Message').css('background','').prop('disabled', false);
            }, 4000);
        }, 1200);
    });

})(jQuery);
