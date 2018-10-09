from botocore.vendored import requests
from lxml import html
import json

def lambda_handler(event, context):

    try:
        platform = event['pathParameters']['platform']
        username = event['pathParameters']['username']
        result = web_scrape(platform, username)
        res = {
            'data' : result,
            'userInfo' : {
                'platform' : platform,
                'username' : username
            }
        }
        res = json.dumps(res)
        return {
            'statusCode' : 200,
            'body' : res
        }
    except Exception as e:
        print(e)
        return {
            'statusCode' : 400,
            'body' : json.dumps({'error': 'Something went wrong!'})
        }

    
def web_scrape(platform, username):
    res = {}
    page = requests.get('https://playoverwatch.com/en-us/career/' + platform + '/' + username)
    tree = html.fromstring(page.content)
    
    no_profile = tree.xpath("//h1[@class='u-align-center']/text()")
    private_profile = tree.xpath("//h3[@class='h4']/text()")
    if(no_profile):
        res['error'] = "Profile does not exist (Make sure you include the ID of your username. e.x.: " + username + "-12345)"
    elif(private_profile):
        res['error'] = "Profile is private. Overwatch defaults profiles to private. To make it public, in game go to Settings > Social > Set career profile to public. Exit game for changes to be made"
    else:
        titles = tree.xpath("//div[@data-group-id='stats'][1]//div//div[@class='card-stat-block']//table[@class='data-table']//tbody//tr//td[1]/text()")
        values = tree.xpath("//div[@data-group-id='stats'][1]//div//div[@class='card-stat-block']//table[@class='data-table'][1]//tbody//tr//td[2]/text()")
        print("Title", titles)
        print("Values", values)

        for i in range(0, len(titles)):
            res[titles[i]] = values[i]
    
    return res

