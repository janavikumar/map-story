// app.js
// main application logic - this is public

class ScrollyMap {
    constructor(config) {
        this.config = config;
        this.map = null;
        this.scroller = null;
        this.init();
    }

    init() {
        this.buildHTML();
        this.initMap();
    }

    buildHTML() {
        // Build header
        const header = document.getElementById('header');
        header.innerHTML = `
            <h1>${this.config.header.title}</h1>
            <div class="byline">${this.config.header.byline}</div>
            <p class="intro">${this.config.header.intro}</p>
        `;

        // Build legend
        const legend = document.getElementById('legend');
        let legendHTML = `<h4>${this.config.legend.title}</h4>`;
        this.config.legend.items.forEach(item => {
            legendHTML += `
                <div class="legend-item">
                    <div class="legend-color" style="background: ${item.color};"></div>
                    <span>${item.label}</span>
                </div>
            `;
        });
        legend.innerHTML = legendHTML;

        // Build story steps
        const story = document.getElementById('story');
        this.config.chapters.forEach((chapter, index) => {
            const step = document.createElement('section');
            step.className = 'step';
            step.setAttribute('data-step', chapter.id);

            let contentHTML = `<h2>${chapter.title}</h2>`;
            
            if (chapter.stat) {
                contentHTML += `<div class="stat">${chapter.stat}</div>`;
            }

            chapter.content.forEach(paragraph => {
                contentHTML += `<p>${paragraph}</p>`;
            });

            if (chapter.caption) {
                contentHTML += `<p class="caption">${chapter.caption}</p>`;
            }

            step.innerHTML = `<div class="step-content">${contentHTML}</div>`;
            story.appendChild(step);
        });

        // Build outro
        const outro = document.getElementById('outro');
        outro.innerHTML = `
            <h2>${this.config.outro.title}</h2>
            <p>${this.config.outro.content}</p>
        `;
    }

    initMap() {
        mapboxgl.accessToken = this.config.mapSettings.accessToken;

        // Get initial chapter settings
        const initialChapter = this.config.chapters[0].map;

        this.map = new mapboxgl.Map({
            container: 'map',
            style: this.config.mapSettings.style,
            center: initialChapter.center,
            zoom: initialChapter.zoom,
            pitch: initialChapter.pitch,
            bearing: initialChapter.bearing,
            interactive: this.config.mapSettings.interactive,
            attributionControl: false
        });

        // Add navigation controls
        this.map.addControl(new mapboxgl.NavigationControl(), 'top-left');

        // Wait for map to load
        this.map.on('load', () => {
            this.loadData();
            this.setupScrollama();
        });

        // Check for token
        if (mapboxgl.accessToken.includes('example')) {
            console.warn('⚠️ Please replace the Mapbox token in story-config.js');
        }
    }

    loadData() {
        // Add data sources
        this.config.data.sources.forEach(source => {
            this.map.addSource(source.id, {
                type: source.type,
                data: source.data
            });
        });

        // Add layers
        this.config.data.layers.forEach(layer => {
            this.map.addLayer({
                id: layer.id,
                type: layer.type,
                source: layer.source,
                paint: layer.paint,
                layout: layer.layout || {}
            });
        });
    }

    setupScrollama() {
        this.scroller = scrollama();

        this.scroller
            .setup({
                step: '.step',
                offset: 0.5,
                progress: true
            })
            .onStepEnter(response => {
                const stepId = response.element.dataset.step;
                const chapter = this.config.chapters.find(c => c.id === stepId);

                if (chapter && chapter.map) {
                    const panelPadding = window.innerWidth >= 768
                        ? { left: 680, right: 0, top: 0, bottom: 0 }
                        : { left: 0, right: 0, top: 0, bottom: 0 };

                    this.map.flyTo({
                        center: chapter.map.center,
                        zoom: chapter.map.zoom,
                        pitch: chapter.map.pitch,
                        bearing: chapter.map.bearing,
                        duration: chapter.map.duration,
                        padding: panelPadding,
                        essential: true
                    });
                }

                // Show/hide layers defined in the chapter
                if (chapter && chapter.showLayers) {
                    chapter.showLayers.forEach(layerId => {
                        if (this.map.getLayer(layerId)) {
                            this.map.setLayoutProperty(layerId, 'visibility', 'visible');
                        }
                    });
                }
                if (chapter && chapter.hideLayers) {
                    chapter.hideLayers.forEach(layerId => {
                        if (this.map.getLayer(layerId)) {
                            this.map.setLayoutProperty(layerId, 'visibility', 'none');
                        }
                    });
                }

                // Call custom chapter handler if defined
                if (this.onChapterEnter) {
                    this.onChapterEnter(stepId, chapter);
                }
            })
            .onStepExit(response => {
                // Call custom exit handler if defined
                if (this.onChapterExit) {
                    this.onChapterExit(response.element.dataset.step);
                }
            });

        // Setup resize listener
        window.addEventListener('resize', () => {
            this.scroller.resize();
        });
    }

    // Public methods for custom interactions

    // Add a new data source
    addDataSource(id, type, data) {
        if (this.map.getSource(id)) {
            console.warn(`Source ${id} already exists`);
            return;
        }
        this.map.addSource(id, { type, data });
    }

    // Add a new layer
    addLayer(layerConfig) {
        if (this.map.getLayer(layerConfig.id)) {
            console.warn(`Layer ${layerConfig.id} already exists`);
            return;
        }
        this.map.addLayer(layerConfig);
    }

    // Toggle layer visibility
    toggleLayer(layerId, visible) {
        const visibility = visible ? 'visible' : 'none';
        this.map.setLayoutProperty(layerId, 'visibility', visibility);
    }

    // Update layer filter
    setFilter(layerId, filter) {
        this.map.setFilter(layerId, filter);
    }

    // Get the map instance for advanced customization
    getMap() {
        return this.map;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Create the map application
    const app = new ScrollyMap(storyConfig);

    // Optional: Add custom chapter handlers
    app.onChapterEnter = (stepId, chapter) => {
        console.log('Entered chapter:', stepId);
        
        // Example: Toggle layers based on chapter
        // if (stepId === '1') {
        //     app.toggleLayer('my-custom-layer', true);
        // }
    };

    app.onChapterExit = (stepId) => {
        console.log('Exited chapter:', stepId);
    };

    // Make app globally available for debugging/customization
    window.scrollyApp = app;
});
