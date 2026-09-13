import React, { useState } from 'react';
import { CreateServerRequest } from '../services/types';

interface CreateServerFormProps {
  onSubmit: (data: CreateServerRequest) => Promise<void>;
  loading: boolean;
}

const PROVIDERS = [
  { value: 'mock', label: 'Mock (Testing)' },
  { value: 'hetzner', label: 'Hetzner Cloud' },
];

const REGIONS = {
  hetzner: [
    { value: 'fsn1', label: 'Falkenstein, Germany' },
    { value: 'nbg1', label: 'Nuremberg, Germany' },
    { value: 'ash', label: 'Ashburn, USA' },
    { value: 'hel1', label: 'Helsinki, Finland' },
  ],
  mock: [
    { value: 'fsn1', label: 'Falkenstein, Germany' },
    { value: 'us-east-1', label: 'US East' },
  ],
};

const SIZES = {
  hetzner: [
    { value: 'cx22', label: 'CX22 (2 vCPU, 4 GB RAM)' },
    { value: 'cx32', label: 'CX32 (2 vCPU, 8 GB RAM)' },
    { value: 'cx42', label: 'CX42 (4 vCPU, 16 GB RAM)' },
  ],
  mock: [
    { value: 'small', label: 'Small (1 vCPU, 1 GB)' },
    { value: 'medium', label: 'Medium (2 vCPU, 4 GB)' },
    { value: 'large', label: 'Large (4 vCPU, 8 GB)' },
  ],
};

const IMAGES = [
  { value: 'ubuntu-24.04', label: 'Ubuntu 24.04 LTS' },
  { value: 'ubuntu-22.04', label: 'Ubuntu 22.04 LTS' },
];

export const CreateServerForm: React.FC<CreateServerFormProps> = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState<CreateServerRequest>({
    name: '',
    provider: 'mock',
    region: 'fsn1',
    size: 'small',
    image: 'ubuntu-24.04',
  });
  const [error, setError] = useState<string | null>(null);

  const availableRegions = REGIONS[formData.provider as keyof typeof REGIONS] || REGIONS.mock;
  const availableSizes = SIZES[formData.provider as keyof typeof SIZES] || SIZES.mock;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const updated = { ...prev, [name]: value };
      // Reset region and size if provider changed
      if (name === 'provider') {
        updated.region = REGIONS[value as keyof typeof REGIONS]?.[0]?.value || 'fsn1';
        updated.size = SIZES[value as keyof typeof SIZES]?.[0]?.value || 'small';
      }
      return updated;
    });
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.name.trim()) {
      setError('Server name is required');
      return;
    }

    try {
      await onSubmit(formData);
      setFormData({
        name: '',
        provider: 'mock',
        region: 'fsn1',
        size: 'small',
        image: 'ubuntu-24.04',
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create server');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8 max-w-2xl">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Server</h2>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-medium">{error}</p>
        </div>
      )}

      <div className="space-y-6">
        {/* Server Name */}
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
            Server Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="e.g., web-server-01"
            disabled={loading}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        {/* Provider */}
        <div>
          <label htmlFor="provider" className="block text-sm font-medium text-gray-700 mb-2">
            Provider
          </label>
          <select
            id="provider"
            name="provider"
            value={formData.provider}
            onChange={handleChange}
            disabled={loading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            {PROVIDERS.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {/* Region */}
          <div>
            <label htmlFor="region" className="block text-sm font-medium text-gray-700 mb-2">
              Region
            </label>
            <select
              id="region"
              name="region"
              value={formData.region}
              onChange={handleChange}
              disabled={loading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              {availableRegions.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>

          {/* Size */}
          <div>
            <label htmlFor="size" className="block text-sm font-medium text-gray-700 mb-2">
              Server Size
            </label>
            <select
              id="size"
              name="size"
              value={formData.size}
              onChange={handleChange}
              disabled={loading}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              {availableSizes.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* OS Image */}
        <div>
          <label htmlFor="image" className="block text-sm font-medium text-gray-700 mb-2">
            Operating System
          </label>
          <select
            id="image"
            name="image"
            value={formData.image}
            onChange={handleChange}
            disabled={loading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            {IMAGES.map((img) => (
              <option key={img.value} value={img.value}>
                {img.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Submit Button */}
      <div className="mt-8">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          {loading && (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
          )}
          {loading ? 'Creating Server...' : 'Create Server'}
        </button>
      </div>
    </form>
  );
};
