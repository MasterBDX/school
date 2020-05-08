$(function () {

    function updateEmptyFormIDs(element, totalForms) {
        let thisInput = element;

        // get current form input name
        let currentName = element.attr('name');

        // replace "prefix" with actual number
        const newName = currentName.replace(/__prefix__/g, totalForms);

        // update input with new name
        thisInput.attr('name', newName)
        thisInput.attr('id', "id_" + newName)


        // // create a new form row id
        let newFormRow = element.closest(".empty-form-div");

        // div_id_form-12-article
        // const newRowId =  "div_id_" + newName
        // newFormRow.attr("id", newRowId)

        // add new class for basic graphic animation
        newFormRow.removeClass("empty-form-div");
        newFormRow.addClass("col-md-4");

        // update form group id
        let parentDiv;
        if (element.attr('type') != 'checkbox') {
            parentDiv = element.parent().parent();
        } else {
            parentDiv = element.parent();
        }
        // update label id

        let inputLabel = parentDiv.find("label")
        if (element.attr('type') != 'hidden') {
            inputLabel.attr("for", "id_" + newName)
            const newDivId = "div_id_" + newName
            parentDiv.attr('id', newDivId)
        }
        // return created row
        return newFormRow

    }



    $('#add-new-form').click(function (e) {
        e.preventDefault()
        // form id like #id_form-TOTAL_FORMS
        let formId = "id_form-TOTAL_FORMS";

        // copy empty form
        let emptyRow = $("#empty-form-div").clone();

        // remove id from new form
        emptyRow.attr("id", null)

        // Insert row after last row

        // get starting form count for formset
        const totalForms = parseInt($('#' + formId).val());

        // create new form row from empty form row

        let newFormRow;
        emptyRow.find("input, select, textarea").each(function () {
            newFormRow = updateEmptyFormIDs($(this), totalForms)
        })


        // insert new form at the end of the last form row
        // $("#hidden-div").after(newFormRow)

        $("#hidden-div").before(emptyRow)

        // // update total form count (to include new row)
        $('#' + formId).val(totalForms + 1);


        // requires: jQuery Color: https://code.jquery.com/color/jquery.color-2.1.2.min.js




    });
    $('input:checkbox').each(function () {
        $(this).parent().find('label').text('حذف')
    })
})

