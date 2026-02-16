// story-config.js
// This file contains all your story content and can be kept private/secure

const storyConfig = {
    // hed/dek
    header: {
        title: "Mapping Movement",
        byline: "By Janavi Kumar · Feb 13, 2026",
        intro: "write a description hereeee"
    },

    // map config
    mapSettings: {
        accessToken: 'YOUR_MAPBOX_TOKEN_HERE',
        style: 'mapbox://styles/mapbox/light-v11',
        interactive: false
    },

    // legend configuration
    legend: {
        title: "Legend",
        items: [
            { color: '#d32f2f', label: 'High density' },
            { color: '#1976d2', label: 'Medium density' },
            { color: '#388e3c', label: 'Low density' }
        ]
    },

    // "story" chapters - each step corresponds to a scroll section
    chapters: [
        {
            id: '0',
            title: 'Section 1',
            content: [
                "blah blah blah paragraph 1 ."
            ],
            map: {
                center: [-98.5795, 39.8283],
                zoom: 3.5,
                pitch: 0,
                bearing: 0,
                duration: 2000
            }
        },
        {
            id: '1',
            title: 'Section 2',
            stat: 'Some StatisticM',
            content: [
                "paragraph 22222222 paragraph 22222222 paragraph 22222222 paragraph, 22222222 paragraph 22222222 paragraph 22222222 paragraph 22222222 paragraph 22222222paragraph 22222222 ."
            ],
            caption: 'catoindf osijsodifjsodfsdfs',
            map: {
                center: [-74.0060, 40.7128],
                zoom: 11,
                pitch: 45,
                bearing: 0,
                duration: 2000
            }
        },
        {
            id: '2',
            title: 'Section 3',
            stat: 'anoter statistic',
            content: [
                "PARAGRAPH 3e."
            ],
            caption: 'capdfjsldkfnjlsdkfjsldkfjlsdf',
            map: {
                center: [-87.6298, 41.8781],
                zoom: 11,
                pitch: 45,
                bearing: 0,
                duration: 2000
            }
        },
        {
            id: '3',
            title: 'Titleeeee Secrion 4',
            stat: '3.9M',
            content: [
                "lkdsjflskdjflsdkfjlskdfjlsdkfjlsdkfjlsdf"
            ],
            caption: 'sdjhskdjfhskdjfhskdjfhsdkjfhskdjfhksdf',
            map: {
                center: [-118.2437, 34.0522],
                zoom: 11,
                pitch: 45,
                bearing: 0,
                duration: 2000
            }
        },
        {
            id: '4',
            title: 'sldkfjlsdkfjlskdjflskdfjlsdkflsdkflsdfs',
            content: [
                "Wsdjfhskdjfhskdjfhksdjfhksdjf.",
                "sdfkjsldkfjsldkfjsldkfjlsdkfjlsdf."
            ],
            map: {
                center: [-98.5795, 39.8283],
                zoom: 3.5,
                pitch: 0,
                bearing: 0,
                duration: 2000
            }
        }
    ],

    // outro
    outro: {
        title: "OUTROOO",
        content: "sdlfkjsdlkfjsdlkfjlsdkfjlsdkfds."
    },

    // data!
    data: {
        sources: [
            {
                id: 'demo-points',
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [-74.0060, 40.7128]
                            },
                            properties: {
                                title: 'New York',
                                density: 'high'
                            }
                        },
                        {
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [-87.6298, 41.8781]
                            },
                            properties: {
                                title: 'Chicago',
                                density: 'medium'
                            }
                        },
                        {
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [-118.2437, 34.0522]
                            },
                            properties: {
                                title: 'Los Angeles',
                                density: 'high'
                            }
                        }
                    ]
                }
            }
        ],
        layers: [
            {
                id: 'demo-points-layer',
                type: 'circle',
                source: 'demo-points',
                paint: {
                    'circle-radius': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        3, 4,
                        11, 20
                    ],
                    'circle-color': [
                        'match',
                        ['get', 'density'],
                        'high', '#d32f2f',
                        'medium', '#1976d2',
                        'low', '#388e3c',
                        '#999999'
                    ],
                    'circle-opacity': 0.7,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff'
                }
            }
        ]
    }
};

// export default storyConfig;