
import json
from decimal import Decimal
import boto3
from time import gmtime, strftime
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CurrencyConverterTable')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
def lambda_handler(event, context):
    conversion_rate = Decimal('74.85')  
    
    # extract the amount in USD from the Lambda service's event object
    amount_usd = Decimal(str(event['amount_usd']))  
    
    # convert the amount to INR
    amount_inr = amount_usd * conversion_rate

    # write the conversion result and time to the DynamoDB table
    response = table.put_item(
        Item={
            'ID': str(amount_usd) + '_to_INR',
            'AmountInUSD': amount_usd,
            'AmountInINR': amount_inr,
            'ConversionRate': conversion_rate,
            'Timestamp': now
        })

    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps({
            'amount_in_usd': float(amount_usd),
            'amount_in_inr': float(amount_inr),
            'conversion_rate': float(conversion_rate),
            'timestamp': now
        })
    }
