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
    st.success("Application Configured Successfully!")
except Exception as e:
    st.error(f"Error configuring pdfkit: {e}")

# Custom CSS for styling Streamlit dashboard
def add_custom_css():
    custom_css = """
    <style>
        .stApp {
            background-image: url('https://example.com/background.jpg');
            background-size: cover;
            background-attachment: fixed;
            color: #000000;
        }
        .main-content {
            padding: 2rem;
            border-radius: 8px;
        }
        .stButton > button {
            background-color: #4A90E2;
            color: #ffffff;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #357ABD;
            transform: scale(1.05);
        }
        .stTabs [role="tab"] {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            color: #000000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stTextInput > div > input {
            border-radius: 10px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-weight: bold;
            background-color: rgba5, 255, 255, 0.95);
            color: #000000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stSidebar {
            background-color:  #000000;
            border-right: 2px solid #e0e0e0;
            padding: 20px;
        }
        .coordinate-label {
            font-size: 18px;
            font-weight: bold;
            color: #000000;
        }
        .stMarkdown h1 {
            color: #000000;
            font-size: 3em;
        }
        .stMarkdown h2 {
            color: #000000;
        }
        .stMarkdown p {
            color: #000000;
        }
        .uploaded-file-name {
            color: #000000;
            font-weight: bold;
        }
        .stRadio > label, .stRadio > div > label {
            color: #000000;
        }
        .stSlider > label {
            color: #000000;
        }
        .stMultiselect > label {
            color: #000000;
        }
        .feedback-label {
            font-weight: bold;
            font-size: 1.2em;
            color: #4A90E2;
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
                        <span style="font-size: 1.2em;">1. Set Parameters</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em;">2. Upload Data</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em;">3. View Analysis</span>
                    </div>
                    <div style="flex: 1; text-align: center; padding: 10px;">
                        <span style="font-size: 1.2em;">4. Generate Report</span>
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
            <title>Infrastructure Report</title>
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
            <h1>Infrastructure Report</h1>
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
        st.success(f"PDF report generated successfully at {output_pdf_path}!")
    except Exception as e:
        st.error(f"Error generating PDF: {e}. Please ensure that local file URLs are enabled for wkhtmltopdf.")

# Analysis function for infrastructure
def analyze_infrastructure_with_apis(
    place_name, density_threshold, proximity_threshold, tags, population_df, busyness_df, air_quality_df, infrastructure_gdf
):
    if population_df.empty:
        st.error("Population DataFrame is empty.")
        return None

    # Convert to GeoDataFrame
    try:
        population_gdf = gpd.GeoDataFrame(
            population_df,
            geometry=gpd.points_from_xy(population_df.Longitude, population_df.Latitude),
            crs="EPSG:4326"
        )
    except Exception as e:
        st.error(f"Error converting to GeoDataFrame: {e}")
        return None

    # Reproject population data
    try:
        population_gdf = population_gdf.to_crs(epsg=32632)
    except Exception as e:
        st.error(f"Error reprojecting population data: {e}")
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
                            'Infrastructure Type': infra_type.capitalize(),
                            'Suggested Latitude': latitude,
                            'Suggested Longitude': longitude,
                            'Area': area['Area'],
                            'Population Density': area['Population Density']
                        })
                except Exception as e:
                    st.error(f"Error processing {infra_type}: {e}")

    if suggested_locations:
        st.success(f"Total suggested locations: {len(suggested_locations)}")
    else:
        st.warning("No suggested locations were generated.")

    return pd.DataFrame(suggested_locations)

# Removed clustering as it is not supported in Plotly Mapbox. Using offset to differentiate points.

# Streamlit app layout with sections/tabs
st.title("Infrascout Dashboard")
st.subheader("An advanced tool to analyze and improve city infrastructure")

# Add custom CSS and JavaScript
add_custom_css()
add_custom_js()

# Adding a loading spinner
st.markdown("""
<div class="loading-spinner">
    <img src="https://example.com/spinner.gif" alt="Loading...">
</div>
""", unsafe_allow_html=True)

# Creating tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Set Parameters", "Upload Data", "View Analysis", "Generate Report"])

with tab1:
    st.header("Input Parameters")
    
    # Define 'place_name' in the session state if it doesn't exist
    if 'place_name' not in st.session_state:
        st.session_state.place_name = "Bern, Switzerland"

    # User input for parameters
    place_name = st.text_input("City Name", st.session_state.place_name, help="Enter the name of the city you want to analyze.")

    # Update session state if the city name changes
    if st.session_state.place_name != place_name:
        st.session_state.place_name = place_name
        # Clear previously fetched data if city changes
        if "infrastructure_gdf" in st.session_state:
            del st.session_state.infrastructure_gdf
            st.write(f"City changed to {place_name}. Previous infrastructure data cleared.")

    density_threshold = st.slider("Population Density Threshold", 0, 2000, 1000, help="Set the population density threshold to identify areas that need more infrastructure.")
    proximity_threshold = st.slider("Proximity Threshold (meters)", 0, 2000, 1000, help="Set the proximity threshold to determine how close existing infrastructure needs to be to consider an area covered.")

    # Select infrastructure types
    infra_types = st.multiselect(
        "Select infrastructure types to analyze:",
        [
            'bench', 'toilets', 'waste_basket', 'bicycle_parking', 'drinking_water', 
            'charging_station', 'bus_stop', 'park', 'public_building', 'crossing', 
            'traffic_signals', 'playground', 'sports_centre', 'viewpoint', 'museum', 'information'
        ],
        default=['bench', 'toilets', 'waste_basket', 'bicycle_parking', 'drinking_water'],
        help="Select the types of infrastructure you want to analyze."
    )

    # Store user inputs in session state
    st.session_state.density_threshold = density_threshold
    st.session_state.proximity_threshold = proximity_threshold
    st.session_state.infra_types = infra_types

    # Sidebar for cost estimation
    st.header("")
    costs = {
        'bench': st.sidebar.number_input("Cost of a Bench (CHF)", value=200),
        'toilets': st.sidebar.number_input("Cost of a Toilet (CHF)", value=1000),
        'waste_basket': st.sidebar.number_input("Cost of a Trash Bin (CHF)", value=150),
        'bicycle_parking': st.sidebar.number_input("Cost of Bicycle Parking (CHF)", value=500),
        'drinking_water': st.sidebar.number_input("Cost of a Drinking Water Fountain (CHF)", value=800),
        'charging_station': st.sidebar.number_input("Cost of a Charging Station (CHF)", value=2000),
        'bus_stop': st.sidebar.number_input("Cost of a Bus Stop (CHF)", value=5000),
        'park': st.sidebar.number_input("Cost of a Park (CHF)", value=10000),
        'public_building': st.sidebar.number_input("Cost of a Public Building (CHF)", value=20000),
        'crossing': st.sidebar.number_input("Cost of a Crossing (CHF)", value=300),
        'traffic_signals': st.sidebar.number_input("Cost of Traffic Signals (CHF)", value=1500),
        'playground': st.sidebar.number_input("Cost of a Playground (CHF)", value=5000),
        'sports_centre': st.sidebar.number_input("Cost of a Sports Centre (CHF)", value=30000),
        'viewpoint': st.sidebar.number_input("Cost of a Viewpoint (CHF)", value=1200),
        'museum': st.sidebar.number_input("Cost of a Museum (CHF)", value=50000),
        'information': st.sidebar.number_input("Cost of an Information Point (CHF)", value=800)
    }

    # Store user inputs in session state
    st.session_state.costs = costs

with tab2:
    st.header("Data Upload & Fetching")

    # Option to choose between OSM data or manual upload
    data_source_option = st.radio(
        "Choose Data Source for Infrastructure Locations:",
        ("Fetch from OpenStreetMap", "Upload Custom Infrastructure Data"),
        help="Choose whether to fetch data from OpenStreetMap or upload your custom data."
    )
    st.session_state['data_source_option'] = data_source_option  # Store the data source option

    if data_source_option == "Fetch from OpenStreetMap":
        # Option to fetch data from OpenStreetMap
        if st.button("Fetch Data from OpenStreetMap"):
            tags = {
                'amenity': st.session_state.infra_types,
                'leisure': ['park', 'pitch', 'playground', 'sports_centre'],
                'tourism': ['information', 'viewpoint', 'museum'],
                'highway': ['crossing', 'bus_stop', 'traffic_signals']
            }
            try:
                st.session_state.infrastructure_gdf = ox.features_from_place(st.session_state.place_name, tags=tags)
                st.session_state.fetched_data = True  # Set flag indicating data has been fetched
                st.success(f"Successfully fetched data from {st.session_state.place_name}!")
                st.write(st.session_state.infrastructure_gdf.head())  # Show a preview of fetched data
            except Exception as e:
                st.error(f"Error fetching data from OpenStreetMap: {e}")
                st.session_state.fetched_data = False

    elif data_source_option == "Upload Custom Infrastructure Data":
        st.write("Upload your custom infrastructure CSV or GPKG files for analysis.")

        # Uploading files for various infrastructure types
        uploaded_files = {
            "Laufstrecken": st.file_uploader("Upload Laufstrecken file", type=["csv", "gpkg"], key="laufstrecken"),
            "ÖV-Haltestellen": st.file_uploader("Upload ÖV-Haltestellen file", type=["csv", "gpkg"], key="ov_haltestellen"),
            "Parkanlagen": st.file_uploader("Upload Parkanlagen file", type=["csv", "gpkg"], key="parkanlagen"),
            "Richtplan Fussverkehr": st.file_uploader("Upload Richtplan Fussverkehr file", type=["csv", "gpkg"], key="richtplan_fussverkehr"),
            "Spielplaetze": st.file_uploader("Upload Spielplaetze file", type=["csv", "gpkg"], key="spielplaetze"),
            "Sportanlagen": st.file_uploader("Upload Sportanlagen file", type=["csv", "gpkg"], key="sportanlagen"),
            "Velopumpenstandorte": st.file_uploader("Upload Velopumpenstandorte file", type=["csv", "gpkg"], key="velopumpenstandorte"),
            "Verkehrsmessstellen": st.file_uploader("Upload Verkehrsmessstellen file", type=["csv", "gpkg"], key="verkehrsmessstellen")
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
                            st.error(f"{key} CSV file is missing 'Longitude' or 'Latitude' columns.")
                            continue
                    elif file.name.endswith(".gpkg"):
                        gdf = gpd.read_file(file)
                        if gdf.empty:
                            st.error(f"{key} GPKG file is empty.")
                            continue

                    # Convert to appropriate projection
                    gdf = gdf.to_crs(epsg=32632)
                    st.session_state[f"{key}_gdf"] = gdf
                    st.write(f"<span class='uploaded-file-name'>{key} data loaded successfully.</span>", unsafe_allow_html=True)
                    st.write(gdf.head())
                    manual_data_loaded = True

                except Exception as e:
                    st.error(f"Error loading {key} data: {e}")

        # Set flag if manual data has been successfully loaded
        st.session_state.manual_data_loaded = manual_data_loaded

    # Placeholder for file uploads for other data
    population_file = st.file_uploader("Choose a CSV file for population density data", type="csv", help="Upload a CSV file containing population density data.")
    busyness_file = st.file_uploader("Choose a CSV file for busyness data", type="csv", help="Upload a CSV file containing busyness data.")
    air_quality_file = st.file_uploader("Choose a CSV file for air quality data", type="csv", help="Upload a CSV file containing air quality data.")

    # Store uploaded files in session state
    if population_file:
        st.session_state.population_df = pd.read_csv(population_file)
        st.write("Population data loaded successfully.")
        st.write(st.session_state.population_df.head())

    if busyness_file:
        st.session_state.busyness_df = pd.read_csv(busyness_file)
        st.write("Busyness data loaded successfully.")
        st.write(st.session_state.busyness_df.head())

    if air_quality_file:
        st.session_state.air_quality_df = pd.read_csv(air_quality_file)
        st.write("Air quality data loaded successfully.")
        st.write(st.session_state.air_quality_df.head())

with tab3:
    st.header("Analysis & Results")

    # Run analysis button
    if st.button("Run Analysis"):
        # Use data stored in session state
        population_df = st.session_state.get('population_df', pd.DataFrame())
        busyness_df = st.session_state.get('busyness_df', pd.DataFrame())
        air_quality_df = st.session_state.get('air_quality_df', pd.DataFrame())

        # Determine if we are using OpenStreetMap or manual data
        data_source_option = st.session_state.get('data_source_option', None)

        if data_source_option == "Fetch from OpenStreetMap":
            if 'infrastructure_gdf' not in st.session_state:
                st.error("Please fetch infrastructure data from OpenStreetMap before running the analysis.")
            else:
                infrastructure_gdf = st.session_state.infrastructure_gdf
                tags = {
                    'amenity': st.session_state.infra_types,
                    'leisure': ['park', 'pitch', 'playground', 'sports_centre'],
                    'tourism': ['information', 'viewpoint', 'museum'],
                    'highway': ['crossing', 'bus_stop', 'traffic_signals']
                }
        elif data_source_option == "Upload Custom Infrastructure Data":
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
                st.error("Please upload at least one infrastructure file before running the analysis.")
            else:
                # Concatenate all manually uploaded infrastructure data into a single GeoDataFrame
                try:
                    infrastructure_gdf = pd.concat(infrastructure_gdfs).pipe(gpd.GeoDataFrame)
                    infrastructure_gdf = infrastructure_gdf.to_crs(epsg=32632)  # Ensure all data is in the same CRS
                except Exception as e:
                    st.error(f"Error combining uploaded infrastructure data: {e}")
                else:
                    tags = {
                        'amenity': st.session_state.infra_types
                    }
        else:
            st.error("Please select a data source option (OpenStreetMap or manual upload).")
        
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
                st.error(f"Error during analysis: {e}")
            else:
                # Save the results in session state
                if results_df is not None and not results_df.empty:
                    st.session_state.results_df = results_df
                    st.success("Analysis completed successfully!")

                    # Display results
                    st.write("Suggested Infrastructure Locations:")
                    st.dataframe(results_df)

                    # Calculate total cost
                    if 'costs' in st.session_state:
                        total_cost = sum(
                            len(results_df[results_df['Infrastructure Type'] == infra_type.capitalize()]) * cost
                            for infra_type, cost in st.session_state.costs.items()
                        )
                        st.write(f"Total Estimated Cost: CHF {total_cost}")

                    # Plot the map with consistent size
                    fig = px.scatter_mapbox(
                        results_df,
                        lat="Suggested Latitude",
                        lon="Suggested Longitude",
                        hover_name="Infrastructure Type",
                        hover_data=["Area", "Population Density"],
                        zoom=12,
                        height=600,
                        color="Infrastructure Type"
                    )
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":0,"l":0,"b":0},
                        annotations=[
                            dict(
                                text="<b>Coordinates</b>",
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
                    st.write("No locations available to display on the map.")

with tab4:
    st.header("Report & Feedback")

    # User feedback section
    st.markdown("<p class='feedback-label'>Provide feedback on the suggested locations:</p>", unsafe_allow_html=True)
    user_feedback = st.text_area("Provide feedback on the suggested locations:")

    if st.button("Download PDF Report"):
        if 'results_df' in st.session_state and not st.session_state.results_df.empty:
            generate_report(st.session_state.results_df, user_feedback)
            # Add branding elements to the report
            html_content = "<div style='text-align:center;'><img src='https://example.com/logo.png' alt='Logo' width='100'></div>"
            with open('C:/Users/moham/Desktop/Infrascout/report.pdf', "rb") as pdf_file:
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_file,
                    file_name='infrastructure_report.pdf',
                    mime='application/pdf'
                )
        else:
            st.error("Please run the analysis before downloading the PDF report.")
