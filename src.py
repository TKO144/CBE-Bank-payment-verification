import pytesseract
from PIL import Image
import requests

def extract_transaction_id(image_path, id_prefix="TxnID:"):

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        for line in text.split("\n"):
            if id_prefix in line:
                return line.split(id_prefix)[-1].strip()
        return None
    except Exception as e:
        return f"Error extracting transaction ID: {e}"

def verify_transaction(transaction_id, verification_url):
    
    try:
        response = requests.get(f"{verification_url}?transaction_id={transaction_id}")
        if response.status_code == 200:
            return response.json().get("status") == "success"
        return False
    except Exception as e:
        return f"Error verifying transaction: {e}"

def check_payment(image_path, verification_url):
   
    print("Extracting transaction ID...")
    transaction_id = extract_transaction_id(image_path)
    
    if not transaction_id:
        return "Transaction ID not found in the image."

    print(f"Transaction ID found: {transaction_id}")
    print("Verifying transaction...")
    
    is_valid = verify_transaction(transaction_id, verification_url)
    
    return "Payment is valid." if is_valid else "Payment verification failed."

# Example usage
#if __name__ == "__main__":
 #   screenshot_path = "uploaded_screenshot.png"  # Replace with the actual path
  #  verification_link = "https://example.com/verify_payment"  # Replace with the actual URL
    
   # result = check_payment(screenshot_path, verification_link)
    print(result)
