import requests
import re
import sys

import json

"""
Go to blue sky.com to understand more of the web system
code was modified and written by Michael
its used to extract data to the last cursor list for followers list
thanks for reading"""



class BskyFollower:
    def __init__(self, bearer_token, file_path):
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
        #self.file=name_file
        self.file_path = file_path

    def get_did(self, username):
        response = self.session.get(f'https://lepista.us-west.host.bsky.network/xrpc/app.bsky.actor.searchActorsTypeahead?q={username}&limit=8', headers=self.headers) #.content 
        cnt_Str = response.content.decode('utf-8')
        did_match = re.search(r'"did":"([^"]+)"', cnt_Str)

        if did_match:
            return did_match.group(1)
        else:
            print(" not found in response content \n something went wrong.")
            deff_non =None
            return deff_non

    def get_all_followers(self, did_value):
        base_url = 'https://lepista.us-west.host.bsky.network/xrpc/app.bsky.graph.getFollowers'
        cursor = None
        all_followers = []

        while True:
        	case= ""
        
            params = {
                'actor': did_value,
                'limit': case,
            }
            if cursor:
                params['cursor'] = cursor

            response = self.session.get(base_url, headers=self.headers, params=params)

            if response.status_code == 200: #except 404
                data = response.json()
                followers = data.get('followers', [])
                for follower in followers:
                    handle = follower.get('handle')
                    display_name = follower.get('displayName')
                    display=f"{handle}|{display_name}\n"
                    disP=f"{handle}|{display_name}"
                    open(self.file_path,'a').write(display)
                  
                    print(f"{str(len(disP))}-  {disP}")
                    all_followers.append(f"{handle}|{display_name}")

                cursor = data.get('cursor')
                print(f" \033[1;92m Generated Cursor [] {cursor}")  
                if not cursor:
                    break
            else:
                print(f"\033[1;91m Failed to get followers {response.status_code}")
                print("")  
                break

        
        return all_followers

if __name__ == "__main__":
    file_path = input('Enter file path: ')
    username = input('Enter Username: ')
    bearer_token = 'eyJhbGciOiJFUzI1NksifQ.eyJzY29wZSI6ImNvbS5hdHByb3RvLmFjY2VzcyIsInN1YiI6ImRpZDpwbGM6NGhienljZG1jcWZ2YWxxNXVwbnlqd2VpIiwiaWF0IjoxNzE5ODAwODAxLCJleHAiOjE3MTk4MDgwMDEsImF1ZCI6ImRpZDp3ZWI6bGVwaXN0YS51cy13ZXN0Lmhvc3QuYnNreS5uZXR3b3JrIn0.7N6oH66CwfMVdLLtKGUz_zIIFkvuZ7XB23Ip1MCA-AboT6PYRRMNIenra-iz0lNH1ytLKmVq_v_AA3nhs8HQKQ'
    fetcher = BskyFollower(bearer_token,file_path)
    
    did_value = fetcher.get_did(username)
    if did_value:
        all_followers = fetcher.get_all_followers(did_value)
        print("All followers retrieved successfully.")