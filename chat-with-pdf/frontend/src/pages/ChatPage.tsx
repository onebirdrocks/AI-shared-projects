import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import FileList from '../components/FileList';
import PDFViewer from '../components/PDFViewer';
import Chat from '../components/Chat';

const ChatPage: React.FC = () => {
  const { fileName } = useParams<{ fileName: string }>();
  const [selectedFile, setSelectedFile] = useState<string>(fileName || '');

  const handleFileSelect = (file: string) => {
    setSelectedFile(file);
  };

  return (
    <div className="flex h-screen">
      {/* 左侧文件列表 */}
      <div className="w-1/5 bg-gray-100 p-4 overflow-y-auto">
        <FileList 
          onFileSelect={handleFileSelect} 
          selectedFile={selectedFile}
          apiUrl="http://localhost:8000"
        />
      </div>

      {/* 中间 PDF 查看器 */}
      <div className="w-2/5 p-4 flex flex-col overflow-y-auto">
        <PDFViewer fileName={selectedFile} />
      </div>

      {/* 右侧聊天界面 */}
      <div className="w-2/5 flex flex-col">
        <Chat fileName={selectedFile} />
      </div>
    </div>
  );
};

export default ChatPage;