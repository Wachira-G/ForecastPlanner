import { Routes, Route } from 'react-router-dom';
import Signup from './components/Signup';

function App() {
  return (
    <Routes>
        <Route path="register" element={<Signup />} />
        </Routes>
      );
    }

    export default App;
