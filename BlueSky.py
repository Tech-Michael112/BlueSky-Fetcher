import requests
import re

class BskyFollower:
    def __init__(self, bearer_token):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; 23106RN0DA Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'authorization': f'Bearer {bearer_token}',
            'atproto-accept-labelers': 'did:plc:ar7c4by46qjdydhdevvrndac;redact',
            'origin': 'https://bsky.app',
            'x-requested-with': 'mark.via.gp',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://bsky.app/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    def get_did(self, username):
        response = self.session.get(f'https://lepista.us-west.host.bsky.network/xrpc/app.bsky.actor.searchActorsTypeahead?q={username}&limit=8', headers=self.headers)
        content_str = response.content.decode('utf-8')
        did_match = re.search(r'"did":"([^"]+)"', content_str)

        if did_match:
            return did_match.group(1)
        else:
            print("DID not found in response content.")
            return None

    def get_all_followers(self, did_value):
        base_url = 'https://lepista.us-west.host.bsky.network/xrpc/app.bsky.graph.getFollowers'
        cursor = None
        all_followers = []

        while True:
            params = {
                'actor': did_value,
                'limit': 30,
            }
            if cursor:
                params['cursor'] = cursor

            response = self.session.get(base_url, headers=self.headers, params=params)
            

            if response.status_code == 200:
                data = response.json()
                followers = data.get('followers', [])
                for follower in followers:
                    handle = follower.get('handle')
                    display_name = follower.get('displayName')
                    print(f"{handle}|{display_name}")
                    all_followers.append(f"{handle}|{display_name}")

                cursor = data.get('cursor')
                print(f"New cursor: {cursor}")  
                if not cursor:
                    break
            else:
                print(f"Failed to get followers: {response.status_code}")
                print(response.text)  
                break

        return all_followers

if __name__ == "__main__":
    username = input('Enter Username: ')
    bearer_token = 'eyJhbGciOiJFUzI1NksifQ.eyJzY29wZSI6ImNvbS5hdHByb3RvLmFjY2VzcyIsInN1YiI6ImRpZDpwbGM6NGhienljZG1jcWZ2YWxxNXVwbnlqd2VpIiwiaWF0IjoxNzE5Njg1MjM5LCJleHAiOjE3MTk2OTI0MzksImF1ZCI6ImRpZDp3ZWI6bGVwaXN0YS51cy13ZXN0Lmhvc3QuYnNreS5uZXR3b3JrIn0.sEhb1hU1lQRhr3qO98qx6TSp3VY6WS3P6NJRS3ZliKEz8edqndqkZTvK7z0v89W1CcXjXXk1GcDoAeQ9Jrl7Lw'
    fetcher = BskyFollower(bearer_token)
    
    did_value = fetcher.get_did(username)
    if did_value:
        all_followers = fetcher.get_all_followers(did_value)
        print("All followers retrieved successfully.")