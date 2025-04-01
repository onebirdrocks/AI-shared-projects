import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import FileUpload from './FileUpload';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('FileUpload Component', () => {
  const mockOnFileUploaded = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders FileUpload component', () => {
    render(<FileUpload onFileUploaded={mockOnFileUploaded} />);
    const uploadText = screen.getByText(/拖放 PDF 文件到此处，或点击选择文件/i);
    expect(uploadText).toBeInTheDocument();
  });

  test('handles file selection', async () => {
    mockedAxios.post.mockResolvedValue({ data: { file_name: 'test.pdf' } });
    render(<FileUpload onFileUploaded={mockOnFileUploaded} />);
    const input = screen.getByLabelText(/选择 PDF 文件/i);
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(input, { target: { files: [file] } });
    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/upload-pdf',
        expect.any(FormData),
        expect.any(Object)
      );
      expect(mockOnFileUploaded).toHaveBeenCalledWith('test.pdf');
    });
  });

  test('handles upload error', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { error: 'Upload failed' } } });
    render(<FileUpload onFileUploaded={mockOnFileUploaded} />);
    const input = screen.getByLabelText(/选择 PDF 文件/i);
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(input, { target: { files: [file] } });
    await waitFor(() => {
      expect(console.error).toHaveBeenCalledWith('Error uploading file:', expect.any(Object));
    });
  });

  test('displays uploading state', async () => {
    mockedAxios.post.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({ data: { file_name: 'test.pdf' } }), 100)));
    render(<FileUpload onFileUploaded={mockOnFileUploaded} />);
    const input = screen.getByLabelText(/选择 PDF 文件/i);
    const file = new File(['dummy content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(input, { target: { files: [file] } });
    expect(screen.getByText(/上传中.../i)).toBeInTheDocument();
  });
});