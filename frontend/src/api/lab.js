import request from '../utils/request'

export function listLabs(params) {
  return request.get('/lab/list', { params })
}

export function getLab(id) {
  return request.get(`/lab/${id}`)
}

export function createLab(data) {
  return request.post('/lab', data)
}

export function updateLab(id, data) {
  return request.put(`/lab/${id}`, data)
}

export function deleteLab(id) {
  return request.delete(`/lab/${id}`)
}
