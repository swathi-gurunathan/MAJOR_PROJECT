1. pip install -r requirements.txt

2. Go to https://platform.openai.com/account/api-keys
    Sign in with your OpenAI account.
    Click "Create new secret key"
    Copy the key and paste it into your .env file under OPEN_API_KEY:

3. Go to the Google Cloud Console:
    https://console.cloud.google.com/
    Create a new project (or use an existing one).
    Navigate to:
    APIs & Services > Credentials
    Click “Create Credentials” → “OAuth Client ID”
    If prompted, configure the OAuth Consent Screen first.
    Choose Application Type → Web Application
    Set name: Autonomous AI App
    Add Authorized redirect URI:
    http://localhost:8000/auth/callback
    (Or your deployed URL)
    Click Create → Copy both:
    Client ID
    Client Secret
    Paste into .env:
    GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
    GOOGLE_CLIENT_SECRET=your-secret-here

4. JWT_SECRET - random string that your FastAPI app uses to sign and verify JWT tokens.