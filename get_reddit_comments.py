import requests

def get_comments(permalink):
    # Replace the `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` placeholders with your own Reddit app's 
    # client ID and client secret, respectively.
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    # Check if the permalink is valid
    if not permalink or not permalink.startswith("r/"):
        return None

    # Construct the Reddit API URL using the permalink
    url = "https://api.reddit.com/{}/comments".format(permalink)

    # Make a request to the Reddit API to get the comments
    response = requests.get(url, auth=(client_id, client_secret))

    # If the request is successful, return the list of comments
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
comments = get_comments("r/funny/comments/5z5v7y/hilarious_dog_gif/")
if comments:
    for comment in comments:
        print(comment["body"])
else:
    print("Invalid permalink or error getting comments.")
