# Import relevant libraries
import pandas as pd
import duckdb as db

# Define a function to extract data from a CSV file
def extract_data(file_path):
    try:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_path)

        # Print information about the data
        print(f"Here's some information about the data stored in {file_path}:")
        print(f"\nThere are {data.shape[0]} rows and {data.shape[1]} columns in the DataFrame.")
        print(f"\nThe columns in the DataFrame have the following types: ")
        print(data.dtypes)
        print(f"\nTo view the DataFrame extracted from {file_path}, display the value returned by this function!\n\n")
    except FileNotFoundError as e:
        # Handle file not found error
        print(f"Error: {e}")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None
    return data

# Define a function to clean the data
def clean_data(df_data):
    # Remove duplicate rows
    data = df_data.drop_duplicates()
    
    # Replace missing values in numeric columns with the mean
    data = data.fillna(data.mean(numeric_only=True))
    
    # Drop rows with any remaining null values
    data = data.dropna()
    return data

# Define a function to merge cleaned data
def merge_data(clean_customers_data, clean_orders_data, clean_products_data):
    try:
        # Merge orders and products DataFrames
        products_orders_data = pd.merge(clean_orders_data, clean_products_data, on='product_id')
        
        # Calculate the total price for each order
        products_orders_data['total_price'] = products_orders_data['quantity'] * products_orders_data['price']
        
        # Merge the resulting DataFrame with the customers DataFrame
        ecommerce_data = pd.merge(products_orders_data, clean_customers_data, on='customer_id')
        
        # Save the merged DataFrame to a CSV file
        ecommerce_data.to_csv("ecommerce_data.csv")
        
        # Print information about the merged DataFrame
        print(f"The transformed DataFrame, which includes {ecommerce_data.shape[0]} rows and {ecommerce_data.shape[1]} columns, has been persisted, and will now be returned\n")
    except FileNotFoundError as e:
        # Handle file not found error
        print(f"Error: {e}")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None
    return ecommerce_data

# Define a function to load data into DuckDB
def load_data(db_data, database_name, table_name):
    # Create a connection to the DuckDB database
    con = db.connect(database_name)
    
    # Write the data to the specified table in the database
    db_data.to_sql(name=table_name, con=con, if_exists="replace", index=False)
    print("Original DataFrame has been loaded to DuckDB\n")
    
    # Read the data from the database for validation
    from_db = pd.read_sql(sql=f"SELECT * FROM {table_name}", con=con)
    print("The loaded DataFrame has been read from DuckDB for validation\n")
    
    try:
        # Validate that the data was loaded correctly
        assert db_data.shape == from_db.shape
        print(f"Success! The data in the {table_name} table has successfully been loaded and validated")
    except AssertionError:
        print("DataFrame shape is not consistent before and after loading. Take a closer look!")
    
    return from_db

# Define a function to run the entire data pipeline
def run_pipeline():
    # Define the file paths for the input data
    customers = './data/customers.csv'
    orders = './data/orders.csv'
    products = './data/products.csv'
    
    # Step 1: Extract data from CSV files
    customers_data = extract_data(customers)
    orders_data = extract_data(orders)
    products_data = extract_data(products)
    
    # Step 2: Clean the extracted data
    clean_customers_data = clean_data(customers_data)
    clean_orders_data = clean_data(orders_data)
    clean_products_data = clean_data(products_data)
    
    # Step 3: Merge the cleaned data to create the final DataFrame
    final_data = merge_data(clean_customers_data, clean_orders_data, clean_products_data)
    
    # Step 4: Load the final DataFrame into DuckDB
    queried_data = load_data(db_data=final_data, database_name='ecommerce.db', table_name='ecommerce_data')
    
    return queried_data

# Run the data pipeline if the script is executed directly
if __name__ == "__main__":
    run_pipeline()
