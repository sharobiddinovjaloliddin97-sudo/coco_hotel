// Only show photographs published by hotel staff, never unrelated stock rooms.
export function getRoomImageUrl(room) {
  return room?.primary_image?.image || room?.images?.find(item => item.image)?.image || null;
}
export function getRoomGalleryImages(room) {
  const images = room?.images?.filter(item => item.image) || [];
  if (images.length) return images;
  return room?.primary_image?.image ? [room.primary_image] : [];
}
