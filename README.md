# Hi there!  Welcome to my Smarat Chatbot Project

Hey! I'm Rohit Garg, a fresher developer, and this is my chatbot project that I built using some really cool AI technology. It's basically a smart chatbot that can read documents and answer questions about them!

## What's Cool About This Project? 

- It can understand and answer questions about any document you give it
- Shows you exactly where it found the answers (no more black-box AI!)
- Has a nice, clean chat interface that's super easy to use
- Uses some cutting-edge AI models (Mistral-7B - pretty neat stuff!)

## Want to Try It Out? 

First, you'll need:
- Python installed on your computer
- An API key from OpenRouter (I'll explain how to get this)

### Setting Things Up 

1. First, grab all the code:
```bash
git clone https://github.com/Rohit-raj96/rag_chatbot_rohit.git
cd chatbot_rohit
```

2. Install all the necessary stuff:
```bash
pip install -r requirements.txt
```

3. Create a file named `.env` and put your API key in it like this:
```
OPENROUTER_API_KEY=your_api_key_here
```

### Running the Chatbot 

Just run this command:
```bash
streamlit run app.py
```

Then open your browser and go to `http://localhost:8501` - that's it!

## How I Organized Everything 

```
├── app.py              # The main chatbot code
├── src/                # Helper code I wrote
├── data/               # Where documents are stored
├── chunks/             # Document pieces for the AI
└── vectordb/          # The AI's "memory"
```

## What I Learned 

Building this project taught me a lot about:
- Working with AI models
- Building user interfaces with Streamlit
- Handling documents and text processing
- Managing API calls and responses

## Future Ideas 

I'm thinking of adding:
- Support for more document types
- Better answer accuracy
- A cooler interface
- Maybe voice input/output?

## Let's Connect! 

I'm always looking to learn and improve! If you have any suggestions or want to chat about the project, feel free to reach out!

## License

This project is open source - feel free to use it and learn from it!
