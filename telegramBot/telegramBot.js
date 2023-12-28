const TelegramBot = require('node-telegram-bot-api');
const fetch = require('node-fetch');

// Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the actual token provided by BotFather
const bot = new TelegramBot('6734116635:AAHEXcUqoQQI2i9YEnnaucU0eR813RYyhyw', { polling: true });

// Replace 'YOUR_API_ENDPOINT' with the actual endpoint of your API
const apiEndpoint = 'http://localhost:3001/api/v1/sentiment';

bot.onText(/\/analyze (.+)/, (msg, match) => {
  const chatId = msg.chat.id;
  const text = match[1];
  console.log('Reached point X');

  // Make a request to your API
  fetch(apiEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
    .then((response) => response.json())
    .then((result) => {

      // Send the result back to the user
      bot.sendMessage(chatId, JSON.stringify(result, null, 2));
    })
    .catch((error) => {
      console.error('Error calling API:', error);
      bot.sendMessage(chatId, 'An error occurred while calling the API.');
    });
});

console.log('Telegram bot is running...');
