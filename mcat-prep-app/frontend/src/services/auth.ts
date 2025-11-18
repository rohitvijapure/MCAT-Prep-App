import api from './api'
import type { LoginCredentials, RegisterData, AuthResponse, User } from '@/types'

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/api/auth/login', credentials)
    const { access_token, refresh_token } = response.data

    // Store tokens
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)

    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/api/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/api/users/me')
    return response.data
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.put<User>('/api/users/me', data)
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/login'
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  },
}
