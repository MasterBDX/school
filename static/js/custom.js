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

    $('#schedule-search-form').submit(function (event) {
        event.preventDefault();
        let form = $(this)
        const id = form.find('select').val()
        const url = `/tabels/api/classroom-schedule/${id}`



        function ScheduleDataHtml(data) {
            let trs = ``
            for (let i of data) {
                let tr = `

                <tr>
                    <th scope="row">${i.day}</th>
                    <td>${i.class_1}</td>
                    <td>${i.class_2}</td>
                    <td>${i.class_3}</td>
                    <td>${i.class_4}</td>
                    <td>${i.class_5}</td>
                    <td>${i.class_6}</td>
                    <td>${i.class_7}</td>

                </tr>
                `
                trs += tr
            }
            return trs
        }
        let element = $('#schedules-tabel-id')

        $.ajax({
            url: url,
            success: (data) => {

                let tabel = `
                <table class="table table-bordered text-center">
                <thead>
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
                </thead>
                <tbody>
                    ${ScheduleDataHtml(data)}
                </tbody>
            </table>
            
                `
                element.html(tabel)
                element.slideDown()
                // element.animate({ 'background-color': '#CCC' }, 1000)
            },
            error: (error) => {
                if (error.status == 404) {
                    const errorMsg = `
                    <p class='lead errorMsg text-center'>
                    عفوا لم يتم إيجاد الجدول لهذا الفصل
                    </p>
                    `
                    element.html(errorMsg)

                }

            }

        })


    })

    $('#exams-tabel-search-form').submit(function (event) {
        event.preventDefault();
        let form = $(this)
        const formData = form.serialize()
        const url = `/tabels/api/exams-tabel/?${formData}`
        let element = $('#exams-tabel-id')
        let iconDiv = $('#exams-icon-div-id')
        $.ajax({
            url: url,
            success: (data) => {
                console.log(data)
                const firstTr = `
                        <tr>
                        <th colspan="5">
                           ${data.title}
                        </th>
                    </tr>
                `
                const secondTr = `
                <tr>
                    <td>${data.year}</td>
                    <td>${data.the_class}</td>
                    <td>${data.exam_type}</td>
                    <td>${data.semester}</td>
                    <td>${data.class_room}</td>

             </tr>
                `
                let LastTrs = ``
                for (let i of data.exam) {
                    const examTr = `
                    <tr>
                    <td>${i.article}</td>
                    <td>${i.start_time}</td>
                    <td>${i.end_time}</td>
                    <td colspan='2'>${i.the_date}</td>

                </tr>
                    `
                    LastTrs += examTr
                }
                const examsTabel = `
        <table class="table table-bordered text-center">
        <thead>
        ${firstTr}
        <tr>
            <th scope="col">السنة</th>
            <th scope="col">الصف </th>
            <th scope="col">نوع الإمتحان </th>
            <th scope="col">الفترة </th>
            <th scope="col">الفصل الدراسي</th>
        ${secondTr}
        </tr>
        <th colspan="5">

        </th>
        <tr>
        <th scope="col">المادة</th>
        <th scope="col">وقت بداية الإمتحان </th>
        <th scope="col">وقت نهاية الإمتحان </th>
        <th scope="col" colspan="2">تاريخ الإمتحان </th>
    </tr>

        ${LastTrs}
     </tbody>
    </table>
        
        `
                iconDiv.show()
                element.html(examsTabel)


            },
            error: (error) => {
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