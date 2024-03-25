import RequireAuth from './components/RequireAuth';
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/" element={<Home />} />

        // <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
        //   <Route path="/" element={<Profile />} />
        // </Route>
      </Routes>
  );
}

export default App;
