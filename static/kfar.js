function log(msg){
    console.log(arguments);
    if('string' === typeof msg){
        $('#log').prepend(
            $('<div>').html(new Date().toLocaleTimeString() + ' - ' + msg)
        );
    }
};

function get(url, data, callback){
    $.ajax({
        url: url,
        dataType: 'jsonp',
        data: data,
        success:function(data){
            if(null !== data && 'string' === typeof data.error) log(data.error);
            callback(data);
        },
        error:function(){
            log('Unable to retrieve ' + url);
        }
    });
};

function addmarkertolayer(layer, latlng, iconname, text, click){
    var icon =  L.icon({
        iconUrl: '/static/images/' + iconname + '.png',
        iconSize: [32, 32],
        iconAnchor: [1, 30],
    });
    var marker = L.marker([latlng[0], latlng[1]], {'icon': icon}).bindPopup(text).on('click', click);
    layer.addLayer(marker);
}

var map;
function getdeliveries(position, range){
    log('getting deliveries');
    get('deliveriesinrange.jsonp', {'lat': position.lat, 'lng': position.lng, 'radius': range}, function(deliveries){
        var fromMarkers = new L.MarkerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 50 });
        var toMarkers = new L.MarkerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 50 });

        L.circle(position, range * 110000,{
            color: 'red',
            weight: '0.5',
            fillColor: '#f00',
            fillOpacity: 0.1
        }).addTo(map);

        $.each(deliveries, function(idx, hash){
            get('delivery.jsonp', {id: hash}, function(delivery){
                log('got delivery ' + hash + ':' + delivery['fromLatlng'] + delivery['time']);
                var popuptext = 'id:' + idx + " from<br>route:" + delivery['time'] + 'min';
                popuptext += '<br>' + delivery['address']
                addmarkertolayer(
                    fromMarkers,
                    delivery['fromLatlng'],
                    'green_flag_icon',
                    "from " + popuptext,
                    function(e){
                        L.polyline(delivery.path, {
                            color: 'red',
                            dashArray: "5, 6, 2, 6",
                            weight: '2',
                        }).addTo(map);
                        log(
                            '"Oh lawdy I\'ve been clicked!", <span style="color: gray;">said marker '
                            + hash
                            + ' (the one at '
                            + delivery['fromLatlng']
                            + ' with the popup "'
                            + e.target._popup._content
                            + '".</span>',
                            e
                        );
                    }
                );
                addmarkertolayer(toMarkers, delivery['toLatlng'], 'pink_flag_icon', "to " + popuptext);
            });
        });
        map.addLayer(fromMarkers);
        map.addLayer(toMarkers);
    });
}

function getcurrentposition(callback, manual){
    // Manual prompting for non mobile devices
    // TODO Should be done with cookie
    if('undefined' !== typeof(manual) || /i686/i.test(navigator.userAgent)){
        var position = prompt('position', '32.0695:34.7987').split(':');
        callback({'lat': position[0], 'lng': position[1]}, 0);
    }else{
        map.on('locationerror', function onLocationError(e){
            log(e.message, e);
            return getcurrentposition(callback, true);
        });
        map.on('locationfound', function(e){
            callback(e.latlng, e.accuracy);
        });
        map.locate({setView: true, maxZoom: 14, timeout: 3000});
    }
}

$(function(){
    $('#nojs').remove();
    log('js detected');

    // Initialize, center and zoom map
    map = L.map('map').setView([32.0695, 34.7987], 13);
    source_mapbox = 'https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png'
    source_openstreetmap = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    source_opencyclemap = 'http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png'

    //TODO review https://gist.github.com/mourner/1804938 - it should be a better solution.

    L.tileLayer(source_mapbox,{
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' + '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' + 'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'examples.map-zr0njcqy'
    }).addTo(map);

    getcurrentposition(function(latlng, accuracy){
        var radius = accuracy / 2;
        var meIcon =  L.icon({
            iconUrl: '/static/images/cyan_pin_icon.png',
            iconSize: [32, 32],
            iconAnchor: [9, 30],
        });
        L.marker(latlng, {icon: meIcon}).addTo(map).bindPopup('you are ' + radius + ' meters from here');

        var range = prompt('range', '0.02');
        getdeliveries(latlng, range);
    });
});