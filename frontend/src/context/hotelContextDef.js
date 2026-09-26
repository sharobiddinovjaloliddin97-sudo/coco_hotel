import { createContext } from 'react';

export const HotelContext = createContext({
  hotelInfo: null,
  loading: true,
  error: null,
});

export default HotelContext;
