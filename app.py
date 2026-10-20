import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Data Detective AI",
    page_icon="🔎",
    layout="wide"
)

# Professional Dashboard Design
st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
    color: #263238;
}

h1, h2, h3 {
    color: #17365D !important;
    font-weight: 700;
}

p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: #263238;
}

[data-testid="stFileUploader"] {
    color: #263238;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #DCE5F0;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 18px;
    font-weight: 600;
}

hr {
    border: none;
    height: 2px;
    background-color: #DCE5F0;
}
</style>
""", unsafe_allow_html=True)

# Project Title
st.title("🔎 Data Detective AI")
st.subheader("Your Intelligent Data Quality Assistant")

st.write(
    "Upload your CSV or Excel dataset to discover hidden data problems, "
    "analyze data quality, and generate useful insights."
)

st.info("👋 Welcome! Upload your dataset using the option below.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Read Dataset
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if df.empty or len(df.columns) == 0:
            st.warning("The uploaded dataset is empty.")

        else:
            st.success("Dataset uploaded successfully!")

            # Original Dataset Information
            original_rows = len(df)
            original_missing = int(df.isnull().sum().sum())
            original_duplicates = int(df.duplicated().sum())

            # Dataset Overview
            st.markdown("---")
            st.header("📊 Dataset Overview")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows", df.shape[0])

            with col2:
                st.metric("Total Columns", df.shape[1])

            with col3:
                st.metric("Duplicate Rows", original_duplicates)

            # Dataset Preview
            st.subheader("👀 Dataset Preview")
            st.dataframe(df.head(10), width="stretch")

            # Missing Value Detection
            st.markdown("---")
            st.subheader("🕵️ Missing Value Detection")

            missing_values = df.isnull().sum()

            missing_df = pd.DataFrame({
                "Column": missing_values.index,
                "Missing Values": missing_values.values
            })

            st.dataframe(missing_df, width="stretch")

            # Data Quality Score
            total_cells = df.shape[0] * df.shape[1]

            if total_cells > 0:
                missing_rate = original_missing / total_cells
                duplicate_rate = original_duplicates / max(len(df), 1)

                quality_score = max(
                    0,
                    round(
                        100 * (
                            1
                            - 0.7 * missing_rate
                            - 0.3 * duplicate_rate
                        )
                    )
                )
            else:
                quality_score = 0

            st.subheader("❤️ Data Health Score")

            st.metric(
                "Data Quality Score",
                f"{quality_score}/100"
            )

            # Interactive Dashboard
            st.markdown("---")
            st.header("📊 Interactive Dashboard")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("📋 Total Rows", len(df))
                st.metric("⚠️ Missing Values", original_missing)

            with col2:
                st.metric("📊 Total Columns", len(df.columns))
                st.metric("🔁 Duplicate Rows", original_duplicates)

            # Numeric Data Analysis
            st.markdown("---")
            st.header("📈 Numeric Data Analysis")

            numeric_df = df.select_dtypes(include=np.number)

            if not numeric_df.empty:

                selected_column = st.selectbox(
                    "Choose a numeric column",
                    numeric_df.columns.tolist()
                )

                fig = px.histogram(
                    numeric_df,
                    x=selected_column,
                    title=f"Distribution of {selected_column}",
                    color_discrete_sequence=["#2563EB"]
                )

                st.plotly_chart(fig, width="stretch")

            else:
                st.info(
                    "No numeric columns found in this dataset "
                    "to create a histogram."
                )

            # AI-Powered Data Insights
            st.markdown("---")
            st.header("🤖 AI-Powered Data Insights")

            st.write(
                f"📌 Your dataset contains **{len(df)} rows** "
                f"and **{len(df.columns)} columns**."
            )

            st.write(f"⚠️ Missing values: **{original_missing}**")
            st.write(f"🔁 Duplicate rows: **{original_duplicates}**")

            numeric_columns = df.select_dtypes(
                include=np.number
            ).columns

            for column in numeric_columns:
                average = df[column].mean()

                if pd.notna(average):
                    st.write(
                        f"📊 Average value of **{column}**: "
                        f"{average:,.2f}"
                    )

            # Business Insights
            st.markdown("---")
            st.header("💡 Business Insights")

            if "Sales" in df.columns:

                sales_df = df.copy()

                sales_df["Sales"] = pd.to_numeric(
                    sales_df["Sales"],
                    errors="coerce"
                )

                valid_sales = sales_df.dropna(subset=["Sales"])

                if not valid_sales.empty:

                    total_sales = valid_sales["Sales"].sum()
                    highest_sale = valid_sales["Sales"].max()
                    lowest_sale = valid_sales["Sales"].min()
                    average_sale = valid_sales["Sales"].mean()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "💰 Total Sales",
                            f"₹{total_sales:,.0f}"
                        )

                        st.metric(
                            "📈 Highest Sale",
                            f"₹{highest_sale:,.0f}"
                        )

                    with col2:
                        st.metric(
                            "📉 Lowest Sale",
                            f"₹{lowest_sale:,.0f}"
                        )

                        st.metric(
                            "📊 Average Sale",
                            f"₹{average_sale:,.2f}"
                        )

                    # Best-Selling Product
                    if "Product" in sales_df.columns:

                        product_data = valid_sales.dropna(
                            subset=["Product"]
                        )

                        if not product_data.empty:

                            product_sales = product_data.groupby(
                                "Product"
                            )["Sales"].sum()

                            if not product_sales.empty:
                                best_product = product_sales.idxmax()

                                st.success(
                                    f"🏆 Best-selling product: "
                                    f"**{best_product}** "
                                    f"(₹{product_sales.max():,.0f})"
                                )

                    # Highest Sales City
                    if "City" in sales_df.columns:

                        city_data = valid_sales.dropna(
                            subset=["City"]
                        )

                        if not city_data.empty:

                            city_sales = city_data.groupby(
                                "City"
                            )["Sales"].sum()

                            if not city_sales.empty:
                                best_city = city_sales.idxmax()

                                st.info(
                                    f"🏙️ Highest sales city: "
                                    f"**{best_city}** "
                                    f"(₹{city_sales.max():,.0f})"
                                )

                    missing_sales = int(
                        sales_df["Sales"].isnull().sum()
                    )

                    if missing_sales > 0:
                        st.warning(
                            f"⚠️ {missing_sales} sales value(s) are missing. "
                            "Clean these values before making business decisions."
                        )

                else:
                    st.warning(
                        "The Sales column does not contain any valid "
                        "numeric values."
                    )

            else:
                st.info(
                    "Business sales insights require a column named "
                    "'Sales'. Other dataset analysis is still available."
                )

            # Advanced Data Visualization
            st.markdown("---")
            st.header("📊 Advanced Data Visualization")

            if "Product" in df.columns and "Sales" in df.columns:

                chart_data = df.copy()

                chart_data["Sales"] = pd.to_numeric(
                    chart_data["Sales"],
                    errors="coerce"
                )

                chart_data = chart_data.dropna(
                    subset=["Product", "Sales"]
                )

                if not chart_data.empty:

                    product_sales = chart_data.groupby(
                        "Product",
                        as_index=False
                    )["Sales"].sum()

                    st.subheader("📱 Product-wise Sales")

                    fig_product = px.bar(
                        product_sales,
                        x="Product",
                        y="Sales",
                        title="Total Sales by Product",
                        text_auto=True,
                        color="Product"
                    )

                    st.plotly_chart(
                        fig_product,
                        width="stretch"
                    )

                    # Product Sales Pie Chart
                    st.subheader("🥧 Product Sales Distribution")

                    fig_pie = px.pie(
                        product_sales,
                        names="Product",
                        values="Sales",
                        title="Sales Share by Product"
                    )

                    st.plotly_chart(
                        fig_pie,
                        width="stretch"
                    )

                else:
                    st.info(
                        "No valid Product and Sales values "
                        "are available for these charts."
                    )

            # City-wise Sales Chart
            if "City" in df.columns and "Sales" in df.columns:

                city_data = df.copy()

                city_data["Sales"] = pd.to_numeric(
                    city_data["Sales"],
                    errors="coerce"
                )

                city_data = city_data.dropna(
                    subset=["City", "Sales"]
                )

                if not city_data.empty:

                    city_sales = city_data.groupby(
                        "City",
                        as_index=False
                    )["Sales"].sum()

                    st.subheader("🏙️ City-wise Sales")

                    fig_city = px.bar(
                        city_sales,
                        x="City",
                        y="Sales",
                        title="Total Sales by City",
                        text_auto=True,
                        color="City"
                    )

                    st.plotly_chart(
                        fig_city,
                        width="stretch"
                    )

            # Smart Data Cleaning
            st.markdown("---")
            st.header("🧹 Smart Data Cleaning")

            st.write(
                "Choose how you want to handle missing values "
                "and duplicate rows."
            )

            cleaning_option = st.selectbox(
                "Choose a cleaning method",
                [
                    "Fill missing values",
                    "Drop rows with missing values"
                ]
            )

            # Create Cleaned Dataset
            cleaned_df = df.drop_duplicates().copy()

            if cleaning_option == "Fill missing values":

                for column in cleaned_df.columns:

                    if cleaned_df[column].isnull().any():

                        if pd.api.types.is_numeric_dtype(
                            cleaned_df[column]
                        ):

                            column_mean = cleaned_df[column].mean()

                            if pd.notna(column_mean):
                                cleaned_df[column] = (
                                    cleaned_df[column].fillna(column_mean)
                                )
                            else:
                                cleaned_df[column] = (
                                    cleaned_df[column].fillna(0)
                                )

                        else:
                            cleaned_df[column] = (
                                cleaned_df[column].fillna("Unknown")
                            )

                st.success(
                    "Missing values handled and duplicate rows removed!"
                )

            elif cleaning_option == "Drop rows with missing values":

                cleaned_df = cleaned_df.dropna()

                st.success(
                    "Rows with missing values and duplicate rows removed!"
                )

            # Cleaning Results
            st.markdown("---")
            st.header("📈 Before vs After Cleaning")

            remaining_rows = len(cleaned_df)
            remaining_missing = int(
                cleaned_df.isnull().sum().sum()
            )
            remaining_duplicates = int(
                cleaned_df.duplicated().sum()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Original Rows", original_rows)

            with col2:
                st.metric("Rows After Cleaning", remaining_rows)

            col3, col4 = st.columns(2)

            with col3:
                st.metric(
                    "Missing Values Before",
                    original_missing
                )

            with col4:
                st.metric(
                    "Missing Values After",
                    remaining_missing
                )

            col5, col6 = st.columns(2)

            with col5:
                st.metric(
                    "Duplicate Rows Before",
                    original_duplicates
                )

            with col6:
                st.metric(
                    "Duplicate Rows After",
                    remaining_duplicates
                )

            st.subheader("👀 Cleaned Dataset Preview")

            st.dataframe(
                cleaned_df.head(10),
                width="stretch"
            )

            # Download Cleaned Dataset
            st.markdown("---")
            st.header("📥 Download Cleaned Dataset")

            csv_data = cleaned_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as error:
        st.error(f"Unable to analyze this file: {error}")