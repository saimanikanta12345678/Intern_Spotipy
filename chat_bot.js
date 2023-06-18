const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");
const apiKey = "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";

const userMessages = [];

const context = [
  {
    role: "system",
    content: `You are a bot, ask user different 
    questions to analyze the mood of the user and interact with the user,
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
  <img src="user.png" alt="user icon"> <span>${message}</span>
  </div>`;

  chatHistory.push({ role: "user", content: message });

  // Use axios library to make a POST request to the OpenAI API
  const response = await axios.post(
    "https://api.openai.com/v1/completions",
    {
      prompt: chatHistory.map((msg) => msg.content).join("\n"),
      model: "text-davinci-003",
      temperature: 0.5,
      max_tokens: 1000,
      top_p: 1,
      frequency_penalty: 0.0,
      presence_penalty: 0.6,
    },
    {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
    }
  );
  const chatbotResponse = response.data.choices[0].text.trim();

  chatHistory.push({ role: "system", content: chatbotResponse });
  console.log(userMessages); // Print the userMessages array
  messages.innerHTML += `<div class="message bot-message">
  <img src="bot.jpeg" alt="bot icon"> <span>${chatbotResponse}</span>
  </div>`;
});