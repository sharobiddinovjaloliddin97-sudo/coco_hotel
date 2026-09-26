import { apiClient } from './client';

export async function sendChatMessage(message, history = []) {
  const response = await apiClient.post(
    '/ai/chat/',
    {
      message,
      history,
    },
    {
      timeout: 35000,
    }
  );
  return response.data;
}

