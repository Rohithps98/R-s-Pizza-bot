## R's Pizza bot

I built a chatbot the 'R's Pizza Bot' where a user can login and enter the location and the bot gives the top pizza 
restaurants at that location. 

If the inputs from the user matches with the intents then the bot asks for the location of the user and returns the weather condition at that location, and suggests top 5 pizza restaurants at that location.
I used Weather api to extract weather information at particular location and zomato api to extract restaurants in user requested location.\

#### Setup and installation instructions:
* Please follow the installation instructions mentioned in: [Installation instructions](installation-instructions.md)

Once the installation is completed,

It's time to train R's pizza bot. 

For training the bot following command is used, for more information visit: https://rasa.com/docs/rasa/user-guide/command-line-interface/#train-a-model
`rasa train`  

To start the server run following command.
`rasa run`

Time to see the performance of the bot and check for any improvements required.
To initiate the chat run following command in very new tab.
`rasa run actions`

Once the rasa server is up, we need to route the local server to the web using Ngrok.

Install Ngrok, and then run the below command, (5005 is the port at which the rasa server is being hosted)
ngrok http 5005

Now, we need to integrate the application with slack

Go to slack developer portal and create an Application.

Once the application is created, head over to OAuth & Permissions and scroll down to Scopes. Scopes give your app permission to do things in your workspace.

To get started, you should at least add the following scopes:

app_mentions:read,
channels:history,
chat:write,
groups:history,
im:history,
mpim:history and
reactions:write.

On the OAuth & Permissions page, click Install App to Workspace to add the bot to your workspace.

Once added, Slack will show you a Bot User OAuth Access Token which you'll need to add to your credentials.yml as the value for slack_token:

Then copy the signing secret in basic information and paste it in credentials.yml as signing secret

Now to receive messages:

To send messages directly to your bot using the slack UI, head to App Home, scroll to the bottom and select the checkbox for Allow users to send Slash commands and messages from the messages tab.

You might have to quit the Slack app and re-open it before your changes take effect.

Configure the webhook by heading to Event Subscriptions and turning Enable Events on.

As a request URL enter the public url of your bot and append /webhooks/slack/webhook, e.g. https://<host>/webhooks/slack/webhook replacing <host> with your URL. If you are using ngrok, your url should look like https://92832de0.ngrok.io/webhooks/slack/webhook.

You won't be able to use a localhost url.

As a last step, you'll need to Subscribe to bot events on the same page. You'll need to add the following events:

message.channels,
message.groups,
message.im and
message.mpim.

For more information visit: https://rasa.com/docs/rasa/connectors/slack/

Now, Start the RASA Server using the `rasa run` command.

Now, you're good to go!