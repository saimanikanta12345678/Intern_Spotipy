const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");

const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();
async function getSecretValue() {
  const [version] = await client.accessSecretVersion({
    name: 'projects/569816125116/secrets/music/versions/1',
  });

  const secretValue = version.payload.data.toString();
  return secretValue;
}

// Call the function to get the secret value
getSecretValue()
  .then(secretValue => {
    // Use the secret value in your code
    console.log('Secret value:', secretValue);
  })
  .catch(err => {
    console.error('Error retrieving secret value:', err);
  });



const userMessages=[];
const context = [
  {
    role: "system",
    content: `You are a bot, start every response with "BOT :". Ask  different 
    questions how did the day went to analyze the mood of the user,
    and every response ends with " amigo"`,
  },
];

let chatHistory = [...context];

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value;
  input.value = "";
  userMessages.push(message);

  messages.innerHTML += `<div class="message user-message">
  <img src="https://static.vecteezy.com/system/resources/previews/008/442/086/original/illustration-of-human-icon-user-symbol-icon-modern-design-on-blank-background-free-vector.jpg"> <span>${message}</span>
  </div>`;

  chatHistory.push({ role: "user", content: message });
  document.getElementById('endChatButton').addEventListener('click', function() 
  {
    endChat();
  });

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
        }
        else if(total>-1){
          sentiment='mild-negative'
        }
        else if(total<-1){
          sentiment='negative';
        }
        return sentiment;
      }
      
      function calculateSentimentRatios(userMessages) {
        const positiveWords = ['love','happy','good','great','excellent','wonderful','amazing','fantastic','awesome','like','beautiful','best',
        'nice','fantastic','fun','enjoy','sweet','perfect','superb','incredible','cool','outstanding','fantastic','fabulous','splendid','charming','delightful','lovely','marvelous',
        'impressive','optimistic','enchanting','refreshing','brilliant','extraordinary','remarkable','heartwarming','genius','genius','innovative',
        'exceptional','genius','generous','phenomenal','breathtaking','admirable','captivating','cherished','enthusiastic','blissful','victorious','vibrant','harmonious',
        'radiant','honorable','authentic','illustrious','benevolent','respected','reputable','prestigious','diligent','noble','elegant','splendid',
        'exuberant','affectionate','compassionate','grateful','thrilled','triumphant','jolly','vivacious','loving','spirited','uplifting',
        'satisfied', 'creative','confident','optimistic','happy','positive','vibrant','charming','delightful',
        'radiant','glowing','inspired','hopeful','proud','content','elated','grateful','joyous','passionate','warm','generous','kind','friendly','supportive'
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

        if(sentiment=='extra-positive')
        window.location.href = '/static/rock.html';
      else if(sentiment=='positive')
        window.location.href = '/static/dance.html';
      else if(sentiment=='mild-negative')
        window.location.href = '/static/melody.html';
      else
        window.location.href='/static/break.html'

  //       const sentimentElement = document.getElementById('sentiment');
  // sentimentElement.textContent = sentiment;
      }
      
   

  
  function endChat() {
    
      // window.location.href = 'end.html';

       calculateSentimentRatios(userMessages);
    
      // You can also use other methods to end the chat, such as redirecting the user to another page or closing the chat window
  }
  
  // Use axios library to make a POST request to the OpenAI API
  const response = await axios.post(
    "https://api.openai.com/v1/completions",
    {
      prompt: chatHistory.map((msg) => msg.content).join("\n"),
      model: "text-davinci-003",
      temperature: 0,
      max_tokens: 1000,
      top_p: 1,
      frequency_penalty: 0.0,
      presence_penalty: 0.0,
    },
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
    }
  );
  const chatbotResponse = response.data.choices[0].text.trim();
  chatHistory.push({ role: "system", content: chatbotResponse});

  // console.log("User Messages:", userMessages);

  messages.innerHTML += `<div class="message bot-message">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnkSMoVY9bC1_nVw__jEl9UBlaGoVX-FHLUiJoJW9CHw&usqp=CAU&ec=48665701"> <span>${chatbotResponse}</span>
  </div>`;
  messages.scrollTop=messages.scrollHeight;

});