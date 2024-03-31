import React, { Component } from "react";
import { Redirect } from 'react-router-dom';
import { connect } from "react-redux";

class Profile extends Component {

  render() {
    const { user: currentUser } = this.props;

    if (!currentUser) {
      return <Redirect to="/login" />;
    }

    return (
      <div className="container">
        <div className="emp-profile">
          <div className="row">
            <div className="col-md-4">
              <div className="profile-img">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS52y5aInsxSm31CvHOFHWujqUx_wWTS9iM6s7BAm21oEN_RiGoog" alt=""/>
              </div>
            </div>
            <div className="col-md-6">
              <div className="profile-head">
                <h5>Sandra Kush</h5>
                <p className="proile-rating">Frequent Place: <span>Mombasa Diani</span></p>
                <nav>
                  <div className="nav nav-tabs nav-justified" id="nav-tab" role="tablist">
                    <button className="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="true">Weather Pattern</button>
                    <button className="nav-link" id="nav-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-profile" type="button" role="tab" aria-controls="nav-profile" aria-selected="false">My next destination</button>
                  </div>
                </nav>
              </div>
            </div>
            <div className="col-md-2">
              <input type="submit" className="profile-edit-btn" name="btnAddMore" value="Edit Profile"/>
            </div>
          </div>
          <div className="row">
            <div className="col-md-4">
              <div className="profile-work">
                <p>WORK LINK</p>
                <a href="">Website Link</a><br/>
                <a href="">Bootsnipp Profile</a><br/>
                <a href="">Bootply Profile</a>
                <p>SKILLS</p>
                <a href="">Web Designer</a><br/>
                <a href="">Web Developer</a><br/>
                <a href="">WordPress</a><br/>
                <a href="">WooCommerce</a><br/>
                <a href="">PHP, .Net</a><br/>
              </div>
            </div>
            <div className="col-md-8">
              <div className="tab-content" id="nav-tabContent">
                <div className="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                  <div className="weather-container-two">
                    <div className="weather-input" style={{ width: '100% !important' }}>
                      <h5>Enter Name Of A City</h5>
                      <input className="city-input" type="text" placeholder="E.g., Nairobi, Kisumu"/>
                      <button className="search-btn bg-warning">Search</button>
                      <div className="separator"></div>
                      <button id="locationNameBtn" className="location-btn">Use Current Location</button>
                    </div>
                    <div className="weather-data" style={{ marginTop: '30px' }}>
                      <div className="current-weather">
                        <div className="details">
                          <h2></h2>
                          <h6>Temperature: __°C</h6>
                          <h6>Wind: __ M/S</h6>
                          <h6>Humidity: __%</h6>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
                  Another here
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  const { user } = state.auth;
  return {
    user,
  };
}

export default connect(mapStateToProps)(Profile);
