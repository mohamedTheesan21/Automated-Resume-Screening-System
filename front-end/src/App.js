import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./Components/Login/Login.jsx";
import Signup from "./Components/Signup/Signup.jsx"
import Home from "./Components/Home/Home.jsx"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
