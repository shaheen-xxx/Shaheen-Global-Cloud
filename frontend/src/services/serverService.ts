import apiClient from './api';
import { Server, Job, CreateServerRequest, ProvisioningJobResponse } from './types';

export const serverService = {
  async createServer(data: CreateServerRequest): Promise<ProvisioningJobResponse> {
    const response = await apiClient.post<ProvisioningJobResponse>('/v1/servers/', data);
    return response.data;
  },

  async listServers(): Promise<Server[]> {
    const response = await apiClient.get<{ total: number; servers: Server[] }>('/v1/servers/');
    return response.data.servers;
  },

  async getServer(id: number): Promise<Server> {
    const response = await apiClient.get<Server>(`/v1/servers/${id}`);
    return response.data;
  },

  async getJob(jobId: string): Promise<Job> {
    const response = await apiClient.get<Job>(`/v1/jobs/${jobId}`);
    return response.data;
  },

  async destroyServer(id: number) {
    const response = await apiClient.post(`/v1/servers/${id}/destroy`);
    return response.data;
  },
};
