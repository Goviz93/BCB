import requests
from datetime import datetime


def get_current_date(location="UTC"):
    try:
        response = requests.get(f"http://worldtimeapi.org/api/timezone/{location}")
        data = response.json()

        current_date = data['datetime'].split('T')[0]  # Extract only the date part
        return current_date

    except requests.RequestException as e:
        return f"Error: {e}"


def validate_date_with_worldtimeapi(limit_date):
    try:
        # Get the current date using WorldTimeAPI
        current_date = get_current_date()

        # Parse the limit date string to a datetime object
        limit_datetime = datetime.strptime(limit_date, "%Y-%m-%d")

        # Compare the current date with the limit date
        if current_date > limit_datetime.strftime("%Y-%m-%d"):
            print(f"Por favor renueva tu licencia, la fecha limite fue: ({limit_date}).")
            return False
        else:
            print(f"La fecha de expiración es: ({limit_date}).")
            return True

    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Specify the limit date in the format YYYY-MM-DD
    limit_date = "2023-01-01"

    # Validate the current date against the limit date using WorldTimeAPI
    validate_date_with_worldtimeapi(limit_date)

