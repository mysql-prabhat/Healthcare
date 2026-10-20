import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "../services/auth.service";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      setLoading(true);

      await AuthService.login({
        username,
        password,
      });

      //navigate("/dashboard");
      navigate("/documents");

    } catch {
      setError(
        "Invalid username or password"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Healthcare AI Platform</h1>

      <form onSubmit={handleSubmit}>

        <input
          placeholder="Username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          disabled={loading}
          type="submit"
        >
          {loading
            ? "Logging in..."
            : "Login"}
        </button>

        {error && <p>{error}</p>}

      </form>
    </div>
  );
}

export default Login;