import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav
      style={{
        background: "#1976d2",
        color: "white",
        padding: "15px",
        display: "flex",
        justifyContent: "space-between",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "20px",
        }}
      >
        <Link
          to="/documents"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          Documents
        </Link>

        <Link
          to="/documents/upload"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          Upload
        </Link>

        <Link
          to="/review"
          style={{
            color: "white",
            textDecoration: "none",
          }}
        >
          Review Queue
        </Link>
        <Link
            to="/audit"
            style={{
                color:"white",
                textDecoration:"none"
            }}
            >
            Audit Logs
        </Link>
        <Link to="/patients"> Patients</Link>
      </div>

      <button
        onClick={logout}
        style={{
          background: "#dc3545",
          color: "white",
          border: "none",
          padding: "8px 16px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </nav>
  );
}

export default Navbar;