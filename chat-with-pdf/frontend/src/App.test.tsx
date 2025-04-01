import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from './App';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('App Component', () => {
  test('renders Chat with PDF title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Chat with PDF/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders upload instruction when no file is selected', () => {
    render(<App />);
    const instructionElement = screen.getByText(/请上传或选择一个PDF文件开始聊天/i);
    expect(instructionElement).toBeInTheDocument();
  });

  test('displays file list when files are available', async () => {
    mockedAxios.get.mockResolvedValue({ data: { files: ['test1.pdf', 'test2.pdf'] } });
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText('test1.pdf')).toBeInTheDocument();
      expect(screen.getByText('test2.pdf')).toBeInTheDocument();
    });
  });

  test('displays error toast when file upload fails', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { error: 'Upload failed' } } });
    render(<App />);
    const uploadButton = screen.getByText(/选择PDF文件/i);
    fireEvent.click(uploadButton);
    await waitFor(() => {
      expect(screen.getByText('Upload failed')).toBeInTheDocument();
    });
  });

  test('switches to chat view when file is selected', async () => {
    mockedAxios.get.mockResolvedValue({ data: { files: ['test.pdf'] } });
    render(<App />);
    await waitFor(() => {
      const fileItem = screen.getByText('test.pdf');
      fireEvent.click(fileItem);
      expect(screen.queryByText(/请上传或选择一个PDF文件开始聊天/i)).not.toBeInTheDocument();
      expect(screen.getByText(/输入您的问题/i)).toBeInTheDocument();
    });
  });
});