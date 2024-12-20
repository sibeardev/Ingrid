function loadServicesAndSpecialists(url) {
    const serviceContainer = $("#servicesAccordion");
    const specialistsContainer = $("#mastersAccordion");

    $.ajax({
        url: url,
        method: "GET",
        success: function (data) {
            if (data.length > 0) {
                // Генерация Услуг
                if (data[0].services) {
                    let servicesHtml = '';
                    if (data[0].services.length > 0) {
                        servicesHtml = data[0].services.map(service => `
                        <div class="accordion__block fic" data-id="${service.id}">
                            <div class="accordion__block_item_intro">${service.title}</div>
                            <div class="accordion__block_item_address">${service.price} ₽</div>
                        </div>
                `).join("");
                    } else {
                        servicesHtml = `
                    <div class="accordion__block fic">
                        <div class="accordion__block_elems fic">
                            <div class="accordion__block_master">Нет доступных услуг</div>
                        </div>
                    </div>
                `;
                    }
                    serviceContainer.html(servicesHtml);
                }

                // Генерация специалистов
                if (data[0].specialists) {
                    let specialistsHtml = '';
                    if (data[0].specialists.length > 0) {
                        specialistsHtml = `
                    <div class="accordion__block fic" data-id="any_master">
                        <div class="accordion__block_elems fic">
                            <img src="${anyMasterImageUrl}" alt="avatar" class="accordion__block_img">
                            <div class="accordion__block_master">Любой мастер</div>
                        </div>
                    </div>
                ` + data[0].specialists.map(specialist => `
                    <div class="accordion__block fic" data-id="${specialist.id}">
                        <div class="accordion__block_elems fic">
                            <img src="${specialist.image_url}" alt="avatar" class="accordion__block_img">
                            <div class="accordion__block_master">${specialist.full_name}</div>
                        </div>
                        <div class="accordion__block_prof">${specialist.position}</div>
                    </div>
                `).join("");
                    } else {
                        specialistsHtml = `
                    <div class="accordion__block fic">
                        <div class="accordion__block_elems fic">
                            <div class="accordion__block_master">Нет доступных специалистов</div>
                        </div>
                    </div>
                `;
                    }
                    specialistsContainer.html(specialistsHtml);
                }
            } else {
                serviceContainer.html("<p>Нет доступных услуг в этом салоне.</p>");
                specialistsContainer.html("<p>Нет доступных специалистов для этой услуги.</p>");
            }
        },
        error: function (xhr, status, error) {
            console.error("Ошибка загрузки данных:", error);
            serviceContainer.html("<p>Произошла ошибка при загрузке данных. Попробуйте позже.</p>");
            specialistsContainer.html("<p>Произошла ошибка при загрузке данных. Попробуйте позже.</p>");
        },
    });
}

function loadSpecialistWorkday(specialistId, date) {
    console.log(date)
    const url = `/api/specialist_workday/?specialist_id=${specialistId}&selected_date=${date}`;
    $.ajax({
        url: url,
        method: "GET",
        success: function (data) {
            if (data.length > 0) {
                const timeslots = data[0].timeslots;
                const timeContainer = $(".time__elems");
                timeContainer.empty();

                // Функция для создания разметки блока времени
                const createTimeBlock = (timePeriod, times) => {
                    if (times.length === 0) return "";

                    const buttonsHtml = times.map(
                        time => `<button data-time="${time}" class="time__elems_btn">${time}</button>`
                    ).join("");

                    return `
                        <div class="time__items">
                            <div class="time__elems_intro">${timePeriod}</div>
                            <div class="time__elems_elem fic">
                                ${buttonsHtml}
                            </div>
                        </div>
                    `;
                };

                // Если все интервалы пустые
                const isAllTimeSlotsEmpty =
                (!timeslots.morning || timeslots.morning.length === 0) &&
                (!timeslots.day || timeslots.day.length === 0) &&
                (!timeslots.evening || timeslots.evening.length === 0);
                if (isAllTimeSlotsEmpty) {
                    timeContainer.html(`<div class="time__items">Нет доступного времени</div>`);
                    return;
                }

                // Генерация разметки для каждого периода времени
                const morningHtml = createTimeBlock("Утро", timeslots.morning);
                const dayHtml = createTimeBlock("День", timeslots.day);
                const eveningHtml = createTimeBlock("Вечер", timeslots.evening);

                timeContainer.append(morningHtml + dayHtml + eveningHtml);

            } else {
                $(".time__elems").html(`<div class="time__items">Нет доступного времени</div>`);
            }
        },
        error: function (xhr, status, error) {
            console.error("Ошибка загрузки рабочих часов:", error);
            $(".time__elems").html(`<div class="time__items">Ошибка загрузки данных</div>`);
        }
    });
}


$(document).ready(function() {
    $('.salonsSlider').slick({
        arrows: true,
        slidesToShow: 4,
        infinite: true,
        prevArrow: $('.salons .leftArrow'),
        nextArrow: $('.salons .rightArrow'),
        responsive: [
            {
                breakpoint: 991,
                settings: {

                    centerMode: true,
                    //centerPadding: '60px',
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
    $('.servicesSlider').slick({
        arrows: true,
        slidesToShow: 4,
        prevArrow: $('.services .leftArrow'),
        nextArrow: $('.services .rightArrow'),
        responsive: [
            {
                breakpoint: 1199,
                settings: {


                    slidesToShow: 3
                }
            },
            {
                breakpoint: 991,
                settings: {

                    centerMode: true,
                    //centerPadding: '60px',
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

    $('.mastersSlider').slick({
        arrows: true,
        slidesToShow: 4,
        prevArrow: $('.masters .leftArrow'),
        nextArrow: $('.masters .rightArrow'),
        responsive: [
            {
                breakpoint: 1199,
                settings: {


                    slidesToShow: 3
                }
            },
            {
                breakpoint: 991,
                settings: {


                    slidesToShow: 2
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

    $('.reviewsSlider').slick({
        arrows: true,
        slidesToShow: 4,
        prevArrow: $('.reviews .leftArrow'),
        nextArrow: $('.reviews .rightArrow'),
        responsive: [
            {
                breakpoint: 1199,
                settings: {


                    slidesToShow: 3
                }
            },
            {
                breakpoint: 991,
                settings: {


                    slidesToShow: 2
                }
            },
            {
                breakpoint: 575,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

    // menu
    $('.header__mobMenu').click(function() {
        $('#mobMenu').show()
    })
    $('.mobMenuClose').click(function() {
        $('#mobMenu').hide()
    })

    //    КАЛЕНДАРЬ
    new AirDatepicker('#datepickerHere', {
        language: 'ru',
        dateFormat: 'yyyy-MM-dd',
        minDate: new Date(),
        onSelect: function ({ formattedDate }) {
            const specialistId = localStorage.getItem('selectedSpecialistId');
            if (specialistId) {
                loadSpecialistWorkday(specialistId, formattedDate);
            } else {
                console.error("Специалист не выбран!");
            }
        }
    });

    localStorage.removeItem('selectedSalonId');
    localStorage.removeItem('selectedServiceId');
    localStorage.removeItem('selectedSpecialistId');

    var acc = document.getElementsByClassName("accordion");
    var i;
    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function(e) {
            e.preventDefault()
            this.classList.toggle("active");
            var panel = $(this).next()
            panel.hasClass('active') ?
            panel.removeClass('active')
            :
            panel.addClass('active')
        });
    }


    // САЛОН
    $(document).on('click', '.service__salons .accordion__block', function(e) {

        // Загрузить услуги и специалистов
        let salonId = $(this).data('id');
        const url = `/api/services/?salon_id=${salonId}`;
        loadServicesAndSpecialists(url);

        localStorage.setItem('selectedSalonId', salonId);

        let thisName,thisAddress;
        thisName = $(this).find('> .accordion__block_intro').text()
        thisAddress = $(this).find('> .accordion__block_address').text()

        // Обновить текста кнопки выбора салона
        $(this).parent().parent().find('> button.active').addClass('selected').text(thisName + " " + thisAddress)

        // Сброс кнопок выбора услуги и специалиста
        $('.service__services button.accordion')
            .removeClass('selected active')
            .text('(Выберите услугу)');

        $('.service__masters button.accordion')
            .removeClass('selected active')
            .text('(Выберите мастера)');
        $(".time__elems").empty();
        // Закрыть панель с выбором салона
        setTimeout(() => {
            $(this).parent().parent().find('> button.active').click()
        }, 200)

        // $(this).parent().addClass('hide')
        // console.log($(this).parent().parent().find('.panel').hasClass('selected'))
        // $(this).parent().parent().find('.panel').addClass('selected')
    })

    //УСЛУГА
    $(document).on('click', '.service__services .accordion__block', function(e) {

        // Загрузить специалистов
        let serviceId = $(this).data('id');
        let selectedSalonId = localStorage.getItem('selectedSalonId');
        let salonId = selectedSalonId ? selectedSalonId : '';
        const url = salonId ? `/api/specialists/?service_id=${serviceId}&salon_id=${salonId}` : `/api/specialists/?service_id=${serviceId}`;
        loadServicesAndSpecialists(url);

        let thisName,thisAddress;
        thisName = $(this).find('> .accordion__block_item_intro').text()
        thisAddress = $(this).find('> .accordion__block_item_address').text()

        localStorage.setItem('selectedServiceId', serviceId);

        $(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
        // $(this).parent().parent().parent().parent().find('> button.active').click()
        // $(this).parent().parent().parent().addClass('hide')

        // Сброс кнопок выбора специалиста
        $('.service__masters button.accordion')
            .removeClass('selected active')
            .text('(Выберите мастера)');
        $(".time__elems").empty();
        setTimeout(() => {
            $(this).parent().parent().find('> button.active').click()
        }, 200)
    })




    // 	console.log($('.service__masters > .panel').attr('data-masters'))
    // if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
    // }

    //МАСТЕР
    $(document).on('click', '.service__masters .accordion__block', function(e) {
        const specialistId = $(this).data('id');
        localStorage.setItem('selectedSpecialistId', specialistId);
        $(".time__elems").empty();
        let clone = $(this).clone()
        console.log(clone)
        $(this).parent().parent().find('> button.active').addClass('selected').html(clone)
        setTimeout(() => {
            $(this).parent().parent().find('> button.active').click()
        }, 200)
    })


    //     $('.accordion__block_item').click(function(e) {
    //     	const thisName = $(this).find('.accordion__block_item_intro').text()
    //     	const thisAddress = $(this).find('.accordion__block_item_address').text()
    //     	console.log($(this).parent().parent().parent().parent())
    //     	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
    //     })

    //     $('.accordion__block_item').click(function(e) {
    //         	const thisChildName = $(this).text()
    //         	console.log(thisChildName)
    //         	console.log($(this).parent().parent().parent())
    //         	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)
    //         })

    //     $('.accordion.selected').click(function() {
    //     	$(this).parent().find('.panel').hasClass('selected') ?
    //     	 $(this).parent().find('.panel').removeClass('selected')
    //     		:
    //     	$(this).parent().find('.panel').addClass('selected')
    //     })


    //popup
    $('.header__block_auth').click(function(e) {
        e.preventDefault()
        $('#authModal').arcticmodal();
        // $('#confirmModal').arcticmodal();

    })

    $('.rewiewPopupOpen').click(function(e) {
        e.preventDefault()
        $('#reviewModal').arcticmodal();
    })
    $('.payPopupOpen').click(function(e) {
        e.preventDefault()
        $('#paymentModal').arcticmodal();
    })
    $('.tipsPopupOpen').click(function(e) {
        e.preventDefault()
        $('#tipsModal').arcticmodal();
    })

    $('.authPopup__form').submit(function() {
        $('#confirmModal').arcticmodal();
        return false
    })

    //    КНОПКИ ВРЕМЕНИ
    $(document).on('click', '.time__items .time__elems_elem .time__elems_btn', function(e) {
        e.preventDefault();
        $('.time__elems_btn').removeClass('active');
        $(this).addClass('active');
    });


    $(document).on('click', '.servicePage', function() {
        if($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').hasClass('selected')) {
            $('.time__btns_next').addClass('active')
        }
    })

    $('#nextButton').click(function () {
        const selectedDate = $('#datepickerHere').val();
        const selectedTime = $('.time__elems_btn.active').data('time');
        const selectedSpecialistId = localStorage.getItem('selectedSpecialistId');
        const selectedServiceId = localStorage.getItem('selectedServiceId') || '';

        if (!selectedDate || !selectedTime || !selectedSpecialistId ) {
            alert("Выберите мастера, дату и время");
            return;
        }

        const url = `/service-finally/?date=${selectedDate}&time=${selectedTime}&specialist_id=${selectedSpecialistId}&service_id=${selectedServiceId}`;

        window.location.href = url;
    });

})
