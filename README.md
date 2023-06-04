# Flask For Google Calendar (ffgl)

## Description

`ffgl` is a simple web application that uses the Flask web framework to interact with Google Calendar API. This application provides basic OAuth2 flow and lets users view their upcoming Google Calendar events.

## Features

- OAuth2 Authorization with Google
- Retrieves and displays the next 10 events from the primary Google Calendar
- Session management with Flask sessions

## Installation

To install the application, follow these steps:

1. Clone this repository to your local machine:
```bash
git clone https://github.com/przadka/ffgl.git
```
2. Go to the directory:
```bash
cd ffgl
```
3. Install the requirements using pip:
```bash
pip install -r requirements.txt
```

## Usage

Before running the application, you need to set up your Google Client ID and Client Secret:

1. Go to the Google Developer Console (https://console.developers.google.com/)
2. Create a new project
3. Enable the Google Calendar API for your project
4. Create credentials for a Web application and set the redirect URI to `http://localhost:8080/oauth2callback`
5. Save the Client ID and Client Secret

Create a `.env` file in the project root and add your Client ID, Client Secret and a secret key to secure your client-side session:

```
CLIENT_ID=<your-client-id>
CLIENT_SECRET=<your-client-secret>
SECRET_KEY=<a-random-string>
```

To run the application using Flask development server:

```bash
python main.py
```

To run the application using Nox, ensure you have Nox installed (you can install it with `pip install nox`). Then simply run:

```bash
nox
```

Visit http://localhost:8080 in your web browser, and you'll be greeted with a page that has a link to begin the authorization process. Once authorization is complete, you'll be able to see the next 10 events from your primary Google Calendar.

## License

This project is licensed under [MIT License](LICENSE).