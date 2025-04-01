import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface FileListProps {
  onFileSelect: (fileName: string) => void;
  selectedFile: string;  // 添加这一行
  apiUrl: string;
}

const FileList: React.FC<FileListProps> = ({ onFileSelect, selectedFile, apiUrl }) => {
  const [files, setFiles] = useState<string[]>([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await axios.get(`${apiUrl}/files`);
      setFiles(response.data.files);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  return (
    <div>
      <h2 className="text-lg font-semibold mb-2">上传的文件</h2>
      <ul className="space-y-2">
        {files.map((file, index) => (
          <li 
            key={index} 
            className={`cursor-pointer p-2 rounded flex items-center ${file === selectedFile ? 'bg-blue-100' : 'hover:bg-gray-200'}`}
            onClick={() => onFileSelect(file)}
          >
            <svg className="w-5 h-5 mr-2 text-gray-500" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            {file}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList;