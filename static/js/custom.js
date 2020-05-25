$(function () {
    $('.semester-toggle').click(function (e) {
        e.preventDefault();
        let element = $(this);
        const endpoint = element.attr('href')

        $.ajax({
            url: endpoint,
            success: (data) => {
                console.log('success');
                element.text(data.active)
            },
            error: (error) => {
                console.log(error)
            }
        })
    })
    function checkLang(lang) {
        const langs = ['ar', 'en']
        if (!langs.includes(lang)) {
            lang = 'ar'
        }
        return lang
    }
    $('#schedule-search-form').submit(function (event) {
        event.preventDefault();

        const id = form.find('select').val()
        console.log(id)
        const url = `/tabels/api/classroom-schedule/${id}`
        const lang = checkLang($('#lang-input-id').val())
        let element = $('#schedules-tabel-id')


        let firstTr;
        if (lang == 'ar') {
            firstTr = `
                            <tr>
                            <th scope="col">اليوم</th>
                            <th scope="col">الحصة الأولى</th>
                            <th scope="col">الحصة الثانية</th>
                            <th scope="col">الحصة الثالثة</th>
                            <th scope="col">الحصة الرابعة</th>
                            <th scope="col">الحصة الخامسة</th>
                            <th scope="col">الحصة السادسة</th>
                            <th scope="col">الحصة السابعة</th>

                        </tr>
                    `
        } else {
            firstTr = `
                                <tr>
                                    <th scope="col">Day</th>
                                    <th scope="col"> First Class</th>
                                    <th scope="col"> Second Class</th>
                                    <th scope="col">Third Class</th>
                                    <th scope="col">Forth Class</th>
                                    <th scope="col">Fifth Class</th>
                                    <th scope="col">Sixth Class</th>
                                    <th scope="col">Seventh Class</th>
                    
                                </tr>`
        }

        function ScheduleDataHtml(data) {
            let trs = ``
            for (let i of data) {
                let tr = `<tr>
                                <th scope="row">${i.day}</th>
                                <td>${i.class_1}</td>
                                <td>${i.class_2}</td>
                                <td>${i.class_3}</td>
                                <td>${i.class_4}</td>
                                <td>${i.class_5}</td>
                                <td>${i.class_6}</td>
                                <td>${i.class_7}</td>

                            </tr> `
                trs += tr
            }
            return trs
        }

        $.ajax({
            url: url,
            success: (data) => {
                console.log(data)
                let tabel = `
                <table class="table table-bordered text-center">
                <thead>
                    ${firstTr}
                </thead>
                <tbody>
                    ${ScheduleDataHtml(data)}
                </tbody>
            </table>            
                `
                element.html(tabel)
                element.slideDown()

            },
            error: (error) => {

                if (error.status == 404) {
                    console.log(error.status)
                    const errorMsg = `
                    <p class='lead errorMsg text-center'>
                        عفوا لم يتم إيجاد الجدول لهذا الفصل
                    </p>
                    `

                    element.html(errorMsg)

                }
                element.show()

            }

        })


    })

    $('#exams-tabel-search-form').submit(function (event) {
        event.preventDefault();
        let form = $(this)
        const formData = form.serialize()
        const lang = checkLang($('#lang-input-id').val())
        const url = `/tabels/api/exams-tabel/?${formData}`
        let element = $('#exams-tabel-id')
        let iconDiv = $('#exams-icon-div-id')
        $.ajax({
            url: url,
            success: (data) => {
                let title = (lang == 'en' && data.en_title) ? data.en_title : data.title
                const firstTr = `
                        <tr>
                        <th colspan="5">
                           ${title}
                        </th>
                    </tr>
                `
                let secondTr;
                let thirdTr;
                let fifthTr;
                if (lang == 'ar') {
                    secondTr = `<tr>
                                    <th scope="col">السنة</th>
                                    <th scope="col">الصف </th>
                                    <th scope="col"> النوع </th>
                                    <th scope="col">الفترة </th>
                                    <th scope="col">الفصل الدراسي</th>
                                </tr>`

                    thirdTr = ` <tr>
                                    <td>${data.year}</td>
                                    <td>${data.the_class.ar_name}</td>
                                    <td>${data.exam_type.ar}</td>
                                    <td>${data.semester.ar}</td>
                                    <td>${data.class_room.ar_name}</td>
                                </tr> `
                    fifthTr = `<tr>
                                <th scope="col">المادة</th>
                                <th scope="col">وقت بداية الإمتحان </th>
                                <th scope="col">وقت نهاية الإمتحان </th>
                                <th scope="col">يوم الإمتحان </th>
                                <th scope="col">تاريخ الإمتحان </th>
                                </tr>`
                } else {
                    secondTr = `<tr>
                                    <th scope="col">Year</th>
                                    <th scope="col"> Class </th>
                                    <th scope="col"> Type </th>
                                    <th scope="col">Semester </th>
                                    <th scope="col">Classroom</th>
                                </tr>`
                    thirdTr = ` <tr>
                                    <td>${data.year}</td>
                                    <td>${data.the_class.ar_name}</td>
                                    <td>${data.exam_type.en}</td>
                                    <td>${data.semester.en}</td>
                                    <td>${data.class_room.ar_name}</td>
                                </tr> `
                    fifthTr = `<tr>
                                    <th scope="col">Subject</th>
                                    <th scope="col">Exam start at </th>
                                    <th scope="col">Exam end at </th>
                                    <th scope="col">Exam Day </th>
                                    <th scope="col" >Exam Date </th>
                                </tr>`



                }
                let LastTrs = ``

                for (let i of data.exam) {
                    const examTr = `
                    <tr>
                    <td>${i.subject}</td>
                    <td>${i.start_time}</td>
                    <td>${i.end_time}</td>
                    <td>${i.day}</td>
                    <td colspan='2'>${i.the_date}</td>
                </tr>
                    `
                    LastTrs += examTr
                }

                const examsTabel = `
        <table class="table table-bordered text-center">
        <thead>
        ${firstTr}
        ${secondTr}
        ${thirdTr}
        <tr>
            <th colspan="5">
            </th>
        </tr>
        ${fifthTr}
        ${LastTrs}
     </tbody>
    </table>
        
        `
                iconDiv.show()
                element.html(examsTabel)


            },
            error: (error) => {
                console.log(error.status)
                if (error.status == 404) {
                    const errorMsg = `
                    <p class='lead errorMsg text-center'>
                    عفوا لم يتم إيجاد الجدول  
                    يرجى التأكد من البيانات
                    </p>
                    `
                    iconDiv.show()
                    element.html(errorMsg)


                }

            }

        })
        setTimeout(() => {
            iconDiv.hide()
            element.show()
        }, 2000);

    })


    //  Users Activetion Ajax Request
    $('.users-activetion-btn').click(function (event) {
        event.preventDefault()
        let element = $(this)
        const url = element.attr('href')
        $.ajax({
            url: url,
            success: (data) => {
                $('.user-activetion-btn').each(function () {
                    $(this).text(data.text)
                })
            },
            error: (error) => {
                console.log(error.status)
            }
        })
    })

    //  User Activetion Ajax Request
    $('.user-activetion-btn').on('click', function (event) {
        event.preventDefault()
        let element = $(this)
        let url = element.attr('href')

        $.ajax({
            url: url,
            success: (data) => {
                url = url.replace(/status-\d/, `status-${data.status}`)
                element.attr('href', url)
                element.text(data.text)

            },
            error: (error) => {
                console.log(error.status)
            }
        })
    })
})