import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/common/Layout';
import Dashboard from './pages/Dashboard';
import CorridorMap from './pages/CorridorMap';
import Simulator from './pages/Simulator';
import Procurement from './pages/Procurement';
import Intelligence from './pages/Intelligence';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/overview" replace />} />
          <Route path="/overview" element={<Dashboard />} />
          <Route path="/map" element={<CorridorMap />} />
          <Route path="/simulator" element={<Simulator />} />
          <Route path="/procurement" element={<Procurement />} />
          <Route path="/intelligence" element={<Intelligence />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
