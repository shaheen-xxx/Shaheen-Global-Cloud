import React from 'react';
import { Server } from '../services/types';
import { formatDistanceToNow } from 'date-fns';

interface ServerDetailsProps {
  server: Server;
  onBack: () => void;
  onDestroy: () => Promise<void>;
  destroying: boolean;
}

const getStatusColor = (status: string): string => {
  switch (status) {
    case 'READY':
      return 'bg-green-100 text-green-800';
    case 'PROVISIONING':
    case 'BOOTSTRAPPING':
      return 'bg-blue-100 text-blue-800';
    case 'PENDING':
      return 'bg-yellow-100 text-yellow-800';
    case 'FAILED':
      return 'bg-red-100 text-red-800';
    case 'DESTROYING':
      return 'bg-orange-100 text-orange-800';
    case 'DESTROYED':
      return 'bg-gray-100 text-gray-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export const ServerDetails: React.FC<ServerDetailsProps> = ({
  server,
  onBack,
  onDestroy,
  destroying,
}) => {
  const isAlive = !['DESTROYED', 'FAILED'].includes(server.status);

  return (
    <div className="space-y-6">
      <button
        onClick={onBack}
        className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
      >
        ← Back to Servers
      </button>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{server.name}</h1>
            <p className="text-gray-600 mt-2">{server.provider.toUpperCase()} • {server.region}</p>
          </div>
          <span className={`px-4 py-2 rounded-lg text-lg font-bold ${getStatusColor(server.status)}`}>
            {server.status}
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">Operating System</p>
            <p className="text-lg font-semibold text-gray-900">{server.image}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">Server Size</p>
            <p className="text-lg font-semibold text-gray-900">{server.size}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">Provider Region</p>
            <p className="text-lg font-semibold text-gray-900">{server.region}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">IPv4 Address</p>
            <p className="text-lg font-mono font-semibold text-gray-900">
              {server.ipv4 || <span className="text-gray-400">Not assigned</span>}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">IPv6 Address</p>
            <p className="text-lg font-mono font-semibold text-gray-900 text-xs">
              {server.ipv6 || <span className="text-gray-400">Not assigned</span>}
            </p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 font-medium mb-1">Created</p>
            <p className="text-lg font-semibold text-gray-900">
              {formatDistanceToNow(new Date(server.created_at), { addSuffix: true })}
            </p>
          </div>
        </div>

        {server.status === 'PROVISIONING' || server.status === 'BOOTSTRAPPING' ? (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-4"></div>
              <div>
                <p className="font-semibold text-blue-900">Server is being provisioned</p>
                <p className="text-blue-800 text-sm mt-1">
                  {server.status === 'PROVISIONING' ? 'Infrastructure is being created...' : 'System is being configured...'}
                </p>
              </div>
            </div>
          </div>
        ) : null}

        {server.status === 'READY' ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
            <p className="font-semibold text-green-900">✓ Server is ready</p>
            <p className="text-green-800 text-sm mt-1">You can now connect to your server via SSH</p>
          </div>
        ) : null}

        {server.status === 'FAILED' ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
            <p className="font-semibold text-red-900">✗ Provisioning failed</p>
            <p className="text-red-800 text-sm mt-1">The server could not be created. Please try again.</p>
          </div>
        ) : null}

        {isAlive && (
          <div className="flex gap-4">
            <button
              onClick={onDestroy}
              disabled={destroying}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors flex items-center"
            >
              {destroying && (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              )}
              {destroying ? 'Destroying...' : 'Destroy Server'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
