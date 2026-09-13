import React, { useState, useEffect } from 'react';
import { Server } from '../services/types';
import { formatDistanceToNow } from 'date-fns';

interface ServerListProps {
  servers: Server[];
  onSelectServer: (server: Server) => void;
  loading: boolean;
  refreshing: boolean;
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

export const ServerList: React.FC<ServerListProps> = ({
  servers,
  onSelectServer,
  loading,
  refreshing,
}) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading servers...</p>
        </div>
      </div>
    );
  }

  if (servers.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <p className="text-gray-600 mb-4">No servers yet</p>
        <p className="text-sm text-gray-500">Create your first server to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {refreshing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
          <span className="text-sm text-blue-800">Refreshing servers...</span>
        </div>
      )}
      <div className="grid gap-4">
        {servers.map((server) => (
          <div
            key={server.id}
            onClick={() => onSelectServer(server)}
            className="bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer border border-gray-200 hover:border-blue-300 p-6"
          >
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{server.name}</h3>
                <p className="text-sm text-gray-600 mt-1">
                  {server.provider} • {server.region} • {server.size}
                </p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(server.status)}`}>
                {server.status}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">OS:</span>
                <p className="font-medium text-gray-900">{server.image}</p>
              </div>
              <div>
                <span className="text-gray-600">IPv4:</span>
                <p className="font-medium text-gray-900 font-mono">{server.ipv4 || '-'}</p>
              </div>
              <div>
                <span className="text-gray-600">Created:</span>
                <p className="font-medium text-gray-900">{formatDistanceToNow(new Date(server.created_at), { addSuffix: true })}</p>
              </div>
              <div>
                <span className="text-gray-600">IPv6:</span>
                <p className="font-medium text-gray-900 font-mono text-xs">{server.ipv6 || '-'}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
