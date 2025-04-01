con# Chat with PDF

Chat with PDF is a web application that allows users to upload PDF files and interact with their content through a chat interface. The application uses RAG (Retrieval-Augmented Generation) to provide accurate responses based on the content of the uploaded PDFs.

## Features

- PDF file upload and management
- Real-time chat interface
- PDF content viewing
- RAG-based question answering
- WebSocket for real-time communication

## Tech Stack

- Frontend: React, TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Machine Learning: Langchain, Ollama (qwen2 model), FAISS

## Prerequisites

- Node.js v20.17 or later
- Python 3.10 or later
- Ollama with qwen2 and nomic-embed-text models installed

## Installation

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required packages:
   ```
   npm install
   ```

## Configuration

1. Create a `.env` file in the backend directory with the following content:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   UPLOAD_DIR=uploads
   DB_PATH=db
   ```

2. Ensure Ollama is running and the required models are installed.

## Running the Application

1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Upload a PDF file using the upload interface.
2. Select the uploaded file from the file list.
3. View the PDF content in the viewer.
4. Ask questions about the PDF content in the chat interface.

## API Documentation

For detailed API documentation, please refer to `docs/api-docs.md`.

## Architecture

For information about the application's architecture, please refer to `docs/architecture.md`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.