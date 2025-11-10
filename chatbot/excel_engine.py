import pandas as pd

# ✅ Function to load and preprocess Excel
def load_excel(file_path):
    try:
        df = pd.read_excel(file_path)

        required = ["InvoiceNo", "Description", "Quantity", "UnitPrice", "Country", "CustomerID"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        df.dropna(subset=["InvoiceNo", "Description"], inplace=True)
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
        return df
    except Exception as e:
        return str(e)

# ✅ Function to answer Excel questions
def answer_excel_question(df, question):
    q = question.lower().strip()

    try:
        df["Country"] = df["Country"].astype(str).str.strip()
        df["Description"] = df["Description"].astype(str).str.strip()
        original_df = df.copy()

        matched_country = None
        matched_product = None

        for c in df["Country"].dropna().unique():
            if c.lower() in q:
                matched_country = c
                df = df[df["Country"].str.lower() == c.lower()]
                break

        for p in df["Description"].dropna().unique():
            if p.lower() in q:
                matched_product = p
                df = df[df["Description"].str.lower() == p.lower()]
                break

        if df.empty:
            return f"⚠️ No matching data found for your query{' in ' + matched_country if matched_country else ''}."

        if any(k in q for k in ["total sales", "sum of sales", "total amount", "total revenue", "sales value"]):
            return f"💰 Total sales value{' in ' + matched_country if matched_country else ''}: £{df['TotalPrice'].sum():.2f}"

        elif any(k in q for k in ["average sales", "average total", "mean sales", "average revenue"]):
            return f"📊 Average total sales{' in ' + matched_country if matched_country else ''}: £{df['TotalPrice'].mean():.2f}"

        elif any(k in q for k in ["average price", "avg price", "mean price", "price average"]):
            return f"💲 Average unit price{' in ' + matched_country if matched_country else ''}: £{df['UnitPrice'].mean():.2f}"

        elif any(k in q for k in ["total quantity", "quantity sold", "sum of quantity", "units sold"]):
            return f"📦 Total quantity sold{' in ' + matched_country if matched_country else ''}: {df['Quantity'].sum()}"

        elif "average quantity" in q or "mean quantity" in q:
            return f"📦 Average quantity per transaction{' in ' + matched_country if matched_country else ''}: {df['Quantity'].mean():.2f}"

        elif any(k in q for k in ["number of sales", "count of sales", "sales count", "invoice count"]):
            return f"#️⃣ Number of unique sales{' in ' + matched_country if matched_country else ''}: {df['InvoiceNo'].nunique()}"

        elif any(k in q for k in ["top product", "best product", "most sold product", "most popular product"]):
            top_product = df.groupby("Description")["TotalPrice"].sum().idxmax()
            return f"🏆 Top selling product{' in ' + matched_country if matched_country else ''}: {top_product}"

        elif any(k in q for k in ["top country", "highest sales country", "best performing country"]):
            top_country = original_df.groupby("Country")["TotalPrice"].sum().idxmax()
            return f"🌍 Country with highest total sales: {top_country}"

        elif any(k in q for k in ["top customer", "highest paying customer", "customer with highest sales"]):
            top_customer = original_df.groupby("CustomerID")["TotalPrice"].sum().idxmax()
            return f"🧑 Customer with highest total sales: {int(top_customer)}"

        elif "sales" in q:
            return f"💰 Total sales across dataset: £{original_df['TotalPrice'].sum():.2f}"

        return "❓ Sorry, I couldn't understand your Excel-related question. Try rephrasing or use keywords like 'total sales', 'average', or 'top'."

    except Exception as e:
        return f"❌ Error processing Excel question: {str(e)}"
