import pandas as pd

def process_excel_calculation(query, excel_path):
    try:
        df = pd.read_excel(excel_path)
        if 'total' in query.lower():
            return f"Total sum: {df.select_dtypes(include='number').sum().sum()}"
        elif 'average' in query.lower():
            return f"Average value: {df.select_dtypes(include='number').mean().mean()}"
        else:
            return "No calculation matched the query."
    except Exception as e:
        return f"Excel calculation failed: {str(e)}"