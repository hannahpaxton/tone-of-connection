"use strict";

mapboxgl.accessToken = 'pk.eyJ1IjoiaHBheHRvbjIiLCJhIjoiY2txYnBqbmw1MGQyOTJvb2VzemlxYzV6MCJ9.TDzOcJidhvzgwrhH-gBZyQ';
var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/dark-v10', // style URL
    center: [-96, 38], // starting position [lng, lat]
    zoom: 3 // starting zoom
});

map.scrollZoom.disable();
map.addControl(new mapboxgl.NavigationControl());
map.doubleClickZoom.disable();


$.get('/api/posts', (posts) => {
    for (const post of posts) {
        var postMarker = new mapboxgl.Marker({
            color: post.color,
        }).setLngLat([post.lng, post.lat])
        .setPopup(new mapboxgl.Popup().setHTML('<strong>' + post.prompt + '</strong><p>' + post.post_text + '</p>'))
        .addTo(map); 
    }
});