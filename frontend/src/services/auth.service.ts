import api from "../api/axios";
import type {
  LoginRequest,
  LoginResponse,
} from "../types/auth";

class AuthService {

  async login(
    payload: LoginRequest
  ): Promise<LoginResponse> {

    const response =
      await api.post<LoginResponse>(
        "/auth/login",
        payload
      );

    localStorage.setItem(
      "token",
      response.data.access_token
    );

    return response.data;
  }

  logout() {
    localStorage.removeItem("token");
  }

  getToken() {
    return localStorage.getItem("token");
  }

  isAuthenticated() {
    return !!this.getToken();
  }
}

export default new AuthService();