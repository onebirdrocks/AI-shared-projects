# API Documentation

This document describes the API endpoints for the Chat with PDF application.

## Base URL

All API requests should be made to: `http://localhost:8000`

## Endpoints

### Upload PDF

Uploads a PDF file to the server.

- **URL:** `/upload-pdf`
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Request Body:**
  - `file`: The PDF file to upload (required)

**Response:**
