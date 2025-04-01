import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUpload from '../components/FileUpload';

const UploadPage: React.FC = () => {
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const navigate = useNavigate();

  const handleFileUploaded = (fileName: string) => {
    setUploadStatus(`文件 ${fileName} 上传成功!`);
    setTimeout(() => {
      navigate(`/chat/${fileName}`);
    }, 2000);
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-blue-50 pt-20">
      <div className="w-full max-w-md text-center">
        <div className="flex items-center justify-center mb-2">
          <svg className="w-8 h-8 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <h1 className="text-3xl font-bold text-blue-600">Chat with PDF</h1>
        </div>
        <p className="text-gray-600 mb-8">上传 PDF 文件或选择已有文件开始聊天</p>
        <div className="bg-white p-8 rounded-lg shadow-md">
          <FileUpload onFileUploaded={handleFileUploaded} />
          {uploadStatus && (
            <p className="mt-4 text-green-600 text-center">{uploadStatus}</p>
          )}
        </div>
        <button
          onClick={handleChatClick}
          className="mt-6 w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition duration-300 font-semibold"
        >
          Chat with PDF
        </button>
      </div>
    </div>
  );
};

export default UploadPage;