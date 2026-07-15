import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/common/Layout';
import Dashboard from './pages/Dashboard';
import CorridorMap from './pages/CorridorMap';
import Simulator from './pages/Simulator';
import Procurement from './pages/Procurement';
import Intelligence from './pages/Intelligence';
import Landing from './pages/Landing';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/*" element={
          <Layout>
            <Routes>
              <Route path="/overview" element={<Dashboard />} />
              <Route path="/map" element={<CorridorMap />} />
              <Route path="/simulator" element={<Simulator />} />
              <Route path="/procurement" element={<Procurement />} />
              <Route path="/intelligence" element={<Intelligence />} />
            </Routes>
          </Layout>
        } />
      </Routes>
    </Router>
  );
}

export default App;
