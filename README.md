# Business Idea Analyzer

This Streamlit application provides a comprehensive analysis of business ideas using AI-powered agents and web search capabilities.

## Features

- Interactive web interface for inputting business ideas
- Multi-agent analysis system covering various aspects of business planning
- Integration with web search for up-to-date information
- Visualizations including SWOT analysis and Business Model Canvas
- Detailed reports on market research, target audience, revenue models, and more

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/business-idea-analyzer.git
   cd business-idea-analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Enter your business idea in the input field and click the arrow button or press Enter

4. Wait for the analysis to complete and explore the results in the various tabs

## Project Structure

- `main.py`: The main Streamlit application
- `pages/`: Contains the different pages of the Streamlit app
- `agents/`: Individual AI agents for different aspects of business analysis
- `models/`: Configuration for the DSPy model
- `utils/`: Utility functions for web search and report generation

## Dependencies

- Streamlit
- DSPy
- Matplotlib
- Pillow
- Requests
- Python-dotenv
- OpenAI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
