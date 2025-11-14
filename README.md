# chatalytics
Creates analytics and summaries from twitch chats.

## Installation
Download zip and install required python packages in requirements.txt

```bash
pip install -r requirements.txt
```

## Setup
1. Create an application in your [Twitch Dev Console](https://dev.twitch.tv/console)
    1. Click Register Your Application
    2. Add http://localhost:17563 to the OAth Redirect URL (to run locally)
    3. Choose a category
   4. Chose confidential
   5. Click create
2. Generate client secret for application
   1. Click manage on your application
   2. Click New Secret
   3. Copy secret value produced
3. Save client and id to environment variables (same name as below)
   1. TWITCH_APP_ID: <app_id_value>
   2. TWITCH_APP_SECRET: <app_secret_value>

## Usage
Change BROADCASTER variable in main.py to user of channel you want to activate script on.
<br />
Change LISTENER variably in main.py to name of twitch account with the application you created.

Run main file to start script. The first time you run it, you will be asked to authorize the application through Twitch.
```bash
python __main__.py
```

When you want to finish collecting data and show the summary, type "exit"
```bash
exit
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
