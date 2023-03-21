import requests
from PIL import Image
import io
from imgurpython import ImgurClient
import pyperclip

# Define a function to send requests to the DALL-E API
def generate_image_from_prompt(prompt, api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'model': 'image-alpha-001',
        'prompt': prompt,
        'num_images': 1,
        'size': '256x256',
    }

    response = requests.post('https://api.openai.com/v1/images/generations', json=data, headers=headers)
    response.raise_for_status()

    image_url = response.json()['data'][0]['url']
    image_data = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_data))

    return image, image_url

# Define a function to upload an image to Imgur
def upload_to_imgur(client_id, client_secret, access_token, refresh_token, image_path):
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    image = client.upload_from_path(image_path)
    return image['link']

# Prompt the user for input and generate an image
def main():
    api_key = 'YOUR_OPENAI_API_KEY'
    client_id = 'APP_IMGUR_CLIENT_ID'
    client_secret = 'APP_IMGUR_CLIENT_SECRET'
    access_token = 'IMGUR_ACCESS_TOKEN'
    refresh_token = 'IMGUR_REFRESH_TOKEN'

    # Prompt the user for input
    prompt = input('Enter a prompt: ')

    # Generate the image
    try:
        image, image_url = generate_image_from_prompt(prompt, api_key)
    except requests.exceptions.HTTPError as e:
        print(f'Error generating image: {e}')
        return

    # Save the generated image
    image_path = 'generated_image.jpg'
    image.save(image_path)

    # Upload the image to Imgur
    try:
        imgur_link = upload_to_imgur(client_id, client_secret, access_token, refresh_token, image_path)
    except requests.exceptions.HTTPError as e:
        print(f'Error uploading image to Imgur: {e}')
        return

    # Copy the Imgur link to the clipboard
    pyperclip.copy(imgur_link)
    print(f'Image uploaded to Imgur: {imgur_link} (link copied to clipboard)')

    # Display the generated image
    image.show()

if __name__ == '__main__':
    main()
