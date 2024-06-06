import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="401K Contribution Calculator", layout="centered")

# Add a banner image
st.image("https://www.commercebank.com/-/media/cb/articles/personal/2022/articlehero_2680x960401k-(1).jpg?revision=85778e7f-dad7-48a8-a86f-804b305d77db&modified=20220216210438", use_column_width=True)
st.caption("Image credit: Commerce Bank")

# Page title
st.write("# 401K Contribution Calculator")

# Inputs
name = st.text_input("Enter your name")
age = st.slider("Enter your current age", 18, 100, 30)
my_contribution = st.number_input("Enter your monthly contribution", min_value=0.0, step=100.0)
employer_contribution = st.number_input("Enter your employer's monthly contribution", min_value=0.0, step=100.0)
years = st.slider("Enter the number of years the contributions are made", 1, 50, 20)
interest_rate_percent = st.selectbox("Enter the annual interest rate (percent)", list(range(1, 21)))

# Convert interest rate from percent to decimal
interest = interest_rate_percent / 100

# Calculation
if st.button("Calculate"):
    total_monthly = my_contribution + employer_contribution
    total_annual = total_monthly * 12
    total_contribution = total_annual * years
    future_value = (((1 + interest) ** years - 1) / interest) * total_annual

    # Display results
    st.write(f"Hello {name}! Let's analyze your 401K situation:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Age at Retirement", age + years)
        st.metric("Total Monthly Contribution", f"${total_monthly:,.2f}")
        st.metric("Total Annual Contribution", f"${total_annual:,.2f}")
    with col2:
        st.metric(f"Total Contribution after {years} Years", f"${total_contribution:,.2f}")
        st.metric("Future Value of Investment", f"${future_value:,.2f}")

    # Plotting growth over time
    contributions = [total_annual] * years
    future_values = [npf.fv(interest, i, -total_annual, 0) for i in range(1, years + 1)]

    df = pd.DataFrame({
        'Year': np.arange(1, years + 1),
        'Total Contributions': np.cumsum(contributions),
        'Future Value': future_values
    })

    st.write("### Growth Over Time")
    st.line_chart(df.set_index('Year'))

    # Additional Visualization: Bar chart of contributions vs future value
    st.write("### Contributions vs Future Value")
    st.bar_chart(df.set_index('Year')[['Total Contributions', 'Future Value']])


# Add author name to footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: small;
    }
    </style>
    <div class="footer">
        Made with ♥︎ by Amitabha Dey
    </div>
    """,
    unsafe_allow_html=True
)
