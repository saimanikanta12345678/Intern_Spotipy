let userMessages = [];
const chatContainer = document.getElementById("chat-messages");
const userMessageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

function appendMessage(role, content) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");

  if (role === "user") {
    messageElement.classList.add("user-message");
    messageElement.innerHTML = `
      <img src="https://w7.pngwing.com/pngs/81/570/png-transparent-profile-logo-computer-icons-user-user-blue-heroes-logo-thumbnail.png" alt="user icon">
      <span>${content}</span>
    `;
  } else if (role === "bot") {
    messageElement.classList.add("bot-message");
    messageElement.innerHTML = `
      <img src="https://m.media-amazon.com/images/I/61HmveTPTsL.jpg" alt="bot icon">
      <span>${content}</span>
    `;
  }

  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function() {
  var form = document.getElementById("message-form");
  var input = document.getElementById("message-input");
  var messages = document.getElementById("chat-messages");

  form.addEventListener("submit", function(e) {
    e.preventDefault();
    var message = input.value;
    if (message.trim() !== "") {
      appendMessage("user", message);
      userMessages.push(message);
      input.value = "";
// console.log(userMessages);
      // Scroll to the bottom of the chat-messages div
      messages.scrollTop = messages.scrollHeight;

      // Send the user message to the server and receive a bot response
      sendUserMessage(message);
    }
  });
});

async function sendUserMessage(message) {
  // Send the user message to the server
  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content: message })
  });

  if (response.ok) {
    const data = await response.json();
    const botMessage = data.message;
    appendMessage("bot", botMessage);
  }
}

document.getElementById('end-chat-button').addEventListener('click', function() {
  endChat();
});

document.getElementById("chat-form").addEventListener("submit", function(e) {
  e.preventDefault();
  sendMessage();
});

function sendMessage() {
  const userMessage = userMessageInput.value;
  if (userMessage.trim() === "") {
    return;
  }

  appendMessage("user", userMessage);
  userMessages.push(userMessage);
  userMessageInput.value = "";
  userMessageInput.focus();

  // Send the user message to the server and receive a bot response
  sendUserMessage(userMessage);
}


// document.getElementById('end-chat-button').addEventListener('click', endChat);

// function endChat() {
//   calculateSentimentRatios(userMessages);
// }


// Remove the existing event listener for the "End Chat" button
// document.getElementById('end-chat-button').removeEventListener('click', endChat);

// Add a new event listener for the "End Chat" button
// document.getElementById('end-chat-button').addEventListener('click', endChat);

// Update the endChat function to handle the chat ending logic
function endChat() {
  // Perform any necessary cleanup or final actions here
  calculateSentimentRatios(userMessages);


// Disable the message input and send button
userMessageInput.disabled = true;
sendButton.disabled = true;
}


function calculateSentiment(sentences, positiveWords, negativeWords, neutralWords) {
  let total = 0;

  sentences.forEach((sentence) => {
    const words = sentence.toLowerCase().split(' ');

    words.forEach((word) => {
      if (positiveWords.includes(word)) {
        total++;
      } else if (negativeWords.includes(word)) {
        total--;
      }
    });
  });

  let sentiment = 'neutral';
  if (total > 2) {
    sentiment = 'extra-positive';
  } else if (total > 0) {
    sentiment = 'positive';
  } else if (total > -1) {
    sentiment = 'mild-negative';
  } else if (total < -1) {
    sentiment = 'negative';
  }
  return sentiment;
}

function calculateSentimentRatios(userMessages) {
  const positiveWords = ['love', 'happy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'fantastic', 'awesome', 'like', 'beautiful', 'best',
    'nice', 'fantastic', 'fun', 'enjoy', 'sweet', 'perfect', 'superb', 'incredible', 'cool', 'outstanding', 'fantastic', 'fabulous', 'splendid', 'charming', 'delightful', 'lovely', 'marvelous',
    'impressive', 'optimistic', 'enchanting', 'refreshing', 'brilliant', 'extraordinary', 'remarkable', 'heartwarming', 'genius', 'genius', 'innovative',
    'exceptional', 'genius', 'generous', 'phenomenal', 'breathtaking', 'admirable', 'captivating', 'cherished', 'enthusiastic', 'blissful', 'victorious', 'vibrant', 'harmonious',
    'radiant', 'honorable', 'authentic', 'illustrious', 'benevolent', 'respected', 'reputable', 'prestigious', 'diligent', 'noble', 'elegant', 'splendid',
    'exuberant', 'affectionate', 'compassionate', 'grateful', 'thrilled', 'triumphant', 'jolly', 'vivacious', 'loving', 'spirited', 'uplifting',
    'satisfied', 'creative', 'confident', 'optimistic', 'happy', 'positive', 'vibrant', 'charming', 'delightful',
    'radiant', 'glowing', 'inspired', 'hopeful', 'proud', 'content', 'elated', 'grateful', 'joyous', 'passionate', 'warm', 'generous', 'kind', 'friendly', 'supportive'
  ];
  const negativeWords = [
    'hate', 'sad', 'bad', 'terrible', 'awful', 'horrible', 'worst', 'no', 'not', 'never',
    'dislike', 'unhappy', 'disgusting', 'angry', 'annoyed', 'frustrated', 'furious', 'rage',
    'irritated', 'upset', 'depressed', 'miserable', 'sorrow', 'grief', 'unfortunate',
    'unpleasant', 'despair', 'lonely', 'pain', 'dreadful', 'distressed', 'tragic', 'broken',
    'heartbreaking', 'disheartened', 'pessimistic', 'guilty', 'regret', 'shame', 'jealous',
    'disappointed', 'betrayed', 'envious', 'defeated', 'hopeless', 'fearful', 'anxious',
    'insecure', 'uneasy', 'stressed', 'tense'
  ];
  const neutralWords = [
    'alright', 'okay', 'fine', 'average', 'ordinary', 'neutral', 'indifferent', 'balanced',
    'mediocre', 'tolerable', 'acceptable', 'adequate', 'decent', 'moderate', 'reasonable',
    'fair', 'unremarkable', 'so-so', 'meh', 'nonchalant', 'detached', 'reserved', 'disinterested',
    'dispassionate', 'equable', 'impartial', 'unbiased', 'uninvolved', 'unemotional', 'uncommitted',
    'uncaring', 'unexcitable', 'unflappable', 'unexpressive', 'unfeeling', 'unimpressed', 'unresponsive',
    'unruffled', 'unstimulated', 'untroubled', 'unaffected', 'unimpassioned', 'unenthusiastic', 'uninspired',
    'uninterested', 'unfazed', 'uninspiring', 'uninspiring', 'unsympathetic', 'unbothered'
  ];

  const sentiment = calculateSentiment(userMessages, positiveWords, negativeWords, neutralWords);
  console.log('Sentiment:', sentiment);

  if (sentiment == 'extra-positive')
    window.location.href = 'rock.html';
  else if (sentiment == 'positive')
    window.location.href = 'dance.html';
  else if (sentiment == 'mild-negative')
    window.location.href = 'melody.html';
  else
    window.location.href = 'break.html';
}

