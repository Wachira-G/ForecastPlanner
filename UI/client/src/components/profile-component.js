import React, { Component } from "react";
import { Redirect } from 'react-router-dom';
import { connect } from "react-redux";
import Weather from "./weather-component";
import ProfileService from "../services/profile-service";
import Destination from "./destination-component";
import Recommendation from "./recommendation-component";
import DestinationList from "./destination-list-component";

class Profile extends Component {
  constructor(props) {
    super(props);

    this.state = {
      content: "",
    };
  }

  componentDidMount() {
    this.fetchUserProfile();
  }

  fetchUserProfile() {
    ProfileService.getUserProfile()
      .then(response => {
        this.setState({
          content: response.data.email
        });
      })
      .catch(error => {
        this.setState({
          content:
            (error.response && error.response.data) ||
            error.message ||
            error.toString()
        });
      });
  }

  render() {
    const { user: currentUser } = this.props;
    const { content } = this.state;

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
                <h6>Email: {this.state.content}</h6>
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
                <DestinationList />
                <Recommendation />
              </div>
            </div>
            <div className="col-md-8">
              <div className="tab-content" id="nav-tabContent">
                <div className="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                  {/* Add weather component here */}
                  <Weather />
                </div>
                <div className="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
                  <Destination />
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
