import pandas as pd


# =========================
# LOAD DATA
# =========================
def load_data(path):
    df = pd.read_excel(path)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    print("Columns after cleaning:", df.columns.tolist())

    # Map different column names to standard names
    column_mapping = {
        'date': 'date',
        'dates': 'date',
        'day': 'date',

        'state': 'state',
        'region': 'state',

        'sales': 'sales',
        'sales_amount': 'sales',
        'revenue': 'sales',
        'total': 'sales'   # your dataset fix
    }

    df = df.rename(columns={col: column_mapping.get(col, col) for col in df.columns})

    # Validate required columns
    required_cols = ['date', 'state', 'sales']
    for col in required_cols:
        if col not in df.columns:
            raise Exception(f"Missing required column: {col}")

    # Convert types
    df['date'] = pd.to_datetime(df['date'])
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    # Sort
    df = df.sort_values(['state', 'date'])

    return df


# =========================
# HANDLE MISSING DATES
# =========================
def fill_missing_dates(df):

    def fill(group):
        state_value = group.name  # SAFE way

        idx = pd.date_range(group['date'].min(), group['date'].max())

        group = group.set_index('date').reindex(idx)

        group['state'] = state_value

        return group

    df = df.groupby('state', group_keys=False).apply(fill).reset_index()
    df.rename(columns={'index': 'date'}, inplace=True)

    return df


# =========================
# HANDLE MISSING VALUES
# =========================
def fill_missing_values(df):
    df['sales'] = df['sales'].ffill()
    df['sales'] = df['sales'].bfill()
    return df