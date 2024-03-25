import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-light navbar-light py-4">
      <div className="container">
        <a href="#" className="navbar-brand">Forecast Planner</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navmenu">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navmenu">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item"><a href="#about" className="nav-link">About</a></li>
            <li className="nav-item"><a href="#reviews" className="nav-link">Reviews</a></li>
            <li className="nav-item"><a href="#contact" className="nav-link">Contacts</a></li>
            <li className="nav-item"><a href="#signup" className="nav-link">Sign Up</a></li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
