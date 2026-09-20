import request from '../utils/request'

export function listReservations(params) {
  return request.get('/reservation/list', { params })
}

export function createReservation(data) {
  return request.post('/reservation', data)
}

export function cancelReservation(id) {
  return request.post(`/reservation/${id}/cancel`)
}

export function approveReservation(id) {
  return request.post(`/reservation/${id}/approve`)
}

export function rejectReservation(id, data) {
  return request.post(`/reservation/${id}/reject`, data)
}
