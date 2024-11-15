import streamlit as st
import pandas as pd

# App Title
st.title("Palliative Care Program Metrics Projection")

# User Inputs
total_population = st.number_input("Eligible Beneficiaries", value=326504)
eligible_population = st.number_input("Eligible for Palliative Care", value=6360)
target_enrollment_percent = st.slider("Target Enrollment (%)", 0, 100, 20) / 100
initial_enrollment_percent = st.slider("Initial Enrollment in First Month (%)", 0, 100, 10) / 100
monthly_growth_rate = st.slider("Monthly Growth Rate (%)", 0.0, 100.0, 12.5) / 100
monthly_attrition_rate = st.slider("Monthly Attrition Rate (%)", 0.0, 100.0, 5.0) / 100
hospice_conversion_rate = st.slider("Hospice Conversion Rate (%)", 0.0, 100.0, 37.0) / 100
projection_months = st.slider("Number of Projection Months", 1, 60, 60)

# Calculating target enrollment
target_enrollment = int(eligible_population * target_enrollment_percent)
initial_enrollment = int(target_enrollment * initial_enrollment_percent)

# Initializing lists to store the results
months = list(range(1, projection_months + 1))
new_enrollments = []
departures = []
census = []
hospice_conversions = []

# Initial variable
current_census = initial_enrollment

# Loop to calculate metrics month by month
for month in months:
    # Calculating new enrollments
    if month == 1:
        new_enrollment = initial_enrollment
    else:
        new_enrollment = int(current_census * monthly_growth_rate)

    # Calculating departures
    departure = int(current_census * monthly_attrition_rate)

    # Calculating hospice conversions
    hospice_conversion = int(departure * hospice_conversion_rate)

    # Updating the census
    current_census = current_census + new_enrollment - departure

    # Storing results
    new_enrollments.append(new_enrollment)
    departures.append(departure)
    census.append(current_census)
    hospice_conversions.append(hospice_conversion)

# Creating a DataFrame for the results
df = pd.DataFrame({
    'Month': months,
    'New Enrollments': new_enrollments,
    'Departures': departures,
    'Census': census,
    'Hospice Conversions': hospice_conversions
})

# Displaying the results
st.subheader("Projection Results")
st.dataframe(df)

# Allow the user to download the results
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name='palliative_care_projection.csv',
    mime='text/csv'
)