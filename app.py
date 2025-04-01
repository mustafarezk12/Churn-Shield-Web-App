import streamlit as st
import pandas as pd
import numpy as np
import pickle
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

df = pd.read_csv("exported_data.csv")

# Load the model and mean/std values
model_filename = "model(1).pkl"

with open(model_filename, "rb") as file:
    model = pickle.load(file)

with open("mean_std_values.pkl", "rb") as f:
    mean_std_values = pickle.load(f)
st.set_page_config(page_title=" Churn Shield", layout="wide")


# Define the plotting functions


def make_histogram(
    df, target_feature, bins=10, custom_ticks=None, unit="", additional=""
):
    plt.figure(figsize=(10, 5))
    plt.hist(df[target_feature], bins=bins)
    if custom_ticks is not None:
        plt.xticks(custom_ticks)
    plt.ylabel("Count")
    plt.xlabel(target_feature)
    plt.title(f"Distribution of {target_feature.lower()}{additional}:\n")
    plt.grid()
    st.pyplot(plt)
    st.write(
        f"Distribution of {target_feature.lower()}{additional}: {df[target_feature].mean():.2f} ± {df[target_feature].median():.2f} {unit}\n"
        f"Median: {df[target_feature].median():.2f} {unit}\n"
        f"Minimum: {df[target_feature].min()} {unit}\n"
        f"Maximum: {df[target_feature].max()} {unit}\n"
        f"Skewness: {df[target_feature].skew():.3f}"
    )


def make_piechart(df, target_feature, additional="", width=300, height=300):
    # Convert pixel dimensions to inches
    width_in = width / 96  # 96 DPI is standard
    height_in = height / 96

    dict_of_val_counts = dict(df[target_feature].value_counts())
    data = list(dict_of_val_counts.values())
    keys = list(dict_of_val_counts.keys())

    # Create the pie chart with "flare" palette
    palette_color = sns.color_palette(
        "flare", len(keys)
    )  # Generate a palette with enough colors
    fig, ax = plt.subplots(figsize=(width_in, height_in))  # Custom size
    ax.pie(data, labels=keys, colors=palette_color, autopct="%.0f%%")
    ax.set_title(f"Distribution of Customer's {target_feature}:")

    # Streamlit display
    st.pyplot(fig)

    # Console print for debugging
    print_str = f"Distribution of customer's {target_feature.lower()}{additional}:"
    for k, v in zip(keys, data):
        print_str += f"\n{v} {k}"
    print(print_str)


def make_barplot(df, target_feature, custom_ticks=None, unit="", additional=""):
    plt.figure(figsize=(10, 5))
    dict_of_val_counts = dict(df[target_feature].value_counts())
    data = list(dict_of_val_counts.values())
    keys = list(dict_of_val_counts.keys())
    plt.bar(keys, data)
    if custom_ticks is not None:
        plt.xticks(custom_ticks)
    plt.xlabel(f"{target_feature.capitalize()}{additional}")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of customer's {target_feature.lower()}{additional}\n")
    plt.grid(axis="y")
    st.pyplot(plt)  # Display bar chart in Streamlit
    st.write(
        f"Distribution of customer's {target_feature.lower()}{additional}: {df[target_feature].mean():.2f} ± {df[target_feature].median():.2f} {unit}\n"
        f"Median: {df[target_feature].median():.2f} {unit}\n"
        f"Minimum: {df[target_feature].min()} {unit}\n"
        f"Maximum: {df[target_feature].max()} {unit}\n"
        f"Skewness: {df[target_feature].skew():.3f}"
    )


def make_boxplot(df, feature):
    plt.figure(figsize=(10, 5))
    sns.boxplot(df, x=feature)
    plt.title(f"Boxplot of {feature}\n")
    plt.xlabel(feature)
    plt.ylabel("Values")
    st.pyplot(plt)


# 1. Define the Home page
def home_page():
    outer_col1, outer_col2, outer_col3 = st.columns([1, 5, 1])
    with outer_col2:
        with st.container():
            col1, col2 = st.columns([2.5, 1])
            with col1:
                st.header("About this app", anchor=None)
                st.markdown(
                    "<div style='font-size:22px;'>- Easily predict if a customer is likely to churn or not using our <span style='color:red;'>Customer Churn Predictor</span>.<br>"
                    "- View customer churn behavior using our <span style='color:red;'>Insights</span>.</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.image("LOGO.jpg", width=400)

        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.header("What is customer churn?")
                st.write(
                    "<div style='font-size:20px;'>Customer churn occurs when customers stop using a company's products. This can result from various factors. "
                    "Customer features like ratings and usage metrics provide insight into customer behavior, especially when they're about to churn.</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.header("Why predict customer churn?")
                st.write(
                    "<div style='font-size:20px;'>It's much more expensive to acquire new customers than to retain existing ones. "
                    "Predicting customer churn and identifying early warning signs can save significant costs for a company.</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<hr style='border: 2px solid gray;'>", unsafe_allow_html=True)

        st.markdown(
            "<h2 style='text-align: center;'>About Dataset</h2>", unsafe_allow_html=True
        )

        st.write(
            "<div style='font-size:18px; text-align: justify;padding: 20px;'>The churn label indicates whether a customer has churned or not. A churned customer is one who has decided to discontinue their subscription or usage of the company's services. On the other hand, a non-churned customer is one who continues to remain engaged and retains their relationship with the company.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='font-size:18px; text-align: justify;padding: 20px;'>The dataset includes customer information such as age, gender, tenure, usage frequency, support calls, payment delay, "
            "subscription type, contract length, total spend, and last interaction details. This information is used to predict whether a customer is likely to churn based on these behaviors.</div>",
            unsafe_allow_html=True,
        )
        st.write(
            "<div style='font-size:18px; text-align: justify; padding: 20px;'>"
            "These datasets contain 12 feature columns. In detail, these are:<br><br>"
            "<ul>"
            "<li><b>CustomerID:</b> A unique identifier for each customer</li>"
            "<li><b>Age:</b> The age of the customer</li>"
            "<li><b>Gender:</b> Gender of the customer</li>"
            "<li><b>Tenure:</b> Duration in months for which a customer has been using the company's products or services</li>"
            "<li><b>Usage Frequency:</b> Number of times the customer has used the company’s services in the last month</li>"
            "<li><b>Support Calls:</b> Number of calls the customer has made to customer support in the last month</li>"
            "<li><b>Payment Delay:</b> Number of days the customer has delayed their payment in the last month</li>"
            "<li><b>Subscription Type:</b> Type of subscription the customer has chosen</li>"
            "<li><b>Contract Length:</b> Duration of the contract the customer has signed with the company</li>"
            "<li><b>Total Spend:</b> Total amount of money the customer has spent on the company's products or services</li>"
            "<li><b>Last Interaction:</b> Number of days since the last interaction the customer had with the company</li>"
            "<li><b>Churn:</b> Binary label indicating whether a customer has churned (1) or not (0)</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )


# 2. Define the Prediction page
def predict_page():
    outer_col1, outer_col2, outer_col3 = st.columns([1, 5, 1])
    with outer_col2:
        # Add image centered
        with st.container():
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.image("image.png", use_column_width=True)

        st.title("Customer Behavior Prediction")

        # Input fields for the user to enter data
        st.header("Enter Customer Details:")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        tenure = st.number_input(
            "Tenure (Months)", min_value=0, max_value=100, value=12
        )
        usage_frequency = st.number_input(
            "Usage Frequency (Last Month)", min_value=0, max_value=100, value=10
        )
        support_calls = st.number_input(
            "Support Calls (Last Month)", min_value=0, max_value=50, value=3
        )
        payment_delay = st.number_input(
            "Payment Delay (Days)", min_value=0, max_value=100, value=5
        )
        subscription_type = st.selectbox(
            "Subscription Type", ["Standard", "Premium", "Basic"]
        )
        contract_length = st.selectbox(
            "Contract Length", ["Monthly", "Annual", "Quarterly"]
        )
        total_spend = st.number_input(
            "Total Spend", min_value=0.0, value=500.0, step=0.1
        )
        last_interaction = st.number_input(
            "Last Interaction (Days)", min_value=0, max_value=100, value=20
        )

        # Convert categorical features to numerical
        gender_dict = {"Male": 1, "Female": 0}
        subscription_dict = {"Standard": 2, "Premium": 1, "Basic": 0}
        contract_dict = {"Monthly": 1, "Annual": 0, "Quarterly": 2}

        gender_val = gender_dict[gender]
        subscription_val = subscription_dict[subscription_type]
        contract_val = contract_dict[contract_length]

        # Prepare the input data
        input_data = np.array(
            [
                age,
                gender_val,
                tenure,
                usage_frequency,
                support_calls,
                payment_delay,
                subscription_val,
                contract_val,
                total_spend,
                last_interaction,
            ]
        ).reshape(1, -1)

        # Normalize the input data
        input_data = (input_data - mean_std_values["mean"]) / mean_std_values["std"]

        # Add the predict button
        if st.button("Predict"):
            # Perform the prediction
            prediction = model.predict(input_data)
            prediction_proba = model.predict_proba(input_data)

            if prediction[0] == 1:
                bg_color = "red"
                prediction_result = "The customer has churned"
            else:
                bg_color = "green"
                prediction_result = "The customer has not churned"

            confidence = (
                prediction_proba[0][1] if prediction[0] == 1 else prediction_proba[0][0]
            )

            # Display the result
            st.markdown(
                f"<p style='background-color:{bg_color}; color:white; padding:15px; font-size:18px;'>Prediction: {prediction_result}<br>Confidence: {((confidence * 10000) // 1) / 100}%</p>",
                unsafe_allow_html=True,
            )


# 3. Define the Insights page (Placeholder for visuals)
def insights_page():
    outer_col1, outer_col2, outer_col3 = st.columns([1, 5, 1])
    with outer_col2:
        with st.container():
            st.header("Customer Churn Behavior Analysis")
            st.write(
                "In this section, you can view visual insights regarding customer churn behavior."
            )

            st.markdown("<hr style='border: 2px solid gray;'>", unsafe_allow_html=True)

            # First plot with description
            st.subheader("1. Distribution of customer's gender")
            st.write("""
                There are more male customers in the company.
            """)
            make_piechart(df, "Gender", width=230, height=230)

            # Second plot with description
            st.subheader("2. Distribution of customer's subscription type")

            st.write("""
                    There is a close balance of customers among the three subscription types: Standard, Premium, and Basic.
                """)

            make_piechart(df, "Subscription Type")

            # Third plot with description
            st.subheader("3. Distribution of customer's contract length")

            st.write("""
                    Annual and quarterly contracts have similar and the highest number of customer counts, followed by monthly contracts with the lowest number of customers.
                """)

            make_piechart(df, "Contract Length")

            # Fourth plot with description
            st.subheader("4. Distribution of cutomer's age (years)")

            st.write("""
                    Most customers are aged 40-50 with age 50 being the most common. There's very low number of customers of age 51 and above.
                """)
            make_barplot(
                df,
                "Age",
                custom_ticks=np.arange(0, 66, 5),
                additional=" (years)",
                unit="years",
            )

            # Fifth plot with description
            st.subheader("5. Distribution of cutomer's support_calls")
            col1, col2 = st.columns([2.5, 1])

            st.write("""
                    On average, customers tend to make 3 support calls in a month. Customers tend to make 1 or 2 support calls per month, with the most make no support calls at all.
                """)

            make_barplot(df, "Support Calls", unit="calls", additional=" (in a month)")
            # Sixth plot with description
            st.subheader("6. Customer Churn Dashboard")
            st.image("dash.png", use_column_width=True)


# 4. Upper navbar to navigate between pages
selected = option_menu(
    menu_title=None,
    options=["Home", "Insights", "Predict"],
    icons=["house", "graph-up-arrow", "bar-chart-line"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f8f9fa"},
        "nav-link": {
            "font-size": "20px",
            "text-align": "center",
            "margin": "0px",
            "width": "100%",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#0d6efd"},
    },
)

# 5. Render the selected page
if selected == "Home":
    home_page()
elif selected == "Predict":
    predict_page()
elif selected == "Insights":
    insights_page()
