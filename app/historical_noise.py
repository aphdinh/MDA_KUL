import pandas as pd
import streamlit as st
import seaborn as sns
import folium
from streamlit_folium import folium_static
from streamlit_extras.colored_header import colored_header
import plotly.express as px
import plotly.graph_objects as go
import re

# Define the coordinates for each location
locations = [
    "MP 01: Naamsestraat 35 Maxim",
    "MP 02: Naamsestraat 57 Xior",
    "MP 03: Naamsestraat 62 Taste",
    "MP 04: His & Hears",
    "MP 05: Calvariekapel KU Leuven",
    "MP 06: Parkstraat 2 La Filosovia",
    "MP 07: Naamsestraat 81",
]
location_coordinates = {
    "MP 01: Naamsestraat 35 Maxim": (50.87711, 4.70071),
    "MP 02: Naamsestraat 57 Xior": (50.87650, 4.70071),
    "MP 03: Naamsestraat 62 Taste": (50.87585, 4.70024),
    "MP 04: His & Hears": (50.87539, 4.70003),
    "MP 05: Calvariekapel KU Leuven": (50.87463, 4.69987),
    "MP 06: Parkstraat 2 La Filosovia": (50.87442, 4.70035),
    "MP 07: Naamsestraat 81": (50.87393, 4.70005),
}


@st.cache_data
def load_data(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        delimiter = re.search(r"[;,]", content).group()
    return pd.read_csv(file_path, sep=delimiter)


def historical_noise_content():
    st.title("✨ Historical Noise Exploration")

    tab1, tab2 = st.tabs(["📊 Overview", "📍 By Location"])

    with tab2:
        st.write(
            """Which specific location would you like to know more about? \
            And could you please specify the temporal pattern you're interested in exploring,\
                whether it's based on the hour of the day or the day of the week?"""
        )

        selected_location = st.selectbox("Select Location", list(locations))
        # Group by option
        group_by_option = st.selectbox(
            "Group By", ["By Hour", "By Day", "By Month", "By Date"]
        )

        # Header 1: Noise percentile
        colored_header(
            label="Noise Level Percentiles",
            description="Explore the temporal pattern of noise level percentile in the selected location",
            color_name="red-70",
        )

        # file40
        dataframes_file40 = {
            "MP 01: Naamsestraat 35 Maxim": "../data/file40/csv_results_40_255439_mp-01-naamsestraat-35-maxim.csv",
            "MP 02: Naamsestraat 57 Xior": "../data/file40/csv_results_40_255440_mp-02-naamsestraat-57-xior.csv",
            "MP 03: Naamsestraat 62 Taste": "../data/file40/csv_results_40_255441_mp-03-naamsestraat-62-taste.csv",
            "MP 04: His & Hears": "../data/file40/csv_results_40_303910_mp-04-his-hears.csv",
            "MP 05: Calvariekapel KU Leuven": "../data/file40/csv_results_40_255442_mp-05-calvariekapel-ku-leuven.csv",
            "MP 06: Parkstraat 2 La Filosovia": "../data/file40/csv_results_40_255443_mp-06-parkstraat-2-la-filosovia.csv",
            "MP 07: Naamsestraat 81": "../data/file40/csv_results_40_255444_mp-07-naamsestraat-81.csv",
            "MP 08: Vrijthof": "../data/file40/csv_results_40_280324_mp08bis---vrijthof.csv",
        }

        df_path_file40 = dataframes_file40[selected_location]
        selected_data_40 = load_data(df_path_file40)
        selected_data_40["result_timestamp"] = pd.to_datetime(
            selected_data_40["result_timestamp"]
        )

        # Create additional columns
        selected_data_40["weekday"] = selected_data_40["result_timestamp"].dt.strftime(
            "%A"
        )
        selected_data_40["date"] = selected_data_40["result_timestamp"].dt.date
        selected_data_40["month"] = selected_data_40["result_timestamp"].dt.month
        selected_data_40["hour"] = selected_data_40["result_timestamp"].dt.hour

        # List of y-value columns to plot
        laf_columns = [
            "laf005_per_hour",
            "laf01_per_hour",
            "laf05_per_hour",
            "laf10_per_hour",
            "laf25_per_hour",
            "laf50_per_hour",
            "laf75_per_hour",
            "laf90_per_hour",
            "laf95_per_hour",
            "laf98_per_hour",
            "laf99_per_hour",
            "laf995_per_hour",
        ]
        laf_cols = [col for col in selected_data_40.columns if col.startswith("laf")]

        def groupby_and_mean_40(data, column):
            return data.groupby(column)[laf_cols].mean().reset_index()

        # Multi-select box for variables
        selected_laf_column = st.multiselect(
            "Select variables", laf_columns, default=laf_columns
        )

        # Variable definition
        with st.expander("Definition of noise level measurements 👉"):
            st.write(
                " The LAf sound level is a specific type of sound level measurement that\
                    represents the A-weighted sound level with a fast time weighting. \
                    The fast time weighting captures the instantaneous sound level at a particular moment."
            )
            st.write(
                "The numbers following `laf` in the variable names represent different percentiles. \
                Percentiles indicate the percentage of values that fall below a certain threshold."
            )

            st.write(
                "For example, `laf50_per_hour` represents the 50th percentile of the LAf sound level per hour,\
                    which is also known as the median. \
                It indicates the value below which 50% of the LAf sound level values per hour are expected to fall."
            )

            st.write(
                "These percentiles provide information about the distribution and variability of \
                the LAf sound level measurements over a specific time period, typically per hour. \
                They can be used to analyze and understand the characteristics of sound exposure\
                    in different scenarios or locations."
            )

        # Group the data based on the selected option
        if group_by_option == "By Hour":
            sorted_data = groupby_and_mean_40(selected_data_40, "hour")
            x_column = "hour"
            x_label = "Hour"
        elif group_by_option == "By Day":
            weekday_order = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            selected_data_40["weekday"] = pd.Categorical(
                selected_data_40["weekday"], categories=weekday_order, ordered=True
            )
            sorted_data = groupby_and_mean_40(selected_data_40, "weekday")
            x_column = "weekday"
            x_label = "Weekday"
        elif group_by_option == "By Month":
            sorted_data = groupby_and_mean_40(selected_data_40, "month")
            x_column = "month"
            x_label = "Month"
        elif group_by_option == "By Date":
            sorted_data = groupby_and_mean_40(selected_data_40, "date")
            x_column = "date"
            x_label = "Date"

        # Plot the line graph
        fig = px.line(
            sorted_data, x=x_column, y=selected_laf_column, line_shape="linear"
        )
        fig.update_layout(
            title=selected_location + " - Lineplot of average noise level percentiles",
            xaxis_title=x_label,
            yaxis_title="Value (dBA)",
            legend_title="Measure",
        )
        st.plotly_chart(fig)

        # Create the box plot
        fig = px.box(sorted_data, x=x_column, y=selected_laf_column)
        fig.update_layout(
            title=selected_location + " - Boxplot of average noise level percentiles",
            xaxis_title=x_label,
            yaxis_title="Value (dBA)",
        )
        st.plotly_chart(fig)

        # Header 2: Noise Level
        colored_header(
            label="Noise Level",
            description="Explore the temporal pattern of noise level in the selected location",
            color_name="red-70",
        )

        file42 = load_data("../data/processed_file42_data.csv")
        loc_dict = {
            "MP 01: Naamsestraat 35 Maxim": 0,
            "MP 02: Naamsestraat 57 Xior": 1,
            "MP 03: Naamsestraat 62 Taste": 2,
            "MP 04: His & Hears": 3,
            "MP 05: Calvariekapel KU Leuven": 4,
            "MP 06: Parkstraat 2 La Filosovia": 5,
            "MP 07: Naamsestraat 81": 6,
        }
        index = loc_dict[selected_location]
        selected_data_42 = file42[
            file42["location"] == list(file42.location.unique())[index]
        ]
        selected_data_42["result_timestamp"] = pd.to_datetime(
            selected_data_42["result_timestamp"], format="%Y-%m-%d %H:%M:%S"
        )
        selected_data_42["date"] = selected_data_42["result_timestamp"].dt.date
        # selected_data_42.dropna(subset=['lamax'], inplace=True)
        selected_data_42 = selected_data_42[
            [
                "result_timestamp",
                "lamax",
                "laeq",
                "lceq",
                "lcpeak",
                "hour",
                "weekday",
                "month",
                "date",
            ]
        ]

        # List of y-value columns to plot
        l_cols = ["lamax", "laeq", "lceq", "lcpeak"]

        def groupby_and_mean(data, column):
            return data.groupby(column)[l_cols].mean().reset_index()

        # Multi-select box for variables
        selected_l_column = st.multiselect("Select variables", l_cols, default=l_cols)

        # Variable definition
        with st.expander("Definition of noise level measurements 👉"):
            st.write("- `LA`: A-weighted, sound level - dB(A)")
            st.write(
                "- `LAmax`: A-weighted, maximum sound level - maximum is not peak - dB(A)"
            )
            st.write("- `LAeq`: A-weighted, equivalent continuous sound level - dB(C)")
            st.write(
                "- `LCeq`: C-weighted, Leq (equivalent continuous sound level) - dB(C)"
            )
            st.write("- `LCpeak`: C-weighted, peak sound level - dB(C)")

        # Group the data based on the selected option
        if group_by_option == "By Hour":
            x_column = "hour"
            sorted_data_42 = groupby_and_mean(selected_data_42, x_column)
            x_label = "Hour"
        elif group_by_option == "By Day":
            x_column = "weekday"
            weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            selected_data_42["weekday"] = pd.Categorical(
                selected_data_42["weekday"], categories=weekday_order, ordered=True
            )
            sorted_data_42 = groupby_and_mean(selected_data_42, x_column)
            x_label = "Weekday"
        elif group_by_option == "By Month":
            x_column = "month"
            sorted_data_42 = groupby_and_mean(selected_data_42, x_column)
            x_label = "Month"
        elif group_by_option == "By Date":
            x_column = "date"
            sorted_data_42 = groupby_and_mean(selected_data_42, x_column)
            x_label = "Date"

        # Plot the line graph
        fig42 = px.line(
            sorted_data_42, x=x_column, y=selected_l_column, line_shape="linear"
        )
        fig42.update_layout(
            title=selected_location + " - Lineplot of average noise level",
            xaxis_title=x_label,
            yaxis_title="Value",
            legend_title="Measure",
        )
        st.plotly_chart(fig42)

        # Boxplot
        selected_y_boxplot = st.selectbox("Select a variable for boxplot", l_cols)
        # Create the box plot
        file42_dropna = file42.dropna(subset=[selected_y_boxplot])
        bp42 = px.box(file42, x=x_column, y=selected_y_boxplot)
        bp42.update_layout(
            title="Mean " + selected_y_boxplot.title() + " by " + x_column.title(),
            xaxis_title=x_label,
            yaxis_title="Value",
        )
        st.plotly_chart(bp42)

        # Header 3: Noise Event
        colored_header(
            label="Noise Event",
            description="Explore the temporal pattern of noise event in the selected location",
            color_name="red-70",
        )

        dataframes_file41 = {
            "MP 01: Naamsestraat 35 Maxim": "../data/file41/csv_results_41_255439_mp-01-naamsestraat-35-maxim.csv",
            "MP 02: Naamsestraat 57 Xior": "../data/file41/csv_results_41_255440_mp-02-naamsestraat-57-xior.csv",
            "MP 03: Naamsestraat 62 Taste": "../data/file41/csv_results_41_255441_mp-03-naamsestraat-62-taste.csv",
            "MP 04: His & Hears": "../data/file41/csv_results_41_303910_mp-04-his-hears.csv",
            "MP 05: Calvariekapel KU Leuven": "../data/file41/csv_results_41_255442_mp-05-calvariekapel-ku-leuven.csv",
            "MP 06: Parkstraat 2 La Filosovia": "../data/file41/csv_results_41_255443_mp-06-parkstraat-2-la-filosovia.csv",
            "MP 07: Naamsestraat 81": "../data/file41/csv_results_41_255444_mp-07-naamsestraat-81.csv",
            "MP 08: Vrijthof": "../data/file41/csv_results_41_280324_mp08bis---vrijthof.csv",
        }

        df_path_file41 = dataframes_file41[selected_location]
        df_file41 = load_data(df_path_file41)
        df_file41 = df_file41[
            ["result_timestamp", "noise_event_laeq_primary_detected_class"]
        ]
        df_file41["result_timestamp"] = pd.to_datetime(df_file41["result_timestamp"])
        df_file41["hour"] = df_file41["result_timestamp"].dt.hour
        df_file41["weekday"] = df_file41["result_timestamp"].dt.strftime("%a")

        # Aggregate the data
        aggregated_file41 = (
            df_file41.groupby(
                ["hour", "weekday", "noise_event_laeq_primary_detected_class"]
            )
            .size()
            .reset_index(name="count")
        )
        weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        aggregated_file41["weekday"] = pd.Categorical(
            aggregated_file41["weekday"], categories=weekday_order, ordered=True
        )
        noise_types = list(
            aggregated_file41.noise_event_laeq_primary_detected_class.unique()
        )
        # Select box for noise type
        selected_noise_type = st.selectbox(
            "Select Noise Type", list(noise_types), index=2
        )
        # Filter the data for the selected noise only
        selected_aggregated_file41 = aggregated_file41[
            aggregated_file41["noise_event_laeq_primary_detected_class"]
            == selected_noise_type
        ].drop(["noise_event_laeq_primary_detected_class"], axis=1)
        heatmap_data = selected_aggregated_file41.pivot_table(
            index="hour", columns="weekday", values="count", fill_value=0
        )
        # Heatmap
        heatmap = px.imshow(heatmap_data, color_continuous_scale="YlGnBu")
        heatmap.update_layout(
            title=f"Frequency of {selected_noise_type} at {selected_location}",
            xaxis_title="Weekday",
            yaxis_title="Hour",
            xaxis=dict(tickmode="linear"),
            yaxis=dict(tickmode="linear"),
        )
        st.plotly_chart(heatmap)

        # Header 4: Map
        colored_header(
            label="Location on the map",
            description="The spatial distribution of noise sensors on Naamsestraat",
            color_name="red-70",
        )

        st.write("You are at", selected_location)
        selected_coordinates = location_coordinates[selected_location]
        map_center = (50.8798, 4.7005)  # Center of Leuven
        map_zoom = 15
        m = folium.Map(location=map_center, zoom_start=map_zoom)

        # Add markers for each location
        for location, coordinates in location_coordinates.items():
            marker_color = "red" if location == selected_location else "blue"
            folium.Marker(
                location=coordinates,
                popup=location,
                icon=folium.Icon(color=marker_color, icon="info-sign"),
            ).add_to(m)

        # Add circle markers for selected location
        folium.CircleMarker(
            location=selected_coordinates,
            radius=10,
            color="#3186cc",
            fill=True,
            fill_color="#3186cc",
        ).add_to(m)

        # Display the map
        folium_static(m)

    with tab1:
        st.write(
            "Which temporal pattern would you like to explore further? \
                Would you prefer to analyze data by hour, weekday, or date?"
        )
        group_options = {
            "Date": ["date", "Frequency of Noise Event by Date"],
            "Hour": ["hour", "Frequency of Noise Event by Hour"],
            "Weekday": ["weekday", "Frequency of Noise Event by Weekday"],
        }

        group_by = st.selectbox("Group By", list(group_options.keys()), index=1)

        # Header 1: Noise event
        colored_header(
            label="Noise Event",
            description="Explore the temporal pattern of noise event in all locations",
            color_name="red-70",
        )
        file41 = load_data("../data/file41.csv")
        file41.result_timestamp = pd.to_datetime(file41.result_timestamp)
        file41.date = pd.to_datetime(file41.date)
        weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        file41["weekday"] = pd.Categorical(
            file41["weekday"], categories=weekday_order, ordered=True
        )

        # Noise event
        group_data = (
            file41.groupby([group_options[group_by][0], "noise_event"])[
                "noise_event_certainty"
            ]
            .count()
            .reset_index(name="count")
        )

        # Lineplot
        fig = px.line(
            group_data,
            x=group_options[group_by][0],
            y="count",
            color="noise_event",
            labels={
                group_options[group_by][0]: group_by,
                "count": "Frequency",
                "noise_event": "Noise Event",
            },
            title=group_options[group_by][1],
        )

        if group_by == "Date":
            fig.update_layout(
                xaxis=dict(tickformat="%b", dtick="M1", ticklabelmode="period")
            )

        st.plotly_chart(fig)

        st.markdown(
            """
        🔍 **Noise event Insights:**
        - May and March are the busiest months in terms of noise events.
        - Leuven tends to be quieter during the weekends, which is not surprising!\
            Watch out for Thursday tho, when noise events hit their peak in Leuven.
        - The most common noise event is related to transportation, particularly car sounds.\
            Interestingly, car sounds are most prevalent in the morning between 8-10 AM when people are starting their day.\
                Surprisingly, during the evening rush hour between 4-6 PM, car sounds seem to be less frequent.
        """
        )

        # Barplot
        grouped = (
            file41.groupby(["location", "noise_event"]).size().reset_index(name="count")
        )
        fig = px.bar(
            grouped,
            x="noise_event",
            y="count",
            color="location",
            title="Frequency by Location and Noise Type",
            labels={"noise_event": "Noise Type", "count": "Frequency"},
            height=500,
            width=700,
        )
        fig.update_layout(xaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig)

        # comment on barplot
        text = """
        - `Transport road - Car sound` is the most common type by far, followed by `Unsupported` noise.
        - And guess who steals the spotlight as the busiest noise hub? It's none other than `MP01` and `MP07`, \
            where all the noise action happens, while `MP02` appears to be the quietest!
        """

        st.write(text)

        # Heatmap
        file41.result_timestamp = pd.to_datetime(file41.result_timestamp)
        file41.date = pd.to_datetime(file41.date)
        aggregated_file41 = (
            file41.groupby(["hour", "weekday", "date", "noise_event", "location"])
            .size()
            .reset_index(name="count")
        )
        weekday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        aggregated_file41["weekday"] = pd.Categorical(
            aggregated_file41["weekday"], categories=weekday_order, ordered=True
        )
        heatmap_data = aggregated_file41.pivot_table(
            index="location", columns=group_by.lower(), values="count", fill_value=0
        )
        fig = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            labels=dict(x=group_by, y="Location", color="Frequency"),
            color_continuous_scale="YlOrRd",
        )
        fig.update_layout(title=f"Frequency by Location and {group_by}")
        st.plotly_chart(fig)

        # comment on heatmap
        st.markdown("##### By Hour")
        hour_text = """
        - There is a clear temporal pattern observed in `MP01`, `MP07`, and `MP08`, with noise events predominantly occurring between 7 AM and 4 PM. \
            This stark contrast in noise frequency during that period compared to others is the most evident in  `MP07`.
        - These findings highlight the influence of transportation and the variations in noise levels across different locations and time frames.
        """
        st.write(hour_text)

        st.markdown("##### By Weekday")
        weekday_text = """
        - While we observe a clear pattern in `MP01` and `MP07`, with most of the noise events happening from Monday to Friday,\
            it is not consistent in other locations.
        - Interestingly, `MP08` seems to have its own unique style. It prefers to make more noise on Saturdays, followed by Sundays \
            and its pattern of noise during the weekdays is also quite erratic.
        """
        st.write(weekday_text)

        # Header 2: Noise level
        colored_header(
            label="Noise Level",
            description="Explore the temporal pattern of noise level in all locations",
            color_name="red-70",
        )

        def create_violin_plot(df, groupby_col, measure, title):

            df[measure] = df[measure].astype(float)
            # color palette
            num_unique_values = df[groupby_col].nunique()
            colors = sns.color_palette("husl", num_unique_values)

            # Create a list of traces for each unique value in the groupby column
            traces = []
            for i, val in enumerate(df[groupby_col].unique()):
                # Convert color to rgb format
                color = "rgb" + str(tuple(int(c * 255) for c in colors[i]))
                traces.append(
                    go.Violin(
                        x=df[measure][df[groupby_col] == val],
                        line_color=color,
                        name=str(val),
                    )
                )

            layout = go.Layout(
                title=title,
                xaxis_title=measure,
                yaxis_title=groupby_col.capitalize(),
                violingap=0,
                violingroupgap=0,
                violinmode="overlay",
            )

            fig = go.Figure(data=traces, layout=layout)
            st.plotly_chart(fig)

        # clean data
        file42["hour"] = file42["hour"].astype(int)
        file42["month"] = file42["month"].astype(int)
        file42["weekday"] = pd.Categorical(
            file42["weekday"],
            categories=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            ordered=True,
        )

        # select box
        l_cols = ["lamax", "laeq", "lceq", "lcpeak"]
        selected_x_violin = st.selectbox("Select a measurement for violin plot", l_cols)
        # expander
        with st.expander("Definition of noise level measurements 👉", expanded=True):
            st.write("- `LA`: A-weighted, sound level - dB(A)")
            st.write(
                "- `LAmax`: A-weighted, maximum sound level - maximum is not peak - dB(A)"
            )
            st.write("- `LAeq`: A-weighted, equivalent continuous sound level - dB(C)")
            st.write(
                "- `LCeq`: C-weighted, Leq (equivalent continuous sound level) - dB(C)"
            )
            st.write("- `LCpeak`: C-weighted, peak sound level - dB(C)")

        # first violin plot
        if group_by == "Date":
            group_by_col = "month"
        else:
            group_by_col = group_by.lower()
        title = f"Distribution of {selected_x_violin.title()} by {group_by_col.title()}"
        create_violin_plot(file42, group_by_col, selected_x_violin, title)
        # comment
        text = """
         🔍 **Noise level Insights:**
        - Noise level has a predictable routine, just like your morning coffee.
        - Leuven takes a break from noise during the summer (July and August), as if the city is on vacation. 
        - Friday and Thursday compete for being the noisiest days, while Saturday and Sunday enjoy a peaceful snooze.
        """
        st.write(text)

        # second violin plot
        title_location = f"Distribution of {selected_x_violin.title()} by location"
        create_violin_plot(file42, "location", selected_x_violin, title_location)
        text = """
        - While `MP08` records more noise events than some other locations, \
            it surprisingly stands out as the quietest in terms of noise levels.
        - `MP01` takes the lead with the highest median noise level, followed closely by `MP06`.
        """
        st.write(text)
