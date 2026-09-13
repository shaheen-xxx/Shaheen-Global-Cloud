import React, { useState, useEffect } from 'react';
import { Server } from '../services/types';
import { serverService } from '../services/serverService';
import { CreateServerForm } from './CreateServerForm';
import { ServerList } from './ServerList';
import { ServerDetails } from './ServerDetails';

type View = 'list' | 'create' | 'details';

export const Dashboard: React.FC = () => {
  const [view, setView] = useState<View>('list');
  const [servers, setServers] = useState<Server[]>([]);
  const [selectedServer, setSelectedServer] = useState<Server | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [creating, setCreating] = useState(false);
  const [destroying, setDestroying] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load servers on mount and periodically refresh
  useEffect(() => {
    loadServers();
    const interval = setInterval(loadServers, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  // Refresh selected server details
  useEffect(() => {
    if (selectedServer && view === 'details') {
      const interval = setInterval(async () => {
        try {
          const updated = await serverService.getServer(selectedServer.id);
          setSelectedServer(updated);
          setServers((prev) =>
            prev.map((s) => (s.id === updated.id ? updated : s))
          );
        } catch (err) {
          console.error('Failed to refresh server details', err);
        }
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [selectedServer, view]);

  const loadServers = async () => {
    try {
      if (view === 'list') {
        setRefreshing(true);
      }
      const data = await serverService.listServers();
      setServers(data);
      setLoading(false);
      setRefreshing(false);
    } catch (err) {
      setError('Failed to load servers');
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleCreateServer = async (data) => {
    setCreating(true);
    setError(null);
    try {
      const response = await serverService.createServer(data);
      setSuccessMessage(`Server "${data.name}" is being provisioned. Job ID: ${response.job_id}`);
      setTimeout(() => setSuccessMessage(null), 5000);
      await loadServers();
      setView('list');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create server');
    } finally {
      setCreating(false);
    }
  };

  const handleSelectServer = (server: Server) => {
    setSelectedServer(server);
    setView('details');
  };

  const handleDestroyServer = async () => {
    if (!selectedServer) return;
    setDestroying(true);
    setError(null);
    try {
      await serverService.destroyServer(selectedServer.id);
      setSuccessMessage('Server destruction initiated');
      setTimeout(() => setSuccessMessage(null), 5000);
      await loadServers();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to destroy server');
    } finally {
      setDestroying(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Shaheen Global Cloud</h1>
          <p className="text-gray-600 mt-2">Cloud provisioning made simple</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {successMessage && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 font-medium">✓ {successMessage}</p>
          </div>
        )}

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">✗ {error}</p>
          </div>
        )}

        {view === 'list' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">My Servers</h2>
              <button
                onClick={() => setView('create')}
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
              >
                + Create Server
              </button>
            </div>
            <ServerList
              servers={servers}
              onSelectServer={handleSelectServer}
              loading={loading}
              refreshing={refreshing}
            />
          </div>
        )}

        {view === 'create' && (
          <div className="space-y-6">
            <button
              onClick={() => setView('list')}
              className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
            >
              ← Back to Servers
            </button>
            <CreateServerForm onSubmit={handleCreateServer} loading={creating} />
          </div>
        )}

        {view === 'details' && selectedServer && (
          <ServerDetails
            server={selectedServer}
            onBack={() => setView('list')}
            onDestroy={handleDestroyServer}
            destroying={destroying}
          />
        )}
      </main>
    </div>
  );
};
