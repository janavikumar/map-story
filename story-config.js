// story-config.js
// This file contains all your story content and can be kept private/secure

const storyConfig = {
    // hed/dek
    header: {
        title: 'They Drew the <a href="migration-map.html" style="color:inherit;text-decoration:underline;text-underline-offset:4px;">Lines</a>. Now They Guard Them.',
        byline: "By JANAVI KUMAR · Feb 13, 2026",
        intro: ["Empires remade entire nations, reshaping lives, borders, and languages. Today, those same ties often pull refugees towards their former colonizers. <br>But the colonizers are closing their doors."]
    },

    // map config
    mapSettings: {
        accessToken: 'pk.eyJ1IjoiamFuYXZpOTYiLCJhIjoiY21ubmh3ZzFlMXd2dTJwcTZwdG5zbGwzayJ9.t-K_o05Petxn5ZGSy_dZ4Q',
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
            title: 'The Corridors Empires Left Behind',
            content: [
                "The world's refugee crisis looks chaotic on the surface. But look closer at where people move, and a quieter logic emerges. Refugees do not travel randomly. They follow the old grooves of empire, moving along linguistic lines, colonial ties, and economic relationships that were carved out over centuries and never fully healed.",
                "Three empires. Three former colonies. Three sets of closed doors. France turned away Haiti. The United States turned away Mexico and Central America. Britain turned away India. In each case, the same power that created the conditions for displacement is now refusing to receive the displaced."
            ],
            hideLayers: ['port-au-prince-dot', 'oaxaca-dot', 'mumbai-dot'],
            map: {
                center: [-20.0, 15.0],
                zoom: 1.8,
                pitch: 0,
                bearing: 0,
                duration: 2000
            }
        },
        {
            id: '1',
            title: 'France and Haiti: The Bill for Freedom',
            stat: '150 years',
            content: [
                "Haiti became the first Black republic in 1804, born from the only successful slave revolt in history. It was an act of defiance that terrified the colonial world, and France made them pay for it. In 1825, Paris sent warships to Port-au-Prince and demanded 150 million gold francs as compensation for the 'loss' of its enslaved workforce. To avoid re-colonization, Haiti agreed. The debt, financed through French and later American banks, was not fully paid off until 1947.",
                "The economic drain stunted Haiti for generations. Infrastructure went unbuilt. Sovereignty came at the price of perpetual poverty. When a catastrophic earthquake struck in 2010, killing more than 200,000 people and displacing over a million, the world watched. Haitian migrants and asylum seekers began moving toward France, the country whose language they spoke, whose culture had been forcibly grafted onto theirs for two centuries.",
                "France's response was to tighten. Visa requirements for Haitians were stiffened. Border controls were reinforced. In 2021 and 2022, following a second earthquake and the assassination of President Jovenel Moïse, France deported hundreds of Haitians even as the country descended into gang violence. The linguistic and historical corridor remained, but the door was closing."
            ],
            caption: 'Haiti paid reparations to France from 1825 until 1947, a debt incurred for the crime of winning its own freedom.',
            showLayers: ['port-au-prince-dot'],
            hideLayers: ['oaxaca-dot', 'mumbai-dot'],
            map: {
                center: [-72.3388, 18.5392],
                zoom: 11,
                pitch: 0,
                bearing: 0,
                duration: 2500
            }
        },
        {
            id: '2',
            title: 'The United States and Mexico: A Border Drawn in Sand',
            stat: '2.4 million',
            content: [
                "In 1848, the United States took nearly half of Mexico's territory. The Treaty of Guadalupe Hidalgo ended the Mexican-American War and transferred what is now California, Arizona, New Mexico, Nevada, Utah, and parts of Colorado to Washington. Overnight, tens of thousands of Mexicans became foreigners in the land where their families had lived for generations.",
                "Over the next century and a half, U.S. intervention across Central America compounded the displacement. In Guatemala, a CIA-backed coup in 1954 toppled a democratically elected government, unleashing decades of civil war. In El Salvador and Honduras, U.S.-backed security forces were implicated in mass atrocities during the Cold War. The violence those interventions seeded is still driving people north.",
                "Today, the U.S.-Mexico border is the most heavily militarized in the world. In fiscal year 2023, Customs and Border Protection recorded over 2.4 million migrant encounters, many of them asylum seekers fleeing conditions that American foreign policy helped create. Title 42, rapid deportation policies, and family separations became the tools of a nation that built an economy on migrant labor while refusing to acknowledge its share of responsibility for why those migrants were moving in the first place."
            ],
            caption: 'The number of migrant encounters at the U.S.-Mexico border in FY2023, a record high.',
            showLayers: ['oaxaca-dot'],
            hideLayers: ['port-au-prince-dot', 'mumbai-dot'],
            map: {
                center: [-96.7270, 17.0732],
                zoom: 11,
                pitch: 0,
                bearing: 0,
                duration: 2500
            }
        },
        {
            id: '3',
            title: 'Britain and India: The Windrush Betrayal',
            stat: '1 in 6',
            content: [
                "At its height, the British Empire controlled roughly a quarter of the world's land surface. In India, two centuries of colonial rule extracted an estimated $45 trillion in wealth, dismantled local industries, engineered famines, and finally, in 1947, drew a partition line so hastily conceived that it displaced up to 20 million people in months. The Partition of India remains one of the largest forced migrations in recorded history.",
                "When Britain needed labor to rebuild after World War II, it turned to the Empire. The British Nationality Act of 1948 gave Commonwealth citizens the right to live and work in the United Kingdom. Hundreds of thousands came from India, Pakistan, Bangladesh, and the Caribbean, welcomed as workers, often treated as second-class residents. By the 1970s, successive immigration acts had begun clawing back those rights.",
                "The Windrush scandal, exposed in 2018, revealed that the Home Office had systematically destroyed the landing cards of Commonwealth migrants who had arrived before 1973, making it impossible for them to prove their legal status. Dozens were wrongfully deported. Hundreds lost jobs, homes, and access to healthcare. Roughly one in six South Asian asylum applicants today is refused at the initial decision stage. The empire that once moved people across oceans to serve its needs now asks them to prove they belong."
            ],
            caption: 'Approximately one in six asylum applicants from South Asia is refused at the initial decision stage in the UK.',
            showLayers: ['mumbai-dot'],
            hideLayers: ['port-au-prince-dot', 'oaxaca-dot'],
            map: {
                center: [72.8777, 19.0760],
                zoom: 11,
                pitch: 0,
                bearing: 0,
                duration: 2500
            }
        }
    ],

    // outro
    outro: {
        title: "A Debt Still Owed",
        content: "The corridors refugees travel today are not random. They trace the old nerve lines of empire, the routes of language, law, and labor that colonial powers spent centuries carving into the world. When Haitians move toward France, when Central Americans move toward the United States, when South Asians move toward Britain, they are following maps drawn long before they were born. The question is not why they come. The question is why the doors are closing."
    },

    // data!
    data: {
        sources: [
            {
                id: 'port-au-prince',
                type: 'geojson',
                data: {
                    type: 'Feature',
                    geometry: { type: 'Point', coordinates: [-72.3388, 18.5392] },
                    properties: {}
                }
            },
            {
                id: 'oaxaca',
                type: 'geojson',
                data: {
                    type: 'Feature',
                    geometry: { type: 'Point', coordinates: [-96.7270, 17.0732] },
                    properties: {}
                }
            },
            {
                id: 'mumbai',
                type: 'geojson',
                data: {
                    type: 'Feature',
                    geometry: { type: 'Point', coordinates: [72.8777, 19.0760] },
                    properties: {}
                }
            }
        ],
        layers: [
            {
                id: 'port-au-prince-dot',
                type: 'circle',
                source: 'port-au-prince',
                layout: { visibility: 'none' },
                paint: {
                    'circle-radius': ['interpolate', ['linear'], ['zoom'], 3, 4, 11, 20],
                    'circle-color': '#d32f2f',
                    'circle-opacity': 0.8,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff'
                }
            },
            {
                id: 'oaxaca-dot',
                type: 'circle',
                source: 'oaxaca',
                layout: { visibility: 'none' },
                paint: {
                    'circle-radius': ['interpolate', ['linear'], ['zoom'], 3, 4, 11, 20],
                    'circle-color': '#d32f2f',
                    'circle-opacity': 0.8,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff'
                }
            },
            {
                id: 'mumbai-dot',
                type: 'circle',
                source: 'mumbai',
                layout: { visibility: 'none' },
                paint: {
                    'circle-radius': ['interpolate', ['linear'], ['zoom'], 3, 4, 11, 20],
                    'circle-color': '#d32f2f',
                    'circle-opacity': 0.8,
                    'circle-stroke-width': 2,
                    'circle-stroke-color': '#ffffff'
                }
            }
        ]
    }
};

// export default storyConfig;