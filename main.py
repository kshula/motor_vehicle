import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Load the data
st.title("Motor Vehicle Tax Policy Analysis")

# File path
data_file_path = os.path.join("data", "vehicle_data.csv")

if os.path.exists(data_file_path):
    # Read the data
    df = pd.read_csv(data_file_path)
    st.subheader("Loaded Data")
    st.dataframe(df)

    # Preprocessing
    years = [2021, 2022, 2023]
    categories = [
        "passenger_vehicle_new",
        "light_commercial_vehicle_new",
        "passenger_vehicle_2_to_5yrs",
        "light_commercial_vehicle_2_to_5yrs",
        "passenger_vehicle_5yrs",
        "light_commercial_vehicle_5yrs"
    ]

    duties = [
        "passenger_vehicle_new_duty",
        "light_commercial_vehicle_new_duty",
        "passenger_vehicle_2_to_5yrs_duty",
        "light_commercial_vehicle_2_to_5yrs_duty",
        "passenger_vehicle_5yrs_duty",
        "light_commercial_vehicle_5yrs_duty"
    ]

    # Compute additional metrics
    df_analysis = pd.DataFrame({
        "Category": categories,
        "Average Duty per Vehicle": [
            np.mean(df[duty] / df[cat]) for cat, duty in zip(categories, duties)
        ],
        "YoY Growth (Vehicles)": [
            ((df[cat].iloc[-1] - df[cat].iloc[0]) / df[cat].iloc[0]) * 100 for cat in categories
        ],
        "YoY Growth (Duties)": [
            ((df[duty].iloc[-1] - df[duty].iloc[0]) / df[duty].iloc[0]) * 100 for duty in duties
        ],
    })

    df_analysis["Proportion of Total Duty"] = [
        df[duty].sum() / df[[d for d in duties]].sum().sum() * 100 for duty in duties
    ]

    st.subheader("Analysis Results")
    st.dataframe(df_analysis)

    # Visualizations
    # Bar Chart: Duty Revenue by Vehicle Age Category
    st.subheader("Duty Revenue by Vehicle Age Category")
    duty_summary = pd.DataFrame({
        "Year": years,
        "New Vehicles": df[["passenger_vehicle_new_duty", "light_commercial_vehicle_new_duty"]].sum(axis=1),
        "2-5 Years": df[["passenger_vehicle_2_to_5yrs_duty", "light_commercial_vehicle_2_to_5yrs_duty"]].sum(axis=1),
        "5+ Years": df[["passenger_vehicle_5yrs_duty", "light_commercial_vehicle_5yrs_duty"]].sum(axis=1)
    })
    fig_duty = px.bar(
        duty_summary, 
        x="Year", 
        y=["New Vehicles", "2-5 Years", "5+ Years"],
        title="Duty Revenue by Vehicle Age Category",
        labels={"value": "Duty Collected", "variable": "Vehicle Age"}
    )
    st.plotly_chart(fig_duty)

    # Pie Chart: Proportion of Total Duty
    st.subheader("Proportion of Total Duty by Vehicle Category")
    fig_pie = px.pie(
        df_analysis, 
        names="Category", 
        values="Proportion of Total Duty",
        title="Proportion of Total Duty by Vehicle Category",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_pie)

    # Bar Chart: Average Duty per Vehicle
    st.subheader("Average Duty per Vehicle by Category")
    fig_avg_duty = px.bar(
        df_analysis, 
        x="Category", 
        y="Average Duty per Vehicle",
        title="Average Duty per Vehicle by Category",
        labels={"Category": "Vehicle Category", "Average Duty per Vehicle": "Average Duty"},
        color="Average Duty per Vehicle",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_avg_duty)

    # Policy recommendations
    st.subheader("Policy Recommendations")
    st.write("""
    1. **New Vehicles**: Encourage importation through lower tax rates to promote modern fleets and reduce environmental impact.
    2. **2-5 Year Vehicles**: Evaluate current tax rates to optimize revenue while not discouraging imports excessively.
    3. **5+ Year Vehicles**: Consider higher taxes to disincentivize imports of older vehicles, which may have greater environmental and maintenance costs.
    4. Analyze elasticity: How do changes in tax rates affect the number of imports and overall revenue?
    5. Simulate scenarios with different tax policies to identify optimal revenue-generation strategies.
    """)
else:
    st.error("The data file does not exist. Please ensure 'vehicle_data.csv' is placed in the 'data' folder.")
