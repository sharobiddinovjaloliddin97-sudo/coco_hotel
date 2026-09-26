import apiClient from './client';

/**
 * Submit a guest callback request.
 * Payload: {
 *   full_name: string,
 *   phone: string,
 *   preferred_time?: string,
 *   message?: string,
 *   website?: string
 * }
 */
export async function createCallbackRequest(payload) {
  const response = await apiClient.post('/callback-requests/', payload);
  return {
    status: response.status,
    data: response.data,
  };
}

/**
 * Submit a guest contact message.
 * Payload: {
 *   full_name: string,
 *   email: string,
 *   phone?: string,
 *   subject: string,
 *   message: string,
 *   website?: string
 * }
 */
export async function createContactMessage(payload) {
  const response = await apiClient.post('/contact-messages/', payload);
  return {
    status: response.status,
    data: response.data,
  };
}
