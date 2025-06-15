<h1>🤖 IIT Mandi JOSAA Counsellor Bot</h1>

<p>A smart <strong>Telegram bot</strong> built using <strong>Google Gemini</strong>, <strong>FAISS</strong>, and <strong>Semantic Search</strong> to assist students with <strong>JOSAA-related queries</strong> about <strong>IIT Mandi</strong> — including branches, placements, campus life, and more.</p>

<hr>

<h2>📌 Features</h2>
<ul>
  <li>💬 <strong>Ask Anything</strong> – From “VLSI vs CSE?” to “How’s the fest life at IIT Mandi?”</li>
  <li>📚 <strong>Context-Aware Answers</strong> – Uses top-matching content for rich, accurate answers</li>
  <li>🚀 <strong>Gemini 2.0 Flash API</strong> – Fast and reliable generative responses</li>
  <li>🧠 <strong>Semantic Search</strong> with Sentence Transformers</li>
  <li>🔗 <strong>Integrated with Telegram</strong> – Smooth chat-based interface</li>
</ul>

<hr>

<h2>🧱 Tech Stack</h2>
<table>
  <thead>
    <tr><th>Layer</th><th>Technology</th></tr>
  </thead>
  <tbody>
    <tr><td>LLM Backend</td><td>Google Gemini (gemini-2.0-flash)</td></tr>
    <tr><td>Embedding Model</td><td>sentence-transformers/all-MiniLM-L6-v2</td></tr>
    <tr><td>Vector DB</td><td>FAISS</td></tr>
    <tr><td>Bot Interface</td><td>python-telegram-bot</td></tr>
    <tr><td>Deployment</td><td>Python 3.10+</td></tr>
  </tbody>
</table>

<hr>

<h2>🛠 Installation & Setup</h2>

<h4>1. Clone the Repo</h4>
<pre><code>git clone https://github.com/your-username/iit-mandi-josaa-bot.git
cd iit-mandi-josaa-bot
</code></pre>

<h4>2. Install Dependencies</h4>
<pre><code>pip install -r requirements.txt
</code></pre>

<h4>3. Set Environment Variables</h4>
<pre><code> 

# On Linux/macOS
export API_KEY="your_google_gemini_api_key"
export JOSAA_BOT="your_telegram_bot_token"
# On Windows (CMD)
set API_KEY=your_google_gemini_api_key
set JOSAA_BOT=your_telegram_bot_token
</code></pre>

<h4>4. Required Files</h4>
<ul>
  <li><code>faiss_index.idx</code> – Precomputed FAISS index</li>
  <li><code>meta.json</code> – Metadata with text previews</li>
  <li><code>system.txt</code> – Optional system instruction prompt</li>
</ul>

<h4>5. Run the Bot</h4>
<pre><code>python bot.py
</code></pre>

<hr>
<h2>🔍 How it Works</h2>
<ol>
  <li><strong>User Input</strong> via Telegram</li>
  <li><strong>Semantic Search</strong> matches query against document chunks</li>
  <li><strong>Context Retrieval</strong> – Top-k text previews are selected</li>
  <li><strong>Prompt to Gemini</strong> – With system instructions and context</li>
  <li><strong>Response</strong> – Gemini returns final answer to user</li>
</ol>


<hr>

<h2>⭐ Credits</h2>
<ul>
  <li>Developed by Saksham Setia (BTech Microelectronics and VLSI, IIT Mandi)</li>
  <li>Powered by:
    <ul>
      <li><a href="https://ai.google.dev/">Google Gemini API</a></li>
      <li><a href="https://github.com/facebookresearch/faiss">FAISS</a></li>
      <li><a href="https://www.sbert.net/">Sentence Transformers</a></li>
      <li><a href="https://github.com/python-telegram-bot/python-telegram-bot">Python Telegram Bot</a></li>
    </ul>
  </li>
</ul>

<hr>

<h2>📄 License</h2>
<p>This project is open-sourced for learning and educational purposes. Please credit the author if reusing or adapting parts of it.</p>
