(function ($) {
    $(function () {

        let i = 0;
        $('.ymap_field').each(function () {
            let input = $(this);

            let ymap_div = $('<div style="float:left"></div>').attr('id', 'ymap_' + i);
            input.data('ymap_div', ymap_div);

            q = ymap_div.insertAfter(input);
            q.css({'width': parseInt(input.attr('data-size_width')), 'height': parseInt(input.attr('data-size_height'))});
            init_map(input);
            i++;
        })
    })
})(django.jQuery);

function init_map(input) {
    ymaps.ready(function () {

        let map = new ymaps.Map(input.data('ymap_div').attr('id'), {
            center: [41, 82],
            zoom: 13,
            controls: ['zoomControl', 'typeSelector', 'rulerControl']
        });

        let searchControl = new ymaps.control.SearchControl({
            options: {
                noPlacemark: true
            }
        });

        map.controls.add(searchControl);

        map.events.add('click', function (e) {
            let coords = e.get('coords');
            django_ymap_change_mark(input, coords)

        });

        input.data("ymap", map);
        let value = input.val();
        value = JSON.parse(value);
        if (value['coordinates'].length === 0) {
            django_ymap_set_center_by_query(input.attr('data-start_query'), map)
        }
        else {

            let current = value['coordinates'];
            django_ymap_set_center_by_coords(current, map);
            django_ymap_change_mark(input, current);
        }
    });

}
function django_ymap_set_center_by_coords(coords, map) {

    map.zoomRange.get(coords).then(function (range) {
        map.setCenter(coords, range[13])
    })
}

function django_ymap_change_mark(input, coords) {
    let mark = input.data('ymap_mark');
    let map = input.data('ymap');
    if (mark) map.geoObjects.remove(mark);

    mark = new ymaps.Placemark(coords);
    input.data('ymap_mark', mark);
    ymaps.geocode(coords).then(function (res) {
        let first = res.geoObjects.get(0);
        let address = first.getAddressLine();
        mark.properties.set({
            balloonContent: address
        });
        map.geoObjects.add(mark);
        input.attr('value', JSON.stringify({'coordinates': coords, 'address': address}))
    }).fail(e => {
        map.geoObjects.add(mark);
        input.attr('value', JSON.stringify({'coordinates': coords, 'address': null}))
    });
}

function django_ymap_set_center_by_query(query, map) {

    ymaps.geocode(query, {results: 1}).then(function (res) {
        let coords = res.geoObjects.get(0).geometry.getCoordinates();
        let firstGeoObject = res.geoObjects.get(0);
        map.setBounds(firstGeoObject.properties.get('boundedBy'));
    });
}
