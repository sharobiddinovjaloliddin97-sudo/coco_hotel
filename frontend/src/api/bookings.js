import apiClient from './client';

/**
 * Submit a guest booking inquiry request.
 * Payload: {
 *   room: number,
 *   check_in: string,
 *   check_out: string,
 *   adults: number,
 *   children: number,
 *   full_name: string,
 *   phone: string,
 *   email: string,
 *   special_request?: string
 * }
 */
export async function createBookingRequest(payload) {
  const response = await apiClient.post('/bookings/', payload);
  return {
    status: response.status,
    data: response.data,
  };
}

export default createBookingRequest;
