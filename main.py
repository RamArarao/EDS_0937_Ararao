import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# CREATE FOLDERS
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# LOAD DATA
def load_dataset(file):

    try:

        data = pd.read_csv(file)

        # RENAME COLUMNS
        data = data.rename(columns={
            'PROPERTY: HV': 'Hardness',
            'PROPERTY: grain size ($\\mu$m)': 'Grain_Size',
            'PROPERTY: YS (MPa)': 'Yield_Strength',
            'PROPERTY: UTS (MPa)': 'Tensile_Strength'
        })

        print("Dataset loaded successfully!")

        return data

    except Exception as e:

        print("Loading error:", e)

# CLEAN DATA
def clean_dataset(data):

    try:

        data = data.drop_duplicates()

        columns = [
            'Hardness',
            'Grain_Size',
            'Yield_Strength',
            'Tensile_Strength'
        ]

        for col in columns:

            data[col] = pd.to_numeric(
                data[col],
                errors='coerce'
            )

            data[col] = data[col].fillna(
                data[col].median()
            )

        data.to_csv(
            "data/dataset_cleaned.csv",
            index=False
        )

        print("Dataset cleaned successfully!")

        return data

    except Exception as e:

        print("Cleaning error:", e)

# COMPARATIVE ANALYSIS
def compare_hardness(data):

    try:

        fine_grain = data[
            data['Grain_Size'] <= 40
        ]['Hardness']

        coarse_grain = data[
            data['Grain_Size'] > 40
        ]['Hardness']

        print("\n===== COMPARATIVE ANALYSIS =====")

        print(
            "Fine Grain Hardness Mean:",
            np.mean(fine_grain)
        )

        print(
            "Coarse Grain Hardness Mean:",
            np.mean(coarse_grain)
        )

        if np.mean(fine_grain) > np.mean(coarse_grain):

            print(
                "Fine grain materials have higher hardness."
            )

        else:

            print(
                "Coarse grain materials have higher hardness."
            )

    except Exception as e:

        print("Comparative analysis error:", e)

# UNIQUE FILTER
def filter_materials(data):

    try:

        filtered = data[
            (data['Hardness'] >= 180) &
            (data['Yield_Strength'] >= 300)
        ]

        print("Unique filter applied!")

        return filtered

    except Exception as e:

        print("Filter error:", e)

# STATISTICAL ANALYSIS
def analyze_statistics(data):

    try:

        hardness = data['Hardness']

        print("\n===== STATISTICAL ANALYSIS =====")

        print("Mean:", np.mean(hardness))

        print("Median:", np.median(hardness))

        print("Standard Deviation:", np.std(hardness))

        print("Variance:", np.var(hardness))

        print("Skewness:", hardness.skew())

        print("\n===== ENGINEERING INTERPRETATION =====")

        if np.mean(hardness) > 180:

            print(
                "The material shows strong hardness characteristics."
            )

        else:

            print(
                "The material shows lower hardness characteristics."
            )

        if np.std(hardness) > 15:

            print(
                "Material hardness values are highly varied."
            )

        else:

            print(
                "Material hardness values are stable."
            )

        Q1 = hardness.quantile(0.25)

        Q3 = hardness.quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR

        upper = Q3 + 1.5 * IQR

        outliers = hardness[
            (hardness < lower) |
            (hardness > upper)
        ]

        print("Outliers Detected:", len(outliers))

    except Exception as e:

        print("Statistics error:", e)

# CORRELATION ANALYSIS
def correlation_analysis(data):

    try:

        print("\n===== CORRELATION ANALYSIS =====")

        corr = data.corr(
            numeric_only=True
        )

        print(corr)

        print("\n===== ENGINEERING INTERPRETATION =====")

        print(
            "Strong positive values indicate direct relationships."
        )

        print(
            "Negative values indicate inverse relationships."
        )

    except Exception as e:

        print("Correlation error:", e)

# VISUALIZATIONS
def create_graphs(data):

    try:

        # HISTOGRAM
        plt.figure(figsize=(6,4))

        plt.hist(
            data['Hardness'],
            bins=12
        )

        plt.title(
            "Hardness Distribution"
        )

        plt.xlabel("Hardness")

        plt.ylabel("Frequency")

        plt.savefig(
            "outputs/histogram.png"
        )

        plt.close()

        # SCATTERPLOT
        plt.figure(figsize=(6,4))

        plt.scatter(
            data['Grain_Size'],
            data['Hardness']
        )

        plt.title(
            "Grain Size vs Hardness"
        )

        plt.xlabel("Grain Size")

        plt.ylabel("Hardness")

        plt.savefig(
            "outputs/scatterplot.png"
        )

        plt.close()

        # HEATMAP
        plt.figure(figsize=(6,4))

        corr = data.corr(
            numeric_only=True
        )

        plt.imshow(corr)

        plt.colorbar()

        plt.xticks(
            range(len(corr.columns)),
            corr.columns,
            rotation=45
        )

        plt.yticks(
            range(len(corr.columns)),
            corr.columns
        )

        plt.title(
            "Correlation Heatmap"
        )

        plt.savefig(
            "outputs/heatmap.png"
        )

        plt.close()

        # BOXPLOT
        plt.figure(figsize=(6,4))

        plt.boxplot(
            data['Hardness']
        )

        plt.title(
            "Hardness Boxplot"
        )

        plt.savefig(
            "outputs/boxplot.png"
        )

        plt.close()

        print("Graphs generated successfully!")

    except Exception as e:

        print("Visualization error:", e)

# ANIMATED VISUALIZATION
def animated_visuals(data):

    try:

        data['Strength_Group'] = pd.cut(
            data['Yield_Strength'],
            bins=5,
            labels=[
                'Very Low',
                'Low',
                'Medium',
                'High',
                'Very High'
            ]
        )

        # ANIMATED SCATTER
        animation1 = px.scatter(
            data,
            x='Grain_Size',
            y='Hardness',
            color='Strength_Group',
            animation_frame='Strength_Group',
            title='Animated Grain Size vs Hardness'
        )

        animation1.write_html(
            "outputs/animated_scatter.html"
        )

        # ANIMATED HISTOGRAM
        animation2 = px.histogram(
            data,
            x='Hardness',
            color='Strength_Group',
            animation_frame='Strength_Group',
            title='Animated Hardness Distribution'
        )

        animation2.write_html(
            "outputs/animated_histogram.html"
        )

        print("Animated graphs generated!")

    except Exception as e:

        print("Animation error:", e)

# MAIN PROGRAM
dataset = load_dataset(
    "data/dataset_original.csv"
)

if dataset is not None:

    dataset = clean_dataset(dataset)

    compare_hardness(dataset)

    filtered_dataset = filter_materials(dataset)

    analyze_statistics(dataset)

    correlation_analysis(dataset)

    create_graphs(dataset)

    animated_visuals(dataset)

    print("\nPROJECT COMPLETED SUCCESSFULLY!")