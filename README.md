# Laboratory Copilot

A web-based AI agent that generates detailed bioscience wet lab protocols. The system uses OpenAI's GPT-4 to create comprehensive, step-by-step experimental protocols with detailed instructions, equipment lists, consumables, safety requirements, and timing information.

## Features

- **Interactive Protocol Generation**: Creates detailed wet lab protocols based on model organism, organ, and measurement type
- **Comprehensive Output**: Generates protocols with:
  - Step-by-step instructions
  - Required consumables (with quantities)
  - Lab equipment needed
  - Safety equipment requirements
  - Detailed timing information

## How It Works

The system uses a multi-stage approach to generate protocols:

1. **Initial Question Generation**: The AI analyzes the experiment requirements and generates specific questions to clarify experimental details
2. **Protocol Design**: Based on the answers, it creates a detailed protocol structure with all necessary steps
3. **Quantity Addition**: Adds specific quantities for all consumables, equipment, and safety items
4. **Final Protocol**: Compiles everything into a comprehensive, markdown-formatted protocol

## Project Structure

```
laboratory-copilot/
├── app2_edited.py          # Main protocol generation logic
├── templates/
│   └── index.html          # Web interface HTML
├── static/
│   ├── css/
│   │   └── style.css       # Styling for web interface
│   └── js/
│       └── script.js       # Frontend JavaScript
└── README.md               # This file
```

## Prerequisites

- Python 3.7+
- OpenAI API key
- Flask (for web interface)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd laboratory-copilot
```

2. Install required dependencies:
```bash
pip install openai flask
```

3. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file (if using python-dotenv):
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Web Interface (Recommended)

1. Start the Flask server (you may need to create a Flask app file that integrates `app2_edited.py`):
```bash
python app.py  # If Flask app exists
```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter your experiment details:
   - Model organism (e.g., "mouse")
   - Organ of interest (e.g., "lung")
   - Measurement type (e.g., "single-cell RNA seq 10x genomics chromium chip")

4. Answer the clarifying questions presented by the system

5. Review the generated protocol

### Command Line

You can also run the script directly:
```bash
python app2_edited.py
```

Note: The current version has hardcoded values for model organism, organ, and measurement. Modify these in the script or adapt it to accept user input.

## Configuration

The script uses the following default settings:
- **Model**: `gpt-4-1106-preview`
- **Max tokens (small)**: 300 (for question generation)
- **Max tokens (limit)**: 2500 (for protocol generation)
- **Temperature**: 0.0 (for deterministic outputs)

You can modify these in `app2_edited.py`:
```python
model = 'gpt-4-1106-preview'
max_token_small = 300
max_token_limit = 2500
```

## Protocol Output Format

The generated protocol includes:

- **Experiment Steps**: Numbered steps with detailed instructions
- **Consumables Required**: Items with quantities and units
- **Safety Equipment**: Required safety gear with quantities
- **Lab Equipment**: Equipment needed with quantities
- **Timing Details**: Specific timing information for each step

Example output structure:
```json
{
  "experiment_steps": [
    {
      "step_number": 1,
      "instruction": "Prepare the extraction solution.",
      "consumables_required": [
        {"item": "70% ethanol", "quantity": "100", "unit": "ml"}
      ],
      "safety_equipment_required": [
        {"item": "Gloves", "quantity": "1", "unit": "pair"}
      ],
      "lab_equipment": [
        {"item": "beaker", "quantity": "1", "unit": "count"}
      ],
      "details_on_timing": "Allow the solution to mix thoroughly for about 2 minutes."
    }
  ]
}
```

## Development

To extend the functionality:

1. **Web Interface Integration**: Create a Flask app that wraps the protocol generation logic from `app2_edited.py`
2. **API Endpoints**: Add REST API endpoints for programmatic access
3. **Protocol Templates**: Create templates for common experiment types
4. **Export Formats**: Add PDF or Word document export capabilities

## Limitations

- Requires an active OpenAI API key with access to GPT-4
- API costs apply based on usage
- Generated protocols should be reviewed by experienced researchers before use
- The web interface expects a Flask server with an `/ask` endpoint (may need to be implemented)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Specify your license here]

## Acknowledgments

This project uses OpenAI's GPT-4 API for protocol generation.
