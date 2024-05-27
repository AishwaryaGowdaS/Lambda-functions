import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Initialize table count
    total_table_count = 0

    # Retrieve all table names
    response = dynamodb.list_tables()

    # Retrieve the first set of table names
    table_names = response['TableNames']
    total_table_count += len(table_names)

    # Check if there are more tables available
    while 'LastEvaluatedTableName' in response:
        # Continue retrieving tables with the last evaluated table name as the marker
        response = dynamodb.list_tables(ExclusiveStartTableName=response['LastEvaluatedTableName'])
        table_names.extend(response['TableNames'])
        total_table_count += len(response['TableNames'])

    # Print the total table count
    print("Total number of tables:", total_table_count)
    print(json.dumps(response))  # Print response in JSON format

    # Filter tables containing the word "restored"
    restored_tables = [table_name for table_name in table_names if 'restored' in table_name]

    # Print the total number of tables containing the word "restored"
    print("Total number of restored tables:", len(restored_tables))

    # Print the list of restored tables
    print("Restored tables:")
    for table_name in restored_tables:
        print(table_name)

    # Delete the restored tables
    for table_name in restored_tables:
        dynamodb.delete_table(TableName=table_name)
        print("Deleted table:", table_name)
