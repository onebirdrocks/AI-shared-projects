import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface FileUploadProps {
  onFileUploaded: (fileName: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUploaded }) => {
  const [uploading, setUploading] = useState<boolean>(false);
  const [fileName, setFileName] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setFileName(file.name);
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);
      try {
        const response = await axios.post('http://localhost:8000/upload-pdf', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        onFileUploaded(response.data.file_name);
      } catch (error) {
        console.error('Error uploading file:', error);
      } finally {
        setUploading(false);
      }
    }
  }, [onFileUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'application/pdf',
    multiple: false
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition duration-300"
      >
        <input {...getInputProps()} />
        {uploading ? (
          <p className="text-blue-600">上传中...</p>
        ) : (
          <>
            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <p className="mt-4 text-sm text-gray-600">
              <span className="font-medium text-blue-600 hover:text-blue-500">
                点击上传文件
              </span>
              {' '}或拖拽文件到这里
            </p>
            <p className="mt-1 text-xs text-gray-500">仅支持 PDF 文件 (最大 10MB)</p>
          </>
        )}
      </div>
      {fileName && !uploading && (
        <div className="mt-4 flex items-center justify-between bg-gray-50 p-2 rounded">
          <span className="text-sm text-gray-600">{fileName}</span>
          <button
            onClick={() => setFileName('')}
            className="text-red-500 hover:text-red-700"
          >
            删除
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;