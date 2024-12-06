import pytesseract
from PIL import Image
import requests
from pdfminer.high_level import extract_text
from pyzbar.pyzbar import decode

verification_url = https://apps.cbe.com.et:100/?id=

def extract_transaction_details(image_path, id_prefix="TxnID:", amount_prefix="Amount:"):
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        transaction_id = None
        amount = None

        for line in text.split("\n"):
            if id_prefix in line:
                transaction_id = line.split(id_prefix)[-1].strip()
            if amount_prefix in line:
                amount = line.split(amount_prefix)[-1].strip()

        # Attempt to scan for QR codes
        qr_codes = decode(image)
        for qr in qr_codes:
            qr_data = qr.data.decode('utf-8')
            print("QR Code Data:", qr_data)

        return transaction_id, amount
    except Exception as e:
        return None, None

def download_pdf(verification_url, transaction_id):
    
    try:
        # Append transaction ID to the URL
        full_url = f"{verification_url}?transaction_id={transaction_id}"
        response = requests.get(full_url)
        if response.status_code == 200:
            pdf_path = "receipt.pdf"
            with open(pdf_path, "wb") as f:
                f.write(response.content)
            return pdf_path
        return None
    except Exception as e:
        return None

def extract_amount_from_pdf(pdf_path, amount_prefix="Amount:"):
    
    try:
        text = extract_text(pdf_path)
        for line in text.split("\n"):
            if amount_prefix in line:
                return line.split(amount_prefix)[-1].strip()
        return None
    except Exception as e:
        return None

def verify_deposit(screenshot_path, verification_url):
    
    print("Extracting transaction details from screenshot...")
    transaction_id, screenshot_amount = extract_transaction_details(screenshot_path)

    if not transaction_id or not screenshot_amount:
        return "Transaction ID or amount not found in the screenshot."

    print(f"Transaction ID: {transaction_id}, Amount: {screenshot_amount}")

    print("Downloading receipt PDF...")
    pdf_path = download_pdf(verification_url, transaction_id)

    if not pdf_path:
        return "Failed to download the receipt PDF."

    print("Extracting amount from PDF...")
    pdf_amount = extract_amount_from_pdf(pdf_path)

    if not pdf_amount:
        return "Amount not found in the receipt PDF."

    print(f"Screenshot Amount: {screenshot_amount}, PDF Amount: {pdf_amount}")

    if screenshot_amount == pdf_amount:
        return "Payment is valid."
    return "Payment verification failed."

# Example usage
#if __name__ == "__main__":
 #   screenshot_path = "uploaded_screenshot.png"  # Replace with the actual screenshot path
  #  verification_link = "https://example.com/download_receipt"  # Replace with the actual base URL
    
   # result = verify_deposit(screenshot_path, verification_link)
    #print(result)
