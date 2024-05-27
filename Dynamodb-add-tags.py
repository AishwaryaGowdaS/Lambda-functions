import boto3

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb_client = boto3.client('dynamodb')
    
    try:
        # List all DynamoDB tables
        tables = []

        # Paginate through DynamoDB tables
        paginator = dynamodb_client.get_paginator('list_tables')
        for page in paginator.paginate():
            tables.extend(page['TableNames'])

        print("DynamoDB tables:", tables)
        print("Number of DynamoDB tables:", len(tables))
        for table_name in tables:
            # Add tag with the same name as the table to each table
            tags = [{'Key': 'Name', 'Value': table_name}]
            table_arn = f'arn:aws:dynamodb:{boto3.Session().region_name}:{boto3.client("sts").get_caller_identity()["Account"]}:table/{table_name}'
            dynamodb_client.tag_resource(ResourceArn=table_arn, Tags=tags)
            print(f"Added tag 'Name={table_name}' to DynamoDB table '{table_name}'.")

        print("Tags added to all DynamoDB tables successfully.")

        # If you want to print each table name individually, uncomment the following loop
        # for table_name in tables:
        #     print("Table name:", table_name)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    lambda_handler(None, None)
