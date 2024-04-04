import React, { Component } from "react";
import ProfileService from "../services/profile-service";

class DestinationList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      userId: null,
      destinations: [],
      loading: true,
      error: null
    };
  }

  componentDidMount() {
    this.fetchUserId();
  }

  fetchUserId() {
    ProfileService.getUserProfile()
      .then(response => {
        const { user_id } = response.data;
        this.setState({ userId: user_id });
        this.fetchPastDestinations(user_id);
      })
      .catch(error => {
        this.setState({ error: "Error fetching user profile", loading: false });
        console.error("Error fetching user profile:", error);
      });
  }

  fetchPastDestinations(userId) {
    ProfileService.getPastDestinations(userId)
      .then(response => {
        this.setState({
          destinations: response.data.destinations,
          loading: false
        });
      })
      .catch(error => {
        this.setState({
          error: "Error fetching past destinations",
          loading: false
        });
        console.error("Error fetching past destinations:", error);
      });
  }

  render() {
    const { destinations, loading, error } = this.state;

    if (loading) {
      return <div>Loading...</div>;
    }

    if (error) {
      return <div>Error: {error}</div>;
    }

    return (
      <div>
        <p className="text-warning bg-secondary">PREVIOUS DESTINATIONS</p>
        {destinations.map((destination, index) => (
          <p key={index}>
            <a href={`destination?id=${index + 1}`}>{destination.name}</a>
          </p>
        ))}
      </div>
    );
  }
}

export default DestinationList;
