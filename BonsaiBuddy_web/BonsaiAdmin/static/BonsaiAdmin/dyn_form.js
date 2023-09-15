function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset]):not(button)').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        if($(this).attr('name').indexOf("tree_name")==-1)
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        else
            $(this).attr({'name': name, 'id': id});
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
          forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
          $(this).attr({'for': forValue});
        }
    });
    newElement.find('div.accordion-collapse').each(function() {
        var id = $(this).attr('id').replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'id': id, 'class': 'accordion-collapse collapse show'});
    });
    newElement.find('button.accordion-button').each(function() {
        var target = $(this).attr('data-bs-target').replace('-' + (total-1) + '-', '-' + total + '-');
        var controls = $(this).attr('aria-controls').replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'data-bs-target': target, 'aria-controls': controls, 'class': 'accordion-button', 'aria-expanded': "true"});
        $(this).html("Association #" + total)
    });
    $(selector).after(newElement);
    newElement.find('tags.tagify').each(function() {
        script = $(this).siblings("script")[0];
        script.innerHTML = script.innerHTML.replace('-' + (total-1) + '-', '-' + total + '-');
        eval(script.innerHTML);
        $(this).remove();
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    return false;
}
