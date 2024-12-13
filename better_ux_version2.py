import streamlit as st 
import pandas as pd
import geopandas as gpd
import osmnx as ox
import plotly.express as px
import pdfkit
from pyproj import Proj
import streamlit.components.v1 as components

# Set the path to wkhtmltopdf
try:
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    st.success("Anwendung erfolgreich konfiguriert!")
except Exception as e:
    st.error(f"Fehler bei der Konfiguration von pdfkit: {e}")

# Custom CSS for styling Streamlit dashboard
def add_custom_css():
    custom_css = """
    <style>
        .stApp {
            background-color: #000013;
            color: #ffffff;
        }
        .main-content {
            padding: 2rem;
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #FF4B4B;
            color: #ffffff;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #000000;
            transform: scale(1.05);
        }
        .stTabs [role="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stTextInput > div > input {
            border-radius: 10px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stTextInput > label {
            color: #ffffff;
        }
        .stSlider > label {
            color: #ffffff;
        }
        .stMultiselect > label {
            color: #ffffff;
        }
        .stSidebar {
            background-color: #000013;
            border-right: 2px solid #e0e0e0;
            padding: 20px;
            color: #ffffff;
        }
        .coordinate-label {
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #ffffff;
        }
        .stMarkdown p {
            color: #ffffff;
        }
        .uploaded-file-name {
            color: #ffffff;
            font-weight: bold;
        }
        .stRadio > label, .stRadio > div > label {
            color: #ffffff;
        }
        .stSlider > label {
            color: #ffffff;
        }
        .stMultiselect > label {
            color: #ffffff;
        }
        .feedback-label {
            font-weight: bold;
            font-size: 1.2em;
            color: #ffffff;
        }
        .stTextArea > label {
            color: #ffffff;
        }
        .loading-spinner {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Custom JavaScript for interactions
def add_custom_js():
    custom_js = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            let buttons = document.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('click', function() {
                    this.style.backgroundColor = '#357ABD';
                    document.querySelector('.loading-spinner').style.display = 'block';
                });
            });

            // Add animations to buttons
            buttons.forEach(button => {
                button.style.transition = 'transform 0.3s ease';
                button.addEventListener('mouseover', function() {
                    this.style.transform = 'scale(1.1)';
                });
                button.addEventListener('mouseout', function() {
                    this.style.transform = 'scale(1)';
                });
            });
        });

        // Progress steps guide
        window.onload = function() {
            let progressSteps = document.createElement('div');
            progressSteps.innerHTML = `
                <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em; color: #ffffff;">1. Parameter festlegen</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em; color: #ffffff;">2. Daten hochladen</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em; color: #ffffff;">3. Analyse anzeigen</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em; color: #ffffff;">4. Bericht generieren</span>
                    </div>
                </div>
            `;
            document.body.insertBefore(progressSteps, document.body.firstChild);
        };
    </script>
    """
    components.html(custom_js, height=0)

# Helper function to generate colorful report (without dashboard background)
def generate_report(data, feedback):
    try:
        html_content = f"""
        <html>
        <head>
            <title>Infrastrukturbericht</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    margin: 40px;
                }}
                h1 {{
                    color: #4A90E2;
                    text-align: center;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #4A90E2;
                    color: white;
                }}
                .feedback-section {{
                    margin-top: 20px;
                    padding: 20px;
                    border: 2px dashed #4A90E2;
                    background-color: rgba(240, 242, 246, 0.8);
                }}
                .feedback-section h2 {{
                    color: #7ED321;
                }}
            </style>
        </head>
        <body>
            <h1>Infrastrukturbericht</h1>
            {data.to_html(classes='table table-striped', border=0)}
            <div class='feedback-section'>
                <h2>Feedback</h2>
                <p>{feedback}</p>
            </div>
        </body>
        </html>
        """
        output_pdf_path = 'C:/Users/moham/Desktop/Infrascout/report.pdf'
        pdfkit.from_string(html_content, output_pdf_path, configuration=pdfkit_config, options={"enable-local-file-access": ""})
        st.success(f"PDF-Bericht erfolgreich generiert unter {output_pdf_path}!")
    except Exception as e:
        st.error(f"Fehler beim Generieren des PDF: {e}. Bitte stellen Sie sicher, dass lokale Dateizugriffe für wkhtmltopdf aktiviert sind.")


# Analysis function for infrastructure
def analyze_infrastructure_with_apis(
    place_name, density_threshold, proximity_threshold, tags, population_df, busyness_df, air_quality_df, infrastructure_gdf
):
    if population_df.empty:
        st.error("Die Population DataFrame ist leer.")
        return None

    # Convert to GeoDataFrame
    try:
        population_gdf = gpd.GeoDataFrame(
            population_df,
            geometry=gpd.points_from_xy(population_df.Longitude, population_df.Latitude),
            crs="EPSG:4326"
        )
    except Exception as e:
        st.error(f"Fehler beim Konvertieren in GeoDataFrame: {e}")
        return None

    # Reproject population data
    try:
        population_gdf = population_gdf.to_crs(epsg=32632)
    except Exception as e:
        st.error(f"Fehler bei der Neukalibrierung der Populationsdaten: {e}")
        return None

    utm_proj = Proj(proj="utm", zone=32, ellps="WGS84")
    suggested_locations = []

    offset_value = 0.0001  # Small offset to differentiate overlapping points
    seen_coordinates = set()

    for idx, area in population_gdf.iterrows():
        if area['Population Density'] > density_threshold:
            for infra_type in tags['amenity']:
                try:
                    if 'amenity' in infrastructure_gdf.columns:
                        # If the 'amenity' column is present, filter based on the tag
                        nearby = infrastructure_gdf[
                            (infrastructure_gdf['amenity'] == infra_type) &
                            (infrastructure_gdf.geometry.distance(area.geometry) < proximity_threshold)
                        ]
                    else:
                        # If 'amenity' column is not present, consider all infrastructure as one group
                        nearby = infrastructure_gdf[
                            (infrastructure_gdf.geometry.distance(area.geometry) < proximity_threshold)
                        ]

                    if nearby.empty:
                        easting = area.geometry.centroid.x
                        northing = area.geometry.centroid.y
                        longitude, latitude = utm_proj(easting, northing, inverse=True)

                        # Adjust the coordinates slightly if they have already been used
                        while (longitude, latitude) in seen_coordinates:
                            longitude += offset_value
                            latitude += offset_value

                        seen_coordinates.add((longitude, latitude))

                        suggested_locations.append({
                            'Infrastrukturtyp': infra_type.capitalize(),
                            'Vorgeschlagene Breite': latitude,
                            'Vorgeschlagene Länge': longitude,
                            'Bereich': area['Area'],
                            'Bevölkerungsdichte': area['Population Density']
                        })
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung von {infra_type}: {e}")

    if suggested_locations:
        st.success(f"Insgesamt vorgeschlagene Standorte: {len(suggested_locations)}")
    else:
        st.warning("Keine vorgeschlagenen Standorte generiert.")

    return pd.DataFrame(suggested_locations)

# Streamlit app layout with sections/tabs
st.title("Infrascout Dashboard")
st.subheader("Ein fortschrittliches Werkzeug zur Analyse und Verbesserung der Stadtinfrastruktur")

# Add custom CSS and JavaScript
add_custom_css()
add_custom_js()

# Adding a loading spinner
st.markdown("""
<div class="loading-spinner">
    <img src="https://example.com/spinner.gif" alt="Lädt...">
</div>
""", unsafe_allow_html=True)

# Creating tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Parameter festlegen", "Daten hochladen", "Analyse anzeigen", "Bericht generieren"])

with tab1:
    st.header("Eingabeparameter")
    
    # Define 'place_name' in the session state if it doesn't exist
    if 'place_name' not in st.session_state:
        st.session_state.place_name = "Bern, Schweiz"

    # User input for parameters
    place_name = st.text_input("Stadtname", st.session_state.place_name, help="Geben Sie den Namen der Stadt ein, die Sie analysieren möchten.")

    # Update session state if the city name changes
    if st.session_state.place_name != place_name:
        st.session_state.place_name = place_name
        # Clear previously fetched data if city changes
        if "infrastructure_gdf" in st.session_state:
            del st.session_state.infrastructure_gdf
            st.write(f"Stadt geändert zu {place_name}. Vorherige Infrastrukturdaten gelöscht.")

    density_threshold = st.slider("Bevölkerungsdichte-Schwellenwert", 0, 2000, 1000, help="Setzen Sie den Schwellenwert der Bevölkerungsdichte, um Bereiche zu identifizieren, die mehr Infrastruktur benötigen.")
    proximity_threshold = st.slider("Nähe-Schwellenwert (Meter)", 0, 2000, 1000, help="Setzen Sie den Schwellenwert, um zu bestimmen, wie nah bestehende Infrastrukturen sein müssen, um einen Bereich als abgedeckt zu betrachten.")

    # Select infrastructure types
    infra_types = st.multiselect(
        "Wählen Sie die Infrastrukturtypen zur Analyse:",
        [
            'bench', 'toilets', 'waste_basket', 'bicycle_parking', 'drinking_water', 
            'charging_station', 'bus_stop', 'park', 'public_building', 'crossing', 
            'traffic_signals', 'playground', 'sports_centre', 'viewpoint', 'museum', 'information'
        ],
        default=['bench', 'toilets', 'waste_basket', 'bicycle_parking', 'drinking_water'],
        help="Wählen Sie die Infrastrukturen, die Sie analysieren möchten."
    )

    # Store user inputs in session state
    st.session_state.density_threshold = density_threshold
    st.session_state.proximity_threshold = proximity_threshold
    st.session_state.infra_types = infra_types

    # Sidebar for cost estimation
    st.header("")
    costs = {
        'bench': st.sidebar.number_input("Kosten einer Bank (CHF)", value=200),
        'toilets': st.sidebar.number_input("Kosten einer Toilette (CHF)", value=1000),
        'waste_basket': st.sidebar.number_input("Kosten eines Mülleimers (CHF)", value=150),
        'bicycle_parking': st.sidebar.number_input("Kosten für Fahrradparkplatz (CHF)", value=500),
        'drinking_water': st.sidebar.number_input("Kosten eines Trinkwasserbrunnens (CHF)", value=800),
        'charging_station': st.sidebar.number_input("Kosten einer Ladestation (CHF)", value=2000),
        'bus_stop': st.sidebar.number_input("Kosten einer Bushaltestelle (CHF)", value=5000),
        'park': st.sidebar.number_input("Kosten eines Parks (CHF)", value=10000),
        'public_building': st.sidebar.number_input("Kosten eines Öffentlichen Gebäudes (CHF)", value=20000),
        'crossing': st.sidebar.number_input("Kosten eines Übergangs (CHF)", value=300),
        'traffic_signals': st.sidebar.number_input("Kosten eines Verkehrssignals (CHF)", value=1500),
        'playground': st.sidebar.number_input("Kosten eines Spielplatzes (CHF)", value=5000),
        'sports_centre': st.sidebar.number_input("Kosten eines Sportzentrums (CHF)", value=30000),
        'viewpoint': st.sidebar.number_input("Kosten eines Aussichtspunktes (CHF)", value=1200),
        'museum': st.sidebar.number_input("Kosten eines Museums (CHF)", value=50000),
        'information': st.sidebar.number_input("Kosten einer Informationsstelle (CHF)", value=800)
    }

    # Store user inputs in session state
    st.session_state.costs = costs

with tab2:
    st.header("Daten hochladen & abrufen")

    # Option to choose between OSM data or manual upload
    data_source_option = st.radio(
        "Datenquelle für Infrastrukturstandorte auswählen:",
        ("Von OpenStreetMap abrufen", "Eigene Infrastrukturdaten hochladen"),
        help="Wählen Sie, ob Sie Daten von OpenStreetMap abrufen oder eigene Daten hochladen möchten."
    )
    st.session_state['data_source_option'] = data_source_option  # Store the data source option

    if data_source_option == "Von OpenStreetMap abrufen":
        # Option to fetch data from OpenStreetMap
        if st.button("Daten von OpenStreetMap abrufen"):
            tags = {
                'amenity': st.session_state.infra_types,
                'leisure': ['park', 'pitch', 'playground', 'sports_centre'],
                'tourism': ['information', 'viewpoint', 'museum'],
                'highway': ['crossing', 'bus_stop', 'traffic_signals']
            }
            try:
                st.session_state.infrastructure_gdf = ox.features_from_place(st.session_state.place_name, tags=tags)
                st.session_state.fetched_data = True  # Set flag indicating data has been fetched
                st.success(f"Daten erfolgreich aus {st.session_state.place_name} abgerufen!")
                st.write(st.session_state.infrastructure_gdf.head())  # Show a preview of fetched data
            except Exception as e:
                st.error(f"Fehler beim Abrufen der Daten von OpenStreetMap: {e}")
                st.session_state.fetched_data = False

    elif data_source_option == "Eigene Infrastrukturdaten hochladen":
        st.write("Laden Sie Ihre eigenen Infrastruktur CSV- oder GPKG-Dateien zur Analyse hoch.")

        # Uploading files for various infrastructure types
        uploaded_files = {
            "Laufstrecken": st.file_uploader("Laufstrecken-Datei hochladen", type=["csv", "gpkg"], key="laufstrecken"),
            "ÖV-Haltestellen": st.file_uploader("ÖV-Haltestellen-Datei hochladen", type=["csv", "gpkg"], key="ov_haltestellen"),
            "Parkanlagen": st.file_uploader("Parkanlagen-Datei hochladen", type=["csv", "gpkg"], key="parkanlagen"),
            "Richtplan Fussverkehr": st.file_uploader("Richtplan Fussverkehr-Datei hochladen", type=["csv", "gpkg"], key="richtplan_fussverkehr"),
            "Spielplaetze": st.file_uploader("Spielplätze-Datei hochladen", type=["csv", "gpkg"], key="spielplaetze"),
            "Sportanlagen": st.file_uploader("Sportanlagen-Datei hochladen", type=["csv", "gpkg"], key="sportanlagen"),
            "Velopumpenstandorte": st.file_uploader("Velopumpenstandorte-Datei hochladen", type=["csv", "gpkg"], key="velopumpenstandorte"),
            "Verkehrsmessstellen": st.file_uploader("Verkehrsmessstellen-Datei hochladen", type=["csv", "gpkg"], key="verkehrsmessstellen")
        }

        # Convert each uploaded file to GeoDataFrame and store in session state
        manual_data_loaded = False
        for key, file in uploaded_files.items():
            if file is not None:
                try:
                    if file.name.endswith(".csv"):
                        df = pd.read_csv(file)
                        if "Longitude" in df.columns and "Latitude" in df.columns:
                            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326")
                        else:
                            st.error(f"{key} CSV-Datei fehlt 'Longitude'- oder 'Latitude'-Spalten.")
                            continue
                    elif file.name.endswith(".gpkg"):
                        gdf = gpd.read_file(file)
                        if gdf.empty:
                            st.error(f"{key} GPKG-Datei ist leer.")
                            continue

                    # Convert to appropriate projection
                    gdf = gdf.to_crs(epsg=32632)
                    st.session_state[f"{key}_gdf"] = gdf
                    st.write(f"<span class='uploaded-file-name'>{key} Daten erfolgreich geladen.</span>", unsafe_allow_html=True)
                    st.write(gdf.head())
                    manual_data_loaded = True

                except Exception as e:
                    st.error(f"Fehler beim Laden der {key} Daten: {e}")

        # Set flag if manual data has been successfully loaded
        st.session_state.manual_data_loaded = manual_data_loaded

    # Placeholder for file uploads for other data
    population_file = st.file_uploader("CSV-Datei für Bevölkerungsdichte-Daten auswählen", type="csv", help="Laden Sie eine CSV-Datei mit Bevölkerungsdichte-Daten hoch.")
    busyness_file = st.file_uploader("CSV-Datei für Verkehrsdaten auswählen", type="csv", help="Laden Sie eine CSV-Datei mit Verkehrsdaten hoch.")
    air_quality_file = st.file_uploader("CSV-Datei für Luftqualitätsdaten auswählen", type="csv", help="Laden Sie eine CSV-Datei mit Luftqualitätsdaten hoch.")

    # Store uploaded files in session state
    if population_file:
        st.session_state.population_df = pd.read_csv(population_file)
        st.write("Bevölkerungsdaten erfolgreich geladen.")
        st.write(st.session_state.population_df.head())

    if busyness_file:
        st.session_state.busyness_df = pd.read_csv(busyness_file)
        st.write("Verkehrsdaten erfolgreich geladen.")
        st.write(st.session_state.busyness_df.head())

    if air_quality_file:
        st.session_state.air_quality_df = pd.read_csv(air_quality_file)
        st.write("Luftqualitätsdaten erfolgreich geladen.")
        st.write(st.session_state.air_quality_df.head())

with tab3:
    st.header("Analyse & Ergebnisse")

    # Run analysis button
    if st.button("Analyse starten"):
        # Use data stored in session state
        population_df = st.session_state.get('population_df', pd.DataFrame())
        busyness_df = st.session_state.get('busyness_df', pd.DataFrame())
        air_quality_df = st.session_state.get('air_quality_df', pd.DataFrame())

        # Determine if we are using OpenStreetMap or manual data
        data_source_option = st.session_state.get('data_source_option', None)

        if data_source_option == "Von OpenStreetMap abrufen":
            if 'infrastructure_gdf' not in st.session_state:
                st.error("Bitte rufen Sie die Infrastrukturdaten von OpenStreetMap ab, bevor Sie die Analyse durchführen.")
            else:
                infrastructure_gdf = st.session_state.infrastructure_gdf
                tags = {
                    'amenity': st.session_state.infra_types,
                    'leisure': ['park', 'pitch', 'playground', 'sports_centre'],
                    'tourism': ['information', 'viewpoint', 'museum'],
                    'highway': ['crossing', 'bus_stop', 'traffic_signals']
                }
        elif data_source_option == "Eigene Infrastrukturdaten hochladen":
            infrastructure_gdfs = []
            for key in [
                "Laufstrecken", "ÖV-Haltestellen", "Parkanlagen",
                "Richtplan Fussverkehr", "Spielplaetze", "Sportanlagen",
                "Velopumpenstandorte", "Verkehrsmessstellen"
            ]:
                gdf = st.session_state.get(f"{key}_gdf", None)
                if gdf is not None:
                    infrastructure_gdfs.append(gdf)

            if not infrastructure_gdfs:
                st.error("Bitte laden Sie mindestens eine Infrastrukturdatei hoch, bevor Sie die Analyse durchführen.")
            else:
                # Concatenate all manually uploaded infrastructure data into a single GeoDataFrame
                try:
                    infrastructure_gdf = pd.concat(infrastructure_gdfs).pipe(gpd.GeoDataFrame)
                    infrastructure_gdf = infrastructure_gdf.to_crs(epsg=32632)  # Ensure all data is in the same CRS
                except Exception as e:
                    st.error(f"Fehler beim Kombinieren der hochgeladenen Infrastrukturdaten: {e}")
                else:
                    tags = {
                        'amenity': st.session_state.infra_types
                    }
        else:
            st.error("Bitte wählen Sie eine Datenquelle aus (OpenStreetMap oder manuelles Hochladen).")
        
        # If infrastructure_gdf is defined, proceed with the analysis
        if 'infrastructure_gdf' in locals():
            # Run the analysis function
            try:
                results_df = analyze_infrastructure_with_apis(
                    st.session_state.place_name, 
                    st.session_state.density_threshold, 
                    st.session_state.proximity_threshold, 
                    tags, 
                    population_df, 
                    busyness_df, 
                    air_quality_df,
                    infrastructure_gdf
                )
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")
            else:
                # Save the results in session state
                if results_df is not None and not results_df.empty:
                    st.session_state.results_df = results_df
                    st.success("Analyse erfolgreich abgeschlossen!")

                    # Display results as table
                    st.write("Vorgeschlagene Infrastrukturlocations:")
                    st.dataframe(results_df)

                    # Calculate total cost
                    if 'costs' in st.session_state:
                        total_cost = sum(
                            len(results_df[results_df['Infrastrukturtyp'] == infra_type.capitalize()]) * cost
                            for infra_type, cost in st.session_state.costs.items()
                        )
                        st.write(f"Gesamtkosten (geschätzt): CHF {total_cost}")

                    # Plot the map with consistent size
                    fig = px.scatter_mapbox(
                        results_df,
                        lat="Vorgeschlagene Breite",
                        lon="Vorgeschlagene Länge",
                        hover_name="Infrastrukturtyp",
                        hover_data=["Bereich", "Bevölkerungsdichte"],
                        zoom=12,
                        height=600,
                        color="Infrastrukturtyp"
                    )
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0},
                        annotations=[
                            dict(
                                text="<b>Koordinaten</b>",
                                showarrow=False,
                                xref="paper",
                                yref="paper",
                                x=0,
                                y=1,
                                font=dict(size=16)
                            )
                        ]
                    )
                    fig.update_traces(marker=dict(size=12))  # Make markers larger for better visibility
                    st.plotly_chart(fig)
                else:
                    st.write("Keine Standorte zur Anzeige auf der Karte verfügbar.")

with tab4:
    st.header("Bericht & Feedback")

    # User feedback section
    st.markdown("<p class='feedback-label'>Geben Sie Feedback zu den vorgeschlagenen Standorten:</p>", unsafe_allow_html=True)
    user_feedback = st.text_area("Geben Sie Feedback zu den vorgeschlagenen Standorten:")

    if st.button("PDF-Bericht herunterladen"):
        if 'results_df' in st.session_state and not st.session_state.results_df.empty:
            generate_report(st.session_state.results_df, user_feedback)
            # Add branding elements to the report
            html_content = "<div style='text-align:center;'><img src='https://example.com/logo.png' alt='Logo' width='100'></div>"
            with open('C:/Users/moham/Desktop/Infrascout/report.pdf', "rb") as pdf_file:
                st.download_button(
                    label="Bericht als PDF herunterladen",
                    data=pdf_file,
                    file_name='infrastrukturbericht.pdf',
                    mime='application/pdf'
                )
        else:
            st.error("Bitte führen Sie die Analyse durch, bevor Sie den PDF-Bericht herunterladen.")
