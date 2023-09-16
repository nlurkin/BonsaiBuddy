function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix, reset=true, copied_index=-1) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    if (copied_index==-1) {
        copied_index = total-1;
    }
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset]):not(button)').each(function() {
        var name = $(this).attr('name').replace('-' + copied_index + '-', '-' + total + '-');
        var id = 'id_' + name;
        if(reset && $(this).attr('name').indexOf("tree_name")==-1)
            $(this).attr({'name': name, 'id': id}) .val('').removeAttr('checked');
        else
            $(this).attr({'name': name, 'id': id});
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + copied_index + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    newElement.find('div.accordion-collapse').each(function() {
        var id = $(this).attr('id').replace('-' + copied_index + '-', '-' + total + '-');
        $(this).attr({'id': id, 'class': 'accordion-collapse collapse show'});
    });
    newElement.find('button.accordion-button').each(function() {
        var target = $(this).attr('data-bs-target').replace('-' + copied_index + '-', '-' + total + '-');
        var controls = $(this).attr('aria-controls').replace('-' + copied_index + '-', '-' + total + '-');
        $(this).attr({'data-bs-target': target, 'aria-controls': controls, 'class': 'accordion-button', 'aria-expanded': "true"});
        $(this).html("Association #" + total)
    });
    $('.form-row:last').after(newElement);
    newElement.find('tags.tagify').each(function() {
        script = $(this).siblings("script")[0];
        script.innerHTML = script.innerHTML.replace('-' + copied_index + '-', '-' + total + '-');
        eval(script.innerHTML);
        $(this).remove();
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    return false;
}
