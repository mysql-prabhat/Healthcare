import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";
import Documents from "./pages/Documents";
import DocumentUpload from "./pages/DocumentUpload";
import ReviewQueue from "./pages/ReviewQueue";
import MainLayout from "./layouts/MainLayout";
import AuditLogs from "./pages/AuditLogs";
import PatientDashboard from "./pages/PatientDashboard";
import Patients from "./pages/Patients";

function App() {
  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/documents" element={<Documents />} />
          <Route path="/documents/upload" element={<DocumentUpload />} />
          <Route path="/review" element={<ReviewQueue />} />
          <Route path="/audit"  element={<AuditLogs/>} />
          <Route path="/patients/:id" element={<PatientDashboard />} />
          <Route path="/patients" element={<Patients />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;