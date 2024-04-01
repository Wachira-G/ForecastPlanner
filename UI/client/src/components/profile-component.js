import React, { Component } from "react";
import { Redirect } from 'react-router-dom';
import { connect } from "react-redux";
import Weather from "./weather-component";

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
                                                <div class="nav nav-tabs nav-justified" id="nav-tab" role="tablist">
                                                  <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="true">Weather Pattern</button>
                                                  <button class="nav-link" id="nav-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-profile" type="button" role="tab" aria-controls="nav-profile" aria-selected="false">My next destination</button>
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
                <p className="text-warning bg-secondary">PREVIOUS DESTINATION</p>
                <p><a href="destination?id=1">Kenya National Park</a></p>
                <p><a href="destination?id=3">Zanzibar Island</a></p>
                <p className="text-warning bg-dark">CURRENT DESTINATION</p>
                <p><a href="destination?id=3">Zanzibar Island</a></p>
                <p className="text-warning bg-info">WALLDROP SUGGESTION</p>
                <p><a href="destination?id=3">Weather: Rainny</a></p>
                <p><a href="destination?id=3">Walldrop: Warm clothes</a></p>

              </div>
            </div>
            <div className="col-md-8">
              <div className="tab-content" id="nav-tabContent">
                <div className="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                  {/* Add weather component here */}
                  <Weather />
                </div>
                <div className="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
                <div className="form p-5">
                  <form method="POST">
                    <div className="mb-3">
                        <label for="cityname" className="" data-placeholder-label="Name (optional)">City Name:</label>
                        <input type="text" className="form-control" id="name" placeholder=""/>
                    </div>
                    <div class="mb-3">
                        <label for="traveDate" className="" data-placeholder-label="Email (optional)">Travel Dates:</label>
                        <input type="date" className="form-control" id="traveDate" placeholder=""/>
                    </div>
                    <div class="mb-3">
                        <label for="activities" className="" data-placeholder-label="Feedback">Number of days</label>
                        <input class="form-control" id="activities" rows="5" placeholder=""/>
                    </div>
                    <button type="submit" className="btn btn-warning">Enter</button>
                  </form>
                  </div>
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
