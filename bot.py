import json
import base64
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Step 1: Gather product information
product_data = {}


# Function to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! To add a product, type /addproduct")


# Function to add product
async def add_product(update: Update, context: CallbackContext):
    await update.message.reply_text("Please provide the product name:")
    context.user_data['state'] = 'waiting_for_name'


# Function to capture user input for product details
async def handle_message(update: Update, context: CallbackContext):
    state = context.user_data.get('state')

    if state == 'waiting_for_name':
        product_data['name'] = update.message.text
        await update.message.reply_text("Now provide a description for the product:")
        context.user_data['state'] = 'waiting_for_description'

    elif state == 'waiting_for_description':
        product_data['description'] = update.message.text
        await update.message.reply_text("Provide a category for the product:")
        context.user_data['state'] = 'waiting_for_category'

    elif state == 'waiting_for_category':
        product_data['category'] = update.message.text
        await update.message.reply_text("Provide a price for the product:")
        context.user_data['state'] = 'waiting_for_price'

    elif state == 'waiting_for_price':
        product_data['price'] = update.message.text
        await update.message.reply_text("Finally, provide an image URL for the product:")
        context.user_data['state'] = 'waiting_for_image_url'

    elif state == 'waiting_for_image_url':
        product_data['image_url'] = update.message.text
        await update.message.reply_text("Thank you! Adding product to the web page...")
        context.user_data['state'] = None

        # Call function to update the JSON file on GitHub
        add_product_to_github(product_data)
        await update.message.reply_text("Product added successfully!")


# Step 3: Function to add product to the GitHub JSON file
def add_product_to_github(product):
    github_repo = 'NurbArys/Sales-Garage'
    github_token = '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'
    products_file_url = f'https://api.github.com/repos/{github_repo}/contents/products.json'

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Get current content of products.json
    response = requests.get(products_file_url, headers=headers)
    
    if response.status_code == 200:
        # If successful, proceed with updating the file
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        current_products = json.loads(content)

        # Update the JSON
        current_products.append(product)

        # Prepare new content, encoded as Base64
        updated_content = json.dumps(current_products, indent=4)
        base64_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')

        commit_message = {
            "message": "Add new product",
            "content": base64_content,
            "sha": response.json()['sha']
        }

        # Commit the new changes
        commit_response = requests.put(products_file_url, json=commit_message, headers=headers)
        
        if commit_response.status_code == 200:
            print("Product successfully added to GitHub.")
        else:
            print(f"Failed to commit changes. Status Code: {commit_response.status_code}, Response: {commit_response.json()}")
    
    elif response.status_code == 404:
        # If the file does not exist, create the products.json file
        print("The file products.json does not exist. Creating a new one.")
        new_content = json.dumps([product], indent=4)
        base64_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

        commit_message = {
            "message": "Create products.json with the first product",
            "content": base64_content
        }

        create_response = requests.put(products_file_url, json=commit_message, headers=headers)

        if create_response.status_code == 201:
            print("products.json file created successfully.")
        else:
            print(f"Failed to create products.json. Status Code: {create_response.status_code}, Response: {create_response.json()}")
    
    else:
        # Print error details for easier debugging
        print(f"Failed to retrieve products.json from GitHub. Status Code: {response.status_code}, Response: {response.json()}")


# Step 4: Main function to set up the bot
def main():
    application = Application.builder().token('7235348489:AAFWVKKPCMbwE-vkTIO2h1l62w3FDjgF7HU').build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('addproduct', add_product))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    application.run_polling()


if __name__ == '__main__':
    main()
