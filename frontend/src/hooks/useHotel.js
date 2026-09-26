import { useContext } from 'react';
import { HotelContext } from '../context/hotelContextDef';

export function useHotel() {
  return useContext(HotelContext);
}

export default useHotel;
