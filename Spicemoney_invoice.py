import streamlit as st
import pandas as pd
from io import BytesIO

def process_data(data_file):
    data = pd.read_excel(data_file)
    data = data[data['Status'] == 'SUCCESS']
    data['Amount'] = data['Amount'].fillna(0)
    data['Amount'] = data['Amount'].astype(int)
    total_amount = data['Amount'].sum()

    if total_amount <= 50_00_00_000:
        commercial_percentage = 0.0024
    elif total_amount <= 100_00_00_000:
        commercial_percentage = 0.0022
    else:
        commercial_percentage = 0.002

    data['Commercial Value'] = data['Amount'] * commercial_percentage
    data['Calculated Amount'] = data['Commercial Value']
    data.loc[data['Calculated Amount'] < 15, 'Calculated Amount'] = 15
    total_calculated_amount = data['Calculated Amount'].sum()

    summary_data = {
        'Description': ['Agent Total', '18%', 'Total Amount'],
        'Total': [total_amount, None, None],
        'Payout': [total_calculated_amount, total_calculated_amount * 0.18, total_calculated_amount + total_calculated_amount * 0.18]
    }
    summary_df = pd.DataFrame(summary_data)

    return data, summary_df

st.title("Invoice Generator")

# Upload file
data_file = st.file_uploader("Upload Samasta Report", type=["xlsx"])

# Process data when file is uploaded
if st.button("Generate Invoice") and data_file:
    data, summary_df = process_data(data_file)
    
    # Save to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Data')
        summary_df.to_excel(writer, index=False, sheet_name='Summary')
    output.seek(0)
    
    # Provide download link
    st.download_button(
        label="Download Invoice",
        data=output,
        file_name='Spicemoney.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    st.success("Invoice generated successfully!")
