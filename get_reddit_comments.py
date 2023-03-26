import requests

def get_comments(permalink):
    # Replace the `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` placeholders with your own Reddit app's 
    # client ID and client secret, respectively.
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    # Check if the permalink is valid
    if not permalink or not permalink.startswith("https://www.reddit.com/"):
        return None

    # Extract the post ID and comment ID from the permalink
    permalink_parts = permalink.split("/")
    post_id = permalink_parts[6]
    comment_id = permalink_parts[8]

    # Construct the Reddit API URL using the post ID and comment ID
    url = f"https://api.reddit.com/r/funny/comments/{post_id}/_/{comment_id}"

    # Make a request to the Reddit API to get the comments
    response = requests.get(url, auth=(client_id, client_secret), headers={"User-agent": "Mozilla/5.0"})

    # If the request is successful, return the list of comments
    if response.status_code == 200:
        comments = response.json()[1]["data"]["children"]
        return [flatten_comment(comment) for comment in comments]
    else:
        return None

def flatten_comment(comment):
    comment_data = comment["data"]
    flattened_comment = {"author": comment_data["author"],
                         "body": comment_data["body"],
                         "created_date": comment_data["created_utc"],
                         "replies": []}
    if "replies" in comment_data:
        replies = comment_data["replies"]["data"]["children"]
        flattened_comment["replies"] = [flatten_comment(reply) for reply in replies]
    return flattened_comment

if __name__ == "__main__":
    # prompt the user to enter a Reddit permalink
    permalink = input("Enter a Reddit permalink: ")

    # call the get_comments function to get the comments for the given permalink
    comments = get_comments(permalink)

    if comments:
        # flatten the comments and print them out
        flattened_comments = [flatten_comments(comment) for comment in comments]
        for comment in flattened_comments:
            print(comment)
    else:
        print("Invalid permalink or unable to retrieve comments.")
