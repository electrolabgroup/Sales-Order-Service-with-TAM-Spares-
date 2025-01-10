from flask import Flask, render_template, request, send_from_directory
import requests
import pandas as pd
from datetime import datetime
import os
import pandas as pd
from flask import Flask, send_file, render_template
import requests
from fuzzywuzzy import process

app = Flask(__name__)

base_url = 'https://erpv14.electrolabgroup.com/'
endpoint = 'api/resource/Sales Order'

headers = {
    'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
}

def retrieve_data(name):
    limit_start = 0
    limit_page_length = 1000
    all_data = []

    while True:
        params = {
            'fields': '["name","customer","items.item_code","items.item_name","items.serial_no","items.item_name","territory","items.qty","address_display","shipping_address","shipping_address_name","po_no","po_date","freight_term","payment_terms_template","currency","items.rate","items.amount","freight_amt","packing_charges","total_net_weight","items.gst_hsn_code","items.uom","total_net_weight","net_total","taxes.account_head","taxes.tax_amount","taxes.total"]',
            'limit_start': limit_start,
            'limit_page_length': limit_page_length,
            'filters': f'[["name", "in", "{name}"]]'
        }

        response = requests.get(base_url + endpoint, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            current_page_data = data.get('data', [])

            if not current_page_data:
                break  # No more data to fetch

            all_data.extend(current_page_data)
            limit_start += limit_page_length
        else:
            print(f"Error: {response.status_code}")
            break

    if all_data:
        so_df = pd.DataFrame(all_data)
        # Sort the DataFrame by the 'amount' column in descending order
        so_df = so_df.sort_values(by='amount', ascending=False)
        so_df['qty'] = so_df['qty'].round(0).astype(int)

        return so_df
    else:
        return None

@app.route('/generate_excel')
def generate_excel():
    # Assuming you have your code for generating the final DataFrame (grouped_final_df)
    
    templates_folder = os.path.join(os.path.dirname(__file__), 'templates')
    
    # Read the Excel file from the templates folder
    key_df = pd.read_excel(os.path.join(templates_folder, 'productgroup.xlsx'))

    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Customer'
    url = base_url + endpoint

    params = {
        'fields': '["name","customer_group","territory","disabled"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
        'filters': '[["customer_group", "!=", "Foreign Customers"]]'
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Fields are correct.")
        customer = pd.DataFrame(data['data'])
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.json())


    # %%
    customer.rename(columns={
        'name': 'ID',
        'customer_group': 'Customer Group',
        'territory': 'Territory',
        'disabled': 'Disabled'
    }, inplace=True)
    customer.head()

    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Opportunity'
    url = base_url + endpoint

    params = {
        'fields': '["name","source","deal_pipeline","customer_name","items.item_code","items.item_group","items.item_name"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
        'filters': '[["status", "not in", ["Order Won", "Lost", "Order Lost", "Converted", "Closed"]],["deal_pipeline", "=", "Spares"]]'
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Fields are correct.")
        opp_df = pd.DataFrame(data['data'])
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.json())


    # %%
    opp_df.rename(columns={
        'name': 'ID',
        'source': 'Source',
        'deal_pipeline': 'Deal Pipeline',
        'customer_name': 'Customer Name',
        'item_code': 'Item Code (Opportunity Item)',
        'item_group': 'Item Group (Opportunity Item)',
        'item_name': 'Item Name (Opportunity Item)'
    }, inplace=True)
    opp_df.head()



    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Opportunity'
    url = base_url + endpoint

    params = {
        'fields': '["name","source","deal_pipeline","customer_name","items.item_code","items.item_group","items.item_name","transaction_date"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
        'filters': '[["deal_pipeline", "=", "Spares"]]'
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Fields are correct.")
        opp_df1 = pd.DataFrame(data['data'])
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.json())


    # %%
    opp_df1.rename(columns={
        'name': 'ID',
        'source': 'Source',
        'deal_pipeline': 'Deal Pipeline',
        'customer_name': 'Customer Name',
        'item_code': 'Item Code (Opportunity Item)',
        'item_group': 'Item Group (Opportunity Item)',
        'item_name': 'Item Name (Opportunity Item)',
        'transaction_date': 'Opportunity Date',
    }, inplace=True)
    opp_df1.head()



    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Sales Order'
    url = base_url + endpoint

    params = {
        'fields': '["name","source","customer","customer_name","items.item_code","items.item_group","items.item_name","items.qty","naming_series"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Fields are correct.")
        sales_df = pd.DataFrame(data['data'])
        sales_df = sales_df[sales_df['naming_series'].str.contains('SODS|SODM', na=False)]
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.json())


    # %%
    sales_df.rename(columns={
        'name': 'ID',
        'source': 'Source',
        'customer': 'Customer',
        'customer_name': 'Customer Name',
        'item_code': 'Item Code (Sales Order Item)',
        'item_name': 'Item Name (Sales Order Item)',
        'item_group': 'Item Group (Sales Order Item)',
        'qty': 'Quantity (Sales Order Item)',
        'naming_series': 'Series'
    }, inplace=True)
    sales_df.head()

    base_url = 'https://erpv14.electrolabgroup.com/'
    endpoint = 'api/resource/Serial No'
    url = base_url + endpoint

    params = {
        'fields': '["name","customer","customer_instrument_id","item_code","item_name","customer_name","territory","serial_no","amc_expiry_date","item_group"]',
        'limit_start': 0, 
        'limit_page_length': 100000000000,
    }

    headers = {
        'Authorization': 'token 3ee8d03949516d0:6baa361266cf807'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Fields are correct.")
        serial_df = pd.DataFrame(data['data'])
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print("Response:", response.json())


    # %%
    serial_df.rename(columns={
        'name': 'ID',
        'customer': 'Customer',
        'customer_instrument_id': 'Customer Instrument ID',
        'item_code': 'Item Code',
        'item_name': 'Item Name',
        'customer_name': 'Customer Name',
        'territory': 'Territory',
        'serial_no': 'Serial No',
        'amc_expiry_date': 'AMC Expiry Date',
        'item_group': 'Item Group'
    }, inplace=True)
    serial_df.head()

    # %%
    customer.rename(columns = {'ID':'Customer'},inplace = True)

    # %%
    serial_df = pd.merge(serial_df, customer,on = 'Customer', how = 'left')

    # %%
    serial_df.rename(columns = {'Territory_x':'Territory'}, inplace = True)
    serial_df.head()

    # %%
    from fuzzywuzzy import process

    def match_item_groups(row, serial_item_groups, threshold=80):
        matches = [match for match, score in process.extract(row['item_group'], serial_item_groups) if score >= threshold]
        return matches
    serial_item_groups = serial_df['Item Group'].tolist()

    # Apply fuzzy matching to find multiple matches
    key_df['matched_item_groups'] = key_df.apply(match_item_groups, serial_item_groups=serial_item_groups, axis=1)
    # Explode the matched groups to create multiple rows
    key_df_exploded = key_df.explode('matched_item_groups').dropna(subset=['matched_item_groups'])

    # Merge with serial_df using exploded matches
    merged_df = pd.merge(key_df_exploded, serial_df, left_on='matched_item_groups', right_on='Item Group', how='inner')
    # %%
    grouped_df = merged_df.groupby(['Item Group', 'item_group', 'Customer', 'item_code','Customer Group','Territory']).size().reset_index(name='count_tam')
    # %%
    # Group by 'Item Code' and 'Customer Name' and count the occurrences
    grouped_opp_df = opp_df.groupby(['Item Code (Opportunity Item)', 'Customer Name']).size().reset_index(name='count_opp')
    grouped_opp_df.head()

    # %%
    # Group by 'Item Code' and 'Customer Name' and count the occurrences
    grouped_opp_df1 = opp_df1.groupby(['Item Code (Opportunity Item)', 'Customer Name']).size().reset_index(name='created_this_month')

    # %%
    # Group by 'Item Code (Sales Order Item)' and 'Customer Name', then sum the 'Quantity' for each group
    grouped_sales_df = sales_df.groupby(['Item Code (Sales Order Item)', 'Customer Name'])['Quantity (Sales Order Item)'].sum().reset_index(name='count_sales')
    # %%
    # First merge grouped_df with grouped_sales_df on item_code and Customer Name
    merged_df_sales = pd.merge(grouped_df, grouped_sales_df, 
                            left_on=['item_code', 'Customer'], 
                            right_on=['Item Code (Sales Order Item)', 'Customer Name'], 
                            how='left')

    # Now merge the result with grouped_opp_df on item_code and Customer Name
    merged_df_sales1 = pd.merge(merged_df_sales, grouped_opp_df, 
                            left_on=['item_code', 'Customer Name'], 
                            right_on=['Item Code (Opportunity Item)', 'Customer Name'], 
                            how='left')
    final_merged_df = pd.merge(merged_df_sales1, grouped_opp_df1, 
                            left_on=['item_code', 'Customer Name'], 
                            right_on=['Item Code (Opportunity Item)', 'Customer Name'], 
                            how='left')

    # %%
    # Grouping by the desired columns and summing the count columns
    grouped_final_df = final_merged_df.groupby(['Item Group', 'item_group', 'Customer','Customer Group','Territory' ,'item_code']).agg(
        {
            'count_tam': 'sum',   # Summing count_tam
            'count_sales': 'sum',       # Summing count from grouped_sales_df
            'count_opp': 'sum',
            'created_this_month':'sum'# Summing count_opp from grouped_opp_df
        }
    ).reset_index()

    # Display the grouped dataframe
    grouped_final_df.head()

    # %%
    # Rename the count columns in the grouped_final_df
    grouped_final_df.rename(columns={
        'count_tam': 'Tam Count (Total Quantity Available with Customer)',
        'count_sales': 'Count Sales (According to the Quantity Booked)',
        'count_opp': 'Count Of Open Opportunity',
        'created_this_month':'Created This Month'
    }, inplace=True)

    # Initialize an Excel writer with xlsxwriter
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder, 'HelpThemToBuy.xlsx')

    # Initialize an Excel writer with xlsxwriter
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        # Loop over each unique item_code
        for item_code in grouped_final_df['item_code'].unique():
            # Filter the dataframe for the current item_code
            df_item_code = grouped_final_df[grouped_final_df['item_code'] == item_code]
            
            # Write the filtered dataframe to a new sheet named after the item_code
            df_item_code.to_excel(writer, sheet_name=str(item_code), index=False)

            # Access the xlsxwriter workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[str(item_code)]

            # Add some formatting
            format_header = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#4F81BD', 'border': 1})
            format_cell = workbook.add_format({'border': 1})

            # Apply the header format
            for col_num, value in enumerate(df_item_code.columns.values):
                worksheet.write(0, col_num, value, format_header)

            for row_num in range(1, len(df_item_code) + 1):
                for col_num in range(len(df_item_code.columns)):
                    worksheet.write(row_num, col_num, df_item_code.iloc[row_num - 1, col_num], format_cell)

            for col_num in range(len(df_item_code.columns)):
                max_len = df_item_code[df_item_code.columns[col_num]].astype(str).map(len).max()
                worksheet.set_column(col_num, col_num, max_len + 2)
    
    return send_file(file_path, as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    item_names = []
    certificate_content = None
    shipping_content = None
    if request.method == 'POST':
        name = request.form.get('name', '')
        if name.strip():
            so_df = retrieve_data(name)
            if so_df is not None:
                item_names = so_df['item_name'].unique().tolist()
                if 'print_certificate' in request.form:
                    selected_item_name = request.form.get('selected_item_name', '')
                    if selected_item_name:
                        selected_row = so_df[so_df['item_name'] == selected_item_name].iloc[0]
                        item_code = selected_row['item_code']
                        serial_no = selected_row['serial_no']
                        qty = selected_row['qty']
                        territory = selected_row['territory']
                        customer = selected_row['customer']
                        certificate_content = render_template('certificate.html', item_name=selected_item_name,
                                                              item_code=item_code,
                                                              serial_no=serial_no, qty=qty, territory=territory,
                                                              customer=customer)
                    else:
                        certificate_content = 'Item name is required to print the certificate.'
                elif 'print_shipping_list' in request.form:
                    shipping_content = render_template('shipping_list.html', items=so_df.to_dict(orient='records'))

                elif 'print_ci' in request.form:
                    shipping_content = render_template('commercial_invoice.html', items=so_df.to_dict(orient='records'))

                elif 'print_pl' in request.form:
                    shipping_content = render_template('packing_list.html', items=so_df.to_dict(orient='records'))

                elif 'print_dgr' in request.form:
                    shipping_content = render_template('non_dgr.html', items=so_df.to_dict(orient='records'))

                elif 'print_scomet' in request.form:
                    shipping_content = render_template('non_scomet.html', items=so_df.to_dict(orient='records'))

                return render_template('index.html', item_names=item_names, certificate_content=certificate_content,
                                       shipping_content=shipping_content, name=name)
            else:
                return f'Request failed to retrieve data for {name}.'
        else:
            return 'Name field is required.'

    return render_template('index.html', item_names=item_names, certificate_content=certificate_content)


@app.route('/print_certificate', methods=['POST'])
def print_certificate():
    selected_item_name = request.form.get('selected_item_name', '')
    name = request.form.get('name', '')
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list
    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()
        if selected_item_name:
            selected_row = so_df[so_df['item_name'] == selected_item_name].iloc[0]
            item_code = selected_row['item_code']
            serial_no = selected_row['serial_no']
            qty = selected_row['qty']
            territory = selected_row['territory']
            customer = selected_row['customer']

            certificate_content = render_template('certificate.html', item_name=selected_item_name, item_code=item_code,
                                                  serial_no=serial_no, qty=qty, territory=territory, customer=customer)
            return render_template('index.html', item_names=item_names, certificate_content=certificate_content,
                                   name=name)
        else:
            return 'Item name is required to print the certificate.'
    else:
        return f'Request failed to retrieve data for {name}.'



@app.route('/print_sticker', methods=['POST'])
def print_sticker():
    selected_item_name = request.form.get('selected_item_name', '')
    name = request.form.get('name', '')
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list
    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()
        if selected_item_name:
            selected_row = so_df[so_df['item_name'] == selected_item_name].iloc[0]
            item_code = selected_row['item_code']
            serial_no = selected_row['serial_no']
            qty = selected_row['qty']
            territory = selected_row['territory']
            customer = selected_row['customer']
            po_no = selected_row['po_no']
            sales_order = selected_row['name']

            certificate_content = render_template('sticker.html', item_name=selected_item_name, item_code=item_code,
                                                  serial_no=serial_no, qty=qty, territory=territory, customer=customer,po_no = po_no,sales_order = sales_order)
            return render_template('index.html', item_names=item_names, certificate_content=certificate_content,
                                   name=name)
        else:
            return 'Item name is required to print the certificate.'
    else:
        return f'Request failed to retrieve data for {name}.'





@app.route('/print_ci', methods=['POST'])
def print_commercial_invoice():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)

    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        sale_charges = sale_charges.drop_duplicates()
        sale_charges = sale_charges.sort_values(by='total', ascending=True)
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')

        unique_currency = so_df['currency'].unique().tolist()
        # Pass the first customer name to the template
        currency = unique_currency[0] if unique_currency else ""

        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term  = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_freight_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""




        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""

        ci_content = render_template('commercial_invoice.html', items=items, currency=currency,charges= charges,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges)

        return render_template('index.html', item_names=item_names, ci_content=ci_content, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'


@app.route('/print_si', methods=['POST'])
def print_shipping_list():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        sale_charges = sale_charges.sort_values(by='total', ascending=True)
        sale_charges = sale_charges.drop_duplicates()
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')

        unique_currency = so_df['currency'].unique().tolist()
        # Pass the first customer name to the template
        currency = unique_currency[0] if unique_currency else ""


        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_payment_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""



        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""

        unique_hsn_code = so_df['gst_hsn_code'].unique().tolist()
        # Pass the first hsn_code to the template
        hsn_code = "<br>".join(unique_hsn_code) if unique_hsn_code else " "



        si_content = render_template('shipping_list.html', charges= charges,items=items, currency=currency,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges,hsn_code=hsn_code)

        return render_template('index.html', item_names=item_names, shipping_content=si_content, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'



@app.route('/packing_list', methods=['POST'])
def packing_list_spares():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')
        currency = so_df['currency']  # Assuming you have a currency variable


        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_payment_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""



        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""



        pl_content = render_template('packing_list.html', items=items, currency=currency,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges)

        return render_template('index.html', item_names=item_names, pl_content=pl_content, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'




@app.route('/packing_list_spares', methods=['POST'])
def packing_list():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')
        currency = so_df['currency']  # Assuming you have a currency variable

        unique_name = so_df['name'].unique().tolist()
        # Pass the first customer name to the template
        sales_order = unique_name[0] if unique_name else ""

        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_payment_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""

        current_date = datetime.now().strftime("%d-%m-%Y")

        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""

        unique_salesorder = so_df['name'].unique().tolist()
        # Pass the first customer name to the template
        sales_order = unique_salesorder[0] if unique_salesorder else ""


        pl_content_spares = render_template('packing_list_spares.html', items=items, currency=currency,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges,current_date=current_date,sales_order=sales_order)

        return render_template('index.html', item_names=item_names, pl_content_spares=pl_content_spares, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'


@app.route('/non_dgr', methods=['POST'])
def non_dgr():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')
        currency = so_df['currency']  # Assuming you have a currency variable



        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_payment_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""



        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""



        nondgr_content = render_template('non_dgr.html', items=items, currency=currency,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges)

        return render_template('index.html', item_names=item_names, nondgr_content=nondgr_content, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'


@app.route('/scomet_page', methods=['POST'])
def scomet():
    # Get shipping address from form data
    name = request.form.get('name', '')
    # Get shipping address from form data
    so_df = retrieve_data(name)
    item_names = []  # Initialize item_names as empty list

    if so_df is not None:
        item_names = so_df['item_name'].unique().tolist()

        sale_charges = so_df[["name", "account_head", "tax_amount", "total"]]
        so_df = so_df[
            ["name", "customer", "item_code", "item_name", "serial_no", "item_name", "territory", "qty",
             "address_display",
             "shipping_address", "shipping_address_name", "po_no", "po_date", "freight_term", "payment_terms_template",
             "currency", "rate", "amount", "freight_amt", "packing_charges", "total_net_weight", "gst_hsn_code", "uom",
             "total_net_weight", "net_total"]]

        # Drop duplicate rows
        so_df = so_df.drop_duplicates()
        items = so_df.to_dict(orient='records')
        charges = sale_charges.to_dict(orient='records')
        currency = so_df['currency']  # Assuming you have a currency variable


        unique_shipname = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address_name = unique_shipname[0] if unique_shipname else ""

        unique_customers = so_df['customer'].unique().tolist()
        # Pass the first customer name to the template
        customer = unique_customers[0] if unique_customers else ""

        unique_shipping = so_df['shipping_address'].unique().tolist()
        # Pass the first customer name to the template
        shipping_address = "<br>".join(unique_shipping) if unique_shipping else ""

        unique_address = so_df['address_display'].unique().tolist()
        # Pass the first customer name to the template
        customer_address = "<br>".join(unique_address) if unique_address else ""

        unique_payment_term = so_df['payment_terms_template'].unique().tolist()
        unique_payment_term = [str(term) for term in unique_payment_term]
        # Pass the first customer name to the template
        payment_terms_template = "<br>".join(unique_payment_term) if unique_payment_term else ""

        unique_freight_term = so_df['freight_term'].unique().tolist()
        # Pass the first customer name to the template
        freight_term = "<br>".join(unique_freight_term) if unique_payment_term else ""

        unique_po_no = so_df['po_no'].unique().tolist()
        # Pass the first customer name to the template
        po_no = "<br>".join(unique_po_no) if unique_po_no else ""

        unique_territory = so_df['territory'].unique().tolist()
        # Pass the first customer name to the template
        territory = "<br>".join(unique_territory) if unique_territory else ""



        unique_packing_charges = so_df['packing_charges'].unique().tolist()
        # Pass the first customer name to the template
        packing_charges = "<br>".join(unique_packing_charges) if unique_packing_charges else ""



        scomet_content = render_template('non_scomet.html', items=items, currency=currency,
                                     customer=customer, shipping_address=shipping_address,
                                     customer_address=customer_address, shipping_address_name=shipping_address_name,po_no= po_no,payment_terms_template = payment_terms_template,freight_term=freight_term,territory=territory,packing_charges = packing_charges)

        return render_template('index.html', item_names=item_names, scomet_content=scomet_content, name=name)
    else:
        return f'Request failed to retrieve data for {name}.'




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
