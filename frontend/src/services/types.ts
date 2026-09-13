export interface Server {
  id: number;
  name: string;
  provider: string;
  region: string;
  size: string;
  image: string;
  status: 'PENDING' | 'PROVISIONING' | 'BOOTSTRAPPING' | 'READY' | 'FAILED' | 'DESTROYING' | 'DESTROYED';
  ipv4: string | null;
  ipv6: string | null;
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: string;
  server_id: number;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  job_type: string;
  error_message: string | null;
  started_at: string | null;
  finished_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateServerRequest {
  name: string;
  provider: string;
  region: string;
  size: string;
  image: string;
}

export interface ProvisioningJobResponse {
  job_id: string;
  server_id: number;
  status: string;
}
