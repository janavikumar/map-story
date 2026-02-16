# NYT-Style Scrollytelling Map - Refactored Version

## What's Different Now?

Your scrollytelling map is now split into **three separate files** for better organization and security:

```
project/
├── index.html          Clean HTML structure (no story content)
├── app.js              Map application logic (reusable)
└── story-config.js     YOUR story, data, and narrative
```

## Why This Structure?

**Before:** Everything in one HTML file meant anyone could view source and see your entire story.

**Now:** 
- ✅ Separate your content from your code
- ✅ Protect story-config.js until you're ready to publish
- ✅ Reuse app.js for multiple projects
- ✅ Easier to maintain and update

## Quick Start

1. **Get a Mapbox token** at https://account.mapbox.com/
2. **Edit `story-config.js`** - Replace the token and add your story
3. **Open `index.html`** in a browser

That's it! Your map will dynamically build from the config.

## Editing Your Story

All your content lives in **story-config.js**. Here's what you can customize:

### Header
```javascript
header: {
    title: "Your Amazing Story Title",
    byline: "By Your Name · Date",
    intro: "Your compelling intro paragraph..."
}
```

### Chapters
Each chapter is a scroll section with its own map position:

```javascript
chapters: [
    {
        id: '0',  // Must be unique and sequential
        title: 'Chapter Title',
        stat: '1.2M',  // Optional big number
        content: [
            "First paragraph...",
            "Second paragraph..."
        ],
        caption: 'Optional caption text',  // Optional
        map: {
            center: [-122.4194, 37.7749],  // [lng, lat] San Francisco
            zoom: 12,        // 0-22 (higher = closer)
            pitch: 45,       // 0-60 (tilt angle)
            bearing: 0,      // 0-360 (rotation)
            duration: 2000   // Animation time (ms)
        }
    }
    // Add more chapters...
]
```

### Map Settings
```javascript
mapSettings: {
    accessToken: 'YOUR_MAPBOX_TOKEN',
    style: 'mapbox://styles/mapbox/light-v11',
    interactive: false  // Disable user panning during scroll
}
```

### Data & Layers
Add your GeoJSON data and map layers:

```javascript
data: {
    sources: [
        {
            id: 'my-data',
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [/* your features */]
            }
        }
    ],
    layers: [
        {
            id: 'my-layer',
            type: 'circle',
            source: 'my-data',
            paint: {
                'circle-radius': 10,
                'circle-color': '#ff0000'
            }
        }
    ]
}
```

## Advanced Customization

### Loading External Data

Instead of embedding GeoJSON in the config, load from a file:

```javascript
sources: [
    {
        id: 'my-data',
        type: 'geojson',
        data: './data/my-data.geojson'  // External file
    }
]
```

### Custom Chapter Actions

Add custom behavior when entering/exiting chapters:

**In app.js or in a `<script>` tag in index.html:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
    const app = new ScrollyMap(storyConfig);
    
    app.onChapterEnter = (stepId, chapter) => {
        if (stepId === '2') {
            // Show specific layer on chapter 2
            app.toggleLayer('heatmap-layer', true);
        }
    };
    
    app.onChapterExit = (stepId) => {
        if (stepId === '2') {
            // Hide layer when leaving chapter 2
            app.toggleLayer('heatmap-layer', false);
        }
    };
});
```

### Public API Methods

The `ScrollyMap` class exposes these methods:

```javascript
// Get the map instance
const map = app.getMap();

// Add a new data source
app.addDataSource('new-source', 'geojson', {
    type: 'FeatureCollection',
    features: [...]
});

// Add a new layer
app.addLayer({
    id: 'new-layer',
    type: 'circle',
    source: 'new-source',
    paint: { 'circle-radius': 5 }
});

// Toggle layer visibility
app.toggleLayer('my-layer', true);  // show
app.toggleLayer('my-layer', false); // hide

// Set layer filter
app.setFilter('my-layer', ['==', ['get', 'year'], 2024]);
```

## File Organization

### Option 1: All in One Folder (Simple)
```
my-project/
├── index.html
├── app.js
├── story-config.js
└── data/
    └── my-data.geojson
```

### Option 2: Organized by Type (Better)
```
my-project/
├── index.html
├── js/
│   ├── app.js
│   └── story-config.js
├── data/
│   └── my-data.geojson
└── css/
    └── custom-styles.css  (optional)
```

Update script paths in `index.html`:
```html
<script src="js/story-config.js"></script>
<script src="js/app.js"></script>
```

### Option 3: Multiple Stories (Advanced)
```
my-project/
├── index.html
├── app.js  (shared application logic)
└── stories/
    ├── immigration-story.js
    ├── climate-story.js
    └── housing-story.js
```

Load different stories by changing the script tag:
```html
<script src="stories/immigration-story.js"></script>
```

## Security

Your story content in `story-config.js` can be protected before publication. See **SECURITY.md** for detailed options:

- Server-side access restrictions
- API-based loading with authentication
- Time-based publication
- Environment-based access

## Layer Types Quick Reference

### Circles
```javascript
{
    id: 'points',
    type: 'circle',
    source: 'my-points',
    paint: {
        'circle-radius': 8,
        'circle-color': '#ff0000',
        'circle-opacity': 0.8
    }
}
```

### Heatmap
```javascript
{
    id: 'heatmap',
    type: 'heatmap',
    source: 'my-points',
    paint: {
        'heatmap-weight': 1,
        'heatmap-intensity': 1,
        'heatmap-radius': 30
    }
}
```

### Choropleth (Filled Polygons)
```javascript
{
    id: 'regions',
    type: 'fill',
    source: 'my-polygons',
    paint: {
        'fill-color': [
            'interpolate',
            ['linear'],
            ['get', 'value'],
            0, '#fff',
            100, '#f00'
        ],
        'fill-opacity': 0.7
    }
}
```

### Lines
```javascript
{
    id: 'routes',
    type: 'line',
    source: 'my-lines',
    paint: {
        'line-color': '#0000ff',
        'line-width': 3
    }
}
```

## Map Styles

Change the base map in `story-config.js`:

```javascript
mapSettings: {
    style: 'mapbox://styles/mapbox/STYLE_NAME'
}
```

**Available styles:**
- `light-v11` - Clean, minimal (default)
- `dark-v11` - Dark theme
- `streets-v12` - Standard street map
- `satellite-v9` - Satellite imagery
- `outdoors-v12` - Topographic
- `navigation-day-v1` - Navigation style

Or create custom styles at https://studio.mapbox.com/

## Finding Coordinates

**Method 1: Google Maps**
1. Right-click on location
2. Click "What's here?"
3. Copy coordinates (flip to [lng, lat] format!)

**Method 2: Mapbox**
1. Go to https://www.mapbox.com/
2. Search for location
3. Copy coordinates from URL

**Method 3: geojson.io**
1. Go to https://geojson.io
2. Click on map
3. See coordinates in the right panel

**Remember:** Mapbox uses [longitude, latitude] (not [lat, lng])!

## Common Issues

**Map doesn't appear:**
- Check console for errors (F12)
- Verify Mapbox token is correct
- Ensure you're connected to internet

**Story content doesn't show:**
- Check that `story-config.js` is loaded before `app.js`
- Verify chapter IDs match in config and HTML data-step
- Check browser console for JavaScript errors

**Coordinates are wrong:**
- Remember: [longitude, latitude] not [lat, lng]
- Longitude is -180 to 180 (negative = west)
- Latitude is -90 to 90 (negative = south)

**Scroll doesn't trigger map:**
- Ensure each chapter has a unique `id`
- Check that chapter `id` matches HTML `data-step`
- Try adjusting Scrollama `offset` (0-1)

## Performance Tips

1. **Simplify GeoJSON** - Remove unnecessary precision
2. **Use appropriate zoom levels** - Don't load city data at country zoom
3. **Limit data points** - Use clustering for thousands of points
4. **Vector tiles for large datasets** - Convert to Mapbox vector tiles
5. **Lazy load data** - Only load when chapter is active

## Publishing

See the original README.md for publishing options:
- GitHub Pages (free)
- Netlify (free, easy)
- Your own server

## Next Steps

1. Edit `story-config.js` with your content
2. Add your Mapbox token
3. Customize the styling
4. Add your data
5. Test thoroughly
6. Review SECURITY.md if content is sensitive
7. Publish!

## Examples of What You Can Build

- Immigration flow maps with animated routes
- Climate change impact by region with choropleths
- Historical events with timeline-based reveals
- Real estate trends with heatmaps
- Election results with state-by-state zooms
- Travel guides with photo markers
- Urban development before/after comparisons

The structure is flexible - adapt it to your story!
